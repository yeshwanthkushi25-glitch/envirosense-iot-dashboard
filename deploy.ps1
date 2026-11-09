# EnviroSense AWS One-Click Deployment Script
# Automatically packages and deploys CloudFormation/SAM stack and syncs S3 website

param (
    [string]$Region = "us-east-1",
    [string]$StackName = "envirosense"
)

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  EnviroSense — AWS Cloud Deployment (Learner Lab / $Region)" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Verify AWS CLI & Credentials
Write-Host "`n[1/4] Checking AWS Credentials..." -ForegroundColor Yellow
try {
    $identity = aws sts get-caller-identity | ConvertFrom-Json
    Write-Host "[OK] Connected as: $($identity.Arn)" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] AWS credentials expired or not configured!" -ForegroundColor Red
    Write-Host "Please update ~/.aws/credentials with your fresh AWS Learner Lab session and rerun." -ForegroundColor Yellow
    exit 1
}

# 2. Deploy Infrastructure with SAM or CloudFormation
Write-Host "`n[2/4] Deploying Serverless Infrastructure (Stack: $StackName)..." -ForegroundColor Yellow

$samAvailable = Get-Command sam -ErrorAction SilentlyContinue
if ($samAvailable) {
    Write-Host "Building with AWS SAM..." -ForegroundColor Cyan
    sam build
    sam deploy --stack-name $StackName --region $Region --resolve-s3 --capabilities CAPABILITY_IAM --no-confirm-changeset
} else {
    Write-Host "[INFO] SAM CLI not found. Falling back to AWS CloudFormation deploy..." -ForegroundColor Yellow
    # Create or use temporary deployment bucket for Lambda package
    $deployBucket = "envirosense-deploy-$($identity.Account)-$Region"
    Write-Host "Ensuring deployment bucket $deployBucket exists..." -ForegroundColor Cyan
    aws s3 mb "s3://$deployBucket" --region $Region 2>$null

    Write-Host "Packaging template..." -ForegroundColor Cyan
    aws cloudformation package --template-file template.yaml --s3-bucket $deployBucket --output-template-file packaged.yaml
    Write-Host "Deploying CloudFormation stack..." -ForegroundColor Cyan
    aws cloudformation deploy --template-file packaged.yaml --stack-name $StackName --region $Region --capabilities CAPABILITY_IAM
}

# 3. Retrieve Outputs
Write-Host "`n[3/4] Fetching Stack Outputs..." -ForegroundColor Yellow
$outputsJson = aws cloudformation describe-stacks --stack-name $StackName --region $Region --query "Stacks[0].Outputs" | ConvertFrom-Json

$apiUrl = ($outputsJson | Where-Object { $_.OutputKey -eq "EnviroApiUrl" }).OutputValue
$bucketName = ($outputsJson | Where-Object { $_.OutputKey -eq "DashboardBucketName" }).OutputValue
$websiteUrl = ($outputsJson | Where-Object { $_.OutputKey -eq "DashboardWebsiteUrl" }).OutputValue

Write-Host "  EnviroApiUrl:        $apiUrl" -ForegroundColor Green
Write-Host "  DashboardBucketName: $bucketName" -ForegroundColor Green
Write-Host "  DashboardWebsiteUrl: $websiteUrl" -ForegroundColor Green

# 4. Upload Frontend to S3
Write-Host "`n[4/4] Uploading Static Dashboard to S3 ($bucketName)..." -ForegroundColor Yellow
aws s3 sync frontend/ "s3://$bucketName" --delete --region $Region

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host "  DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "  Open your dashboard in browser: $websiteUrl" -ForegroundColor Cyan
Write-Host "  Paste your API URL ($apiUrl) into the dashboard." -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Green

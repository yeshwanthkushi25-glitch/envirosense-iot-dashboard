# Workspace Guidelines & Operational Guardrails

## 1. Local Server Launch Protocol
- Never assume a port (especially 8080 or 8000) is free.
- Always verify port availability using `Get-NetTCPConnection` or socket test before launching a local server.
- After starting an HTTP server, always execute a test request to verify both `index.html` and `styles.css` return `HTTP 200 OK` before announcing the URL or launching the user's browser.

## 2. Academic & Course Project Deliverable Standards
- Never deliver PowerPoint (`.pptx`) decks or Word (`.docx`) reports containing only plain text cards.
- Always generate high-resolution PNG diagrams for:
  - System architecture and data flow
  - Hardware / circuit wiring schematics (for IoT/microcontroller projects)
  - Live UI screenshots showing normal and hazard/failure states
  - Terminal test execution showing unit tests passing
- Embed these visual diagrams directly into the PowerPoint slides, the Word report body as numbered figures, and the GitHub `README.md`.

## 3. AWS Learner Lab Compatibility
- When generating CloudFormation or AWS SAM templates for university coursework or student accounts, always include a `UseLabRole` parameter default to `'true'`.
- Bind Lambda execution roles conditionally to `!Sub 'arn:aws:iam::${AWS::AccountId}:role/LabRole'` to prevent `iam:CreateRole` sandbox permission failures.

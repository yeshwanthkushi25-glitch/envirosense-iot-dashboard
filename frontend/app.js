/**
 * EnviroSense — IoT Climate & Environmental Dashboard
 * Supports AWS HTTP API Gateway live polling and 100% offline interactive demo mode.
 */

// DOM Elements
const apiUrlInput = document.querySelector("#api-url");
const apiKeyInput = document.querySelector("#api-key");
const apiForm = document.querySelector("#api-form");
const connectionMsg = document.querySelector("#connection-message");
const envBadge = document.querySelector("#environment-badge");
const systemBadge = document.querySelector("#system-status-badge");

// Metrics DOM
const tempVal = document.querySelector("#temp-val");
const tempFahrenheit = document.querySelector("#temp-fahrenheit");
const tempMeter = document.querySelector("#temp-meter");
const humidityVal = document.querySelector("#humidity-val");
const humidityComfort = document.querySelector("#humidity-comfort");
const humidityMeter = document.querySelector("#humidity-meter");
const heatIndexVal = document.querySelector("#heat-index-val");
const heatIndexRisk = document.querySelector("#heat-index-risk");
const heatMeter = document.querySelector("#heat-meter");
const deviceIdVal = document.querySelector("#device-id-val");
const locationVal = document.querySelector("#location-val");
const lastUpdatedVal = document.querySelector("#last-updated-val");
const statusDetailText = document.querySelector("#status-detail-text");
const tableBody = document.querySelector("#telemetry-table-body");
const chartLatestTime = document.querySelector("#chart-latest-time");

// SVG Chart Elements
const svgGrid = document.querySelector("#chart-grid");
const pathTemp = document.querySelector("#path-temp");
const pathHum = document.querySelector("#path-hum");
const chartDots = document.querySelector("#chart-dots");

// State
let currentMode = "demo"; // "demo" or "api"
let pollInterval = null;
let streamInterval = null;
let isStreaming = false;

// Initial 10-point realistic baseline dataset
const initialHistory = [
  { time: "18:40:00", temp: 23.8, hum: 49.2, hi: 24.1, status: "NORMAL", device: "enviro-node-01", loc: "Campus Greenhouse Lab" },
  { time: "18:42:00", temp: 24.0, hum: 48.9, hi: 24.3, status: "NORMAL", device: "enviro-node-01", loc: "Campus Greenhouse Lab" },
  { time: "18:44:00", temp: 24.1, hum: 48.5, hi: 24.4, status: "NORMAL", device: "enviro-node-01", loc: "Campus Greenhouse Lab" },
  { time: "18:46:00", temp: 24.3, hum: 48.2, hi: 24.6, status: "NORMAL", device: "enviro-node-01", loc: "Campus Greenhouse Lab" },
  { time: "18:48:00", temp: 24.2, hum: 48.0, hi: 24.5, status: "NORMAL", device: "enviro-node-01", loc: "Campus Greenhouse Lab" },
  { time: "18:50:00", temp: 24.4, hum: 47.8, hi: 24.7, status: "NORMAL", device: "enviro-node-01", loc: "Campus Greenhouse Lab" },
  { time: "18:52:00", temp: 24.6, hum: 47.5, hi: 24.9, status: "NORMAL", device: "enviro-node-01", loc: "Campus Greenhouse Lab" },
  { time: "18:54:00", temp: 24.5, hum: 47.9, hi: 24.8, status: "NORMAL", device: "enviro-node-01", loc: "Campus Greenhouse Lab" },
  { time: "18:56:00", temp: 24.7, hum: 48.1, hi: 25.0, status: "NORMAL", device: "enviro-node-01", loc: "Campus Greenhouse Lab" },
  { time: "18:58:00", temp: 24.5, hum: 48.0, hi: 24.8, status: "NORMAL", device: "enviro-node-01", loc: "Campus Greenhouse Lab" },
];

let telemetryHistory = [...initialHistory];

// Calculations
function calculateHeatIndex(tempC, rh) {
  const tF = (tempC * 9.0 / 5.0) + 32.0;
  let hiF = 0.5 * (tF + 61.0 + ((tF - 68.0) * 1.2) + (rh * 0.094));
  if (hiF >= 80.0) {
    hiF = -42.379 + (2.04901523 * tF) + (10.14333127 * rh)
      - (0.22475541 * tF * rh) - (0.00683783 * (tF ** 2))
      - (0.05481717 * (rh ** 2)) + (0.00122874 * (tF ** 2) * rh)
      + (0.00085282 * tF * (rh ** 2)) - (0.00000199 * (tF ** 2) * (rh ** 2));
  }
  return Number(((hiF - 32.0) * 5.0 / 9.0).toFixed(1));
}

function getComfortLabel(rh) {
  if (rh < 30) return "Comfort: Dry Air";
  if (rh > 70) return "Comfort: Very Humid";
  return "Comfort: Optimal";
}

function getHeatRiskLabel(hi) {
  if (hi >= 41) return "Risk Level: Danger (Heat Exhaustion)";
  if (hi >= 35) return "Risk Level: Caution (Fatigue)";
  if (hi <= 5) return "Risk Level: Cold / Frostbite Risk";
  return "Risk Level: Safe / Normal";
}

function getStatusBadge(status) {
  if (status === "HEAT_ALERT") return '<span class="table-badge badge-danger">HEAT ALERT</span>';
  if (status === "FREEZE_ALERT") return '<span class="table-badge badge-danger">FREEZE ALERT</span>';
  if (status === "HIGH_HUMIDITY" || status === "WARNING") return '<span class="table-badge badge-warning">CAUTION</span>';
  return '<span class="table-badge badge-success">NORMAL</span>';
}

// Render Dashboard UI
function renderDashboard(latest) {
  // 1. Digital Values
  tempVal.textContent = latest.temp.toFixed(1);
  tempFahrenheit.textContent = `${((latest.temp * 9/5) + 32).toFixed(1)} °F`;
  humidityVal.textContent = latest.hum.toFixed(1);
  humidityComfort.textContent = getComfortLabel(latest.hum);
  
  const hi = latest.hi ?? calculateHeatIndex(latest.temp, latest.hum);
  heatIndexVal.textContent = hi.toFixed(1);
  heatIndexRisk.textContent = getHeatRiskLabel(hi);

  deviceIdVal.textContent = latest.device || "enviro-node-01";
  locationVal.textContent = latest.loc || "Campus Greenhouse Lab";
  lastUpdatedVal.textContent = latest.time || new Date().toLocaleTimeString();

  // 2. Meters (Scale temp -10°C to 50°C -> 0% to 100%)
  const tempPct = Math.min(100, Math.max(0, ((latest.temp - (-10)) / 60) * 100));
  tempMeter.style.width = `${tempPct}%`;
  humidityMeter.style.width = `${Math.min(100, Math.max(0, latest.hum))}%`;
  const heatPct = Math.min(100, Math.max(0, ((hi - 15) / 35) * 100));
  heatMeter.style.width = `${heatPct}%`;

  // 3. System Status Badge
  systemBadge.className = "badge";
  if (latest.status === "HEAT_ALERT" || latest.temp >= 40) {
    systemBadge.classList.add("badge-danger");
    systemBadge.textContent = "HEAT ALERT";
    statusDetailText.textContent = `High thermal hazard! Heat index reaches ${hi}°C.`;
    statusDetailText.style.borderLeftColor = "var(--accent-rose)";
  } else if (latest.status === "FREEZE_ALERT" || latest.temp <= 5) {
    systemBadge.classList.add("badge-danger");
    systemBadge.textContent = "FREEZE ALERT";
    statusDetailText.textContent = `Low temperature alert: ${latest.temp}°C. Freeze protection needed.`;
    statusDetailText.style.borderLeftColor = "var(--accent-rose)";
  } else if (latest.hum >= 85 || latest.status === "HIGH_HUMIDITY") {
    systemBadge.classList.add("badge-warning");
    systemBadge.textContent = "HIGH HUMIDITY";
    statusDetailText.textContent = `High humidity (${latest.hum}%) may promote mildew/condensation.`;
    statusDetailText.style.borderLeftColor = "var(--accent-amber)";
  } else {
    systemBadge.classList.add("badge-success");
    systemBadge.textContent = "NORMAL";
    statusDetailText.textContent = "All environmental metrics are within safe operational thresholds.";
    statusDetailText.style.borderLeftColor = "var(--accent-emerald)";
  }

  // 4. Render Table
  renderTable();

  // 5. Render SVG Chart
  renderChart();
}

function renderTable() {
  const reversed = [...telemetryHistory].reverse().slice(0, 10);
  tableBody.innerHTML = reversed.map(row => `
    <tr>
      <td>${row.time}</td>
      <td><code>${row.device || "enviro-node-01"}</code></td>
      <td>${row.loc || "Campus Lab"}</td>
      <td style="font-weight:600; color:var(--accent-cyan);">${row.temp.toFixed(1)} °C</td>
      <td style="font-weight:600; color:var(--accent-blue);">${row.hum.toFixed(1)} %</td>
      <td>${row.hi ? row.hi.toFixed(1) + " °C" : "—"}</td>
      <td>${getStatusBadge(row.status)}</td>
    </tr>
  `).join("");
}

function renderChart() {
  const w = 800;
  const h = 240;
  const padX = 40;
  const padY = 20;
  const chartW = w - (padX * 2);
  const chartH = h - (padY * 2);

  const n = telemetryHistory.length;
  if (n < 2) return;

  // Grid
  let gridHtml = "";
  for (let i = 0; i <= 4; i++) {
    const y = padY + (chartH / 4) * i;
    gridHtml += `<line class="chart-grid-line" x1="${padX}" y1="${y}" x2="${w - padX}" y2="${y}" />`;
  }
  svgGrid.innerHTML = gridHtml;

  // Scales
  // Temperature: 0°C to 50°C
  const minT = 0, maxT = 50;
  // Humidity: 0% to 100%
  const minH = 0, maxH = 100;

  const pointsT = [];
  const pointsH = [];

  telemetryHistory.forEach((pt, idx) => {
    const x = padX + (idx / (n - 1)) * chartW;
    const yT = padY + chartH - ((Math.min(maxT, Math.max(minT, pt.temp)) - minT) / (maxT - minT)) * chartH;
    const yH = padY + chartH - ((Math.min(maxH, Math.max(minH, pt.hum)) - minH) / (maxH - minH)) * chartH;
    pointsT.push({ x, y: yT });
    pointsH.push({ x, y: yH });
  });

  const pathStringT = pointsT.map((p, i) => `${i === 0 ? "M" : "L"} ${p.x.toFixed(1)} ${p.y.toFixed(1)}`).join(" ");
  const pathStringH = pointsH.map((p, i) => `${i === 0 ? "M" : "L"} ${p.x.toFixed(1)} ${p.y.toFixed(1)}`).join(" ");

  pathTemp.setAttribute("d", pathStringT);
  pathHum.setAttribute("d", pathStringH);

  // Dots
  const dotsHtml = pointsT.map((pt, i) => `
    <circle cx="${pt.x.toFixed(1)}" cy="${pt.y.toFixed(1)}" r="4" fill="var(--accent-cyan)" />
    <circle cx="${pointsH[i].x.toFixed(1)}" cy="${pointsH[i].y.toFixed(1)}" r="4" fill="var(--accent-blue)" />
  `).join("");
  chartDots.innerHTML = dotsHtml;

  chartLatestTime.textContent = `Last reading: ${telemetryHistory[telemetryHistory.length - 1].time}`;
}

// Ingestion of a new telemetry item
function pushTelemetry(item) {
  telemetryHistory.push(item);
  if (telemetryHistory.length > 20) {
    telemetryHistory.shift();
  }
  renderDashboard(item);
}

// Presets
function applyPreset(temp, hum, status, note) {
  const now = new Date();
  const timeStr = now.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
  const hi = calculateHeatIndex(temp, hum);
  const item = {
    time: timeStr,
    temp: Number(temp.toFixed(1)),
    hum: Number(hum.toFixed(1)),
    hi: hi,
    status: status,
    device: "enviro-node-01",
    loc: "Campus Greenhouse Lab"
  };
  pushTelemetry(item);
  connectionMsg.textContent = `Simulation preset applied: ${note}`;
  connectionMsg.className = "status-msg";
}

document.querySelector("#sim-normal").addEventListener("click", () => {
  applyPreset(24.5, 48.0, "NORMAL", "Optimal room conditions (24.5°C, 48%)");
});

document.querySelector("#sim-heat").addEventListener("click", () => {
  applyPreset(41.8, 82.0, "HEAT_ALERT", "Critical Heatwave event! (>41°C, 82% humidity)");
});

document.querySelector("#sim-freeze").addEventListener("click", () => {
  applyPreset(2.4, 34.0, "FREEZE_ALERT", "Cold wave / frost risk (2.4°C, 34%)");
});

document.querySelector("#sim-humid").addEventListener("click", () => {
  applyPreset(29.2, 92.0, "HIGH_HUMIDITY", "Heavy precipitation / high moisture (29.2°C, 92%)");
});

// Live Continuous Simulation Stream
const streamBtn = document.querySelector("#sim-stream");
streamBtn.addEventListener("click", () => {
  if (isStreaming) {
    clearInterval(streamInterval);
    isStreaming = false;
    streamBtn.textContent = "▶️ Start Live Stream";
    streamBtn.classList.remove("active");
    connectionMsg.textContent = "Live simulation stream paused.";
  } else {
    isStreaming = true;
    streamBtn.textContent = "⏹️ Stop Live Stream";
    streamBtn.classList.add("active");
    connectionMsg.textContent = "Live simulation active: streaming simulated telemetry every 3 seconds.";

    streamInterval = setInterval(() => {
      const last = telemetryHistory[telemetryHistory.length - 1];
      // Random walk with mean reversion towards 25°C and 50%
      const deltaT = (Math.random() - 0.48) * 0.8 + (25.0 - last.temp) * 0.05;
      const deltaH = (Math.random() - 0.48) * 1.5 + (50.0 - last.hum) * 0.05;

      const newT = Number((last.temp + deltaT).toFixed(1));
      const newH = Number((last.hum + deltaH).toFixed(1));
      const hi = calculateHeatIndex(newT, newH);

      let status = "NORMAL";
      if (newT >= 40 || hi >= 40) status = "HEAT_ALERT";
      else if (newT <= 5) status = "FREEZE_ALERT";
      else if (newH >= 85) status = "HIGH_HUMIDITY";

      const timeStr = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
      pushTelemetry({
        time: timeStr,
        temp: newT,
        hum: newH,
        hi: hi,
        status: status,
        device: "enviro-node-01",
        loc: "Campus Greenhouse Lab"
      });
    }, 3000);
  }
});

// Live AWS API Gateway Polling
async function fetchFromApi() {
  const url = apiUrlInput.value.trim().replace(/\/$/, "");
  if (!url) {
    setDemoMode();
    return;
  }

  try {
    const headers = {};
    const key = apiKeyInput.value.trim();
    if (key) headers["x-api-key"] = key;

    const res = await fetch(`${url}/telemetry`, { headers });
    if (!res.ok) throw new Error(`API returned HTTP ${res.status}`);
    const data = await res.json();

    envBadge.className = "badge badge-aws";
    envBadge.textContent = "AWS CONNECTED";
    connectionMsg.textContent = "Connected to AWS API Gateway. Streaming live DynamoDB records every 6 seconds.";
    connectionMsg.className = "status-msg success";

    if (data.latest) {
      const timeStr = data.latest.recordedAt 
        ? new Date(data.latest.recordedAt).toLocaleTimeString() 
        : new Date().toLocaleTimeString();

      pushTelemetry({
        time: timeStr,
        temp: data.latest.temperatureC,
        hum: data.latest.humidityPct,
        hi: data.latest.heatIndexC,
        status: data.latest.status,
        device: data.latest.deviceId,
        loc: data.latest.location
      });
    }
  } catch (err) {
    envBadge.className = "badge badge-demo";
    envBadge.textContent = "DEMO MODE";
    connectionMsg.textContent = `Could not reach API: ${err.message}. Showing local state.`;
    connectionMsg.className = "status-msg error";
  }
}

function setDemoMode() {
  currentMode = "demo";
  envBadge.className = "badge badge-demo";
  envBadge.textContent = "DEMO MODE";
  connectionMsg.textContent = "Showing local demonstration state. No AWS connection required.";
  connectionMsg.className = "status-msg";
  if (pollInterval) clearInterval(pollInterval);
}

// Form Handlers
apiForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const url = apiUrlInput.value.trim();
  const key = apiKeyInput.value.trim();
  localStorage.setItem("envirosense-api-url", url);
  localStorage.setItem("envirosense-api-key", key);

  if (pollInterval) clearInterval(pollInterval);
  fetchFromApi();
  pollInterval = setInterval(fetchFromApi, 6000);
});

document.querySelector("#btn-reset-demo").addEventListener("click", () => {
  apiUrlInput.value = "";
  apiKeyInput.value = "";
  localStorage.removeItem("envirosense-api-url");
  localStorage.removeItem("envirosense-api-key");
  setDemoMode();
});

// Initialization
apiUrlInput.value = localStorage.getItem("envirosense-api-url") || "";
apiKeyInput.value = localStorage.getItem("envirosense-api-key") || "";

renderDashboard(telemetryHistory[telemetryHistory.length - 1]);

if (apiUrlInput.value) {
  fetchFromApi();
  pollInterval = setInterval(fetchFromApi, 6000);
}

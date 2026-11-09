/**
 * EnviroSense — IoT Climate & Environmental Dashboard
 * Redesigned with Circular SVG Radial Gauges, Gradient Area Charts & Web Audio Alerts
 */

// DOM Elements
const apiUrlInput = document.querySelector("#api-url");
const apiKeyInput = document.querySelector("#api-key");
const apiForm = document.querySelector("#api-form");
const connectionMsg = document.querySelector("#connection-message");
const envBadge = document.querySelector("#environment-badge");
const systemBadge = document.querySelector("#system-status-badge");
const badgeStatusText = document.querySelector("#badge-status-text");
const activeEndpointDisplay = document.querySelector("#active-endpoint-display");
const soundToggleBtn = document.querySelector("#btn-sound-toggle");
const soundIcon = document.querySelector("#sound-icon");

// Metrics & Dials
const tempVal = document.querySelector("#temp-val");
const tempFahrenheit = document.querySelector("#temp-fahrenheit");
const tempDialArc = document.querySelector("#temp-dial-arc");

const humidityVal = document.querySelector("#humidity-val");
const humidityComfort = document.querySelector("#humidity-comfort");
const humidityDialArc = document.querySelector("#humidity-dial-arc");

const heatIndexVal = document.querySelector("#heat-index-val");
const heatIndexRisk = document.querySelector("#heat-index-risk");
const heatDialArc = document.querySelector("#heat-dial-arc");

const deviceIdVal = document.querySelector("#device-id-val");
const locationVal = document.querySelector("#location-val");
const lastUpdatedVal = document.querySelector("#last-updated-val");
const statusDetailBox = document.querySelector("#status-detail-box");
const facilityStateIcon = document.querySelector("#facility-state-icon");
const facilityStateTitle = document.querySelector("#facility-state-title");
const statusDetailText = document.querySelector("#status-detail-text");
const tableBody = document.querySelector("#telemetry-table-body");
const logCountBadge = document.querySelector("#log-count-badge");
const chartLatestTime = document.querySelector("#chart-latest-time");

// SVG Chart Elements
const svgGrid = document.querySelector("#chart-grid");
const pathTemp = document.querySelector("#path-temp");
const pathHum = document.querySelector("#path-hum");
const areaTemp = document.querySelector("#area-temp");
const areaHum = document.querySelector("#area-hum");
const chartDots = document.querySelector("#chart-dots");

// Circumference of radius 62 circle: 2 * PI * 62 = ~389.55
const CIRCUMFERENCE = 389.55;

// Audio Synthesizer State
let audioEnabled = true;
let audioCtx = null;

function playTone(freq, type = "sine", duration = 0.15) {
  if (!audioEnabled) return;
  try {
    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    if (audioCtx.state === "suspended") audioCtx.resume();
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = type;
    osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
    gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start();
    osc.stop(audioCtx.currentTime + duration);
  } catch (e) {
    // Audio context policy
  }
}

function playChimeNormal() {
  playTone(523.25, "sine", 0.12); // C5
  setTimeout(() => playTone(659.25, "sine", 0.2), 100); // E5
}

function playHazardAlert() {
  playTone(880, "sawtooth", 0.25); // A5 alert
  setTimeout(() => playTone(880, "sawtooth", 0.3), 300);
}

soundToggleBtn.addEventListener("click", () => {
  audioEnabled = !audioEnabled;
  soundIcon.textContent = audioEnabled ? "🔔 Audio: ON" : "🔕 Audio: OFF";
  if (audioEnabled) playTone(440, "sine", 0.1);
});

// State
let pollInterval = null;
let streamInterval = null;
let isStreaming = false;

// 10-point initial dataset
const initialHistory = [
  { time: "21:40:00", temp: 23.9, hum: 49.0, hi: 24.1, status: "NORMAL", device: "enviro-node-01", loc: "Campus Greenhouse Lab" },
  { time: "21:42:00", temp: 24.1, hum: 48.7, hi: 24.3, status: "NORMAL", device: "enviro-node-01", loc: "Campus Greenhouse Lab" },
  { time: "21:44:00", temp: 24.0, hum: 48.5, hi: 24.2, status: "NORMAL", device: "enviro-node-01", loc: "Campus Greenhouse Lab" },
  { time: "21:46:00", temp: 24.3, hum: 48.2, hi: 24.5, status: "NORMAL", device: "enviro-node-01", loc: "Campus Greenhouse Lab" },
  { time: "21:48:00", temp: 24.2, hum: 48.0, hi: 24.4, status: "NORMAL", device: "enviro-node-01", loc: "Campus Greenhouse Lab" },
  { time: "21:50:00", temp: 24.4, hum: 47.8, hi: 24.6, status: "NORMAL", device: "enviro-node-01", loc: "Campus Greenhouse Lab" },
  { time: "21:52:00", temp: 24.6, hum: 47.6, hi: 24.8, status: "NORMAL", device: "enviro-node-01", loc: "Campus Greenhouse Lab" },
  { time: "21:54:00", temp: 24.5, hum: 47.9, hi: 24.7, status: "NORMAL", device: "enviro-node-01", loc: "Campus Greenhouse Lab" },
  { time: "21:56:00", temp: 24.7, hum: 48.1, hi: 24.9, status: "NORMAL", device: "enviro-node-01", loc: "Campus Greenhouse Lab" },
  { time: "21:58:00", temp: 24.5, hum: 48.0, hi: 24.8, status: "NORMAL", device: "enviro-node-01", loc: "Campus Greenhouse Lab" },
];

let telemetryHistory = [...initialHistory];

// Steadman Heat Index Calculation
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
  if (rh < 30) return "Comfort: Dry Air (<30%)";
  if (rh > 75) return "Comfort: High Humidity (>75%)";
  return "Comfort: Optimal (40-60%)";
}

function getHeatRiskLabel(hi) {
  if (hi >= 41) return "Risk: Critical Heat Danger";
  if (hi >= 35) return "Risk: Caution (Heat Fatigue)";
  if (hi <= 5) return "Risk: Freezing Hazard";
  return "Risk: Safe / Low Stress";
}

function getTableBadge(status) {
  if (status === "HEAT_ALERT") return '<span class="badge-tag tag-heat">🔥 HEAT ALERT</span>';
  if (status === "FREEZE_ALERT") return '<span class="badge-tag tag-freeze">❄️ FREEZE ALERT</span>';
  if (status === "HIGH_HUMIDITY" || status === "WARNING") return '<span class="badge-tag tag-humid">💧 HIGH MOISTURE</span>';
  return '<span class="badge-tag tag-normal">🟢 NORMAL</span>';
}

// Render Complete UI
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

  // 2. Circular Radial Dials (0% to 100% mapped to circumference)
  // Temp scale: 0°C to 50°C
  const tempPct = Math.min(1, Math.max(0, latest.temp / 50.0));
  tempDialArc.style.strokeDashoffset = CIRCUMFERENCE * (1 - tempPct);

  // Humidity scale: 0% to 100%
  const humPct = Math.min(1, Math.max(0, latest.hum / 100.0));
  humidityDialArc.style.strokeDashoffset = CIRCUMFERENCE * (1 - humPct);

  // Heat Index scale: 0°C to 50°C
  const heatPct = Math.min(1, Math.max(0, hi / 50.0));
  heatDialArc.style.strokeDashoffset = CIRCUMFERENCE * (1 - heatPct);

  // 3. System Status Evaluation & Audio Tone
  systemBadge.className = "badge";
  if (latest.status === "HEAT_ALERT" || latest.temp >= 40 || hi >= 40) {
    systemBadge.classList.add("badge-danger");
    badgeStatusText.textContent = "HEAT ALERT";
    facilityStateIcon.textContent = "🔥";
    facilityStateTitle.textContent = "Critical Heat Hazard Active";
    facilityStateTitle.style.color = "var(--accent-coral)";
    statusDetailText.textContent = `Extreme thermal hazard: ${latest.temp}°C ambient, Heat Index reaches ${hi}°C. Immediate cooling needed.`;
    statusDetailBox.style.borderColor = "var(--accent-coral)";
    statusDetailBox.style.background = "rgba(244, 63, 94, 0.12)";
    playHazardAlert();
  } else if (latest.status === "FREEZE_ALERT" || latest.temp <= 5) {
    systemBadge.classList.add("badge-danger");
    badgeStatusText.textContent = "FREEZE ALERT";
    facilityStateIcon.textContent = "❄️";
    facilityStateTitle.textContent = "Freezing Condition Detected";
    facilityStateTitle.style.color = "#38bdf8";
    statusDetailText.textContent = `Frost risk: Temperature at ${latest.temp}°C. Heating protection activated.`;
    statusDetailBox.style.borderColor = "#38bdf8";
    statusDetailBox.style.background = "rgba(56, 189, 248, 0.12)";
    playHazardAlert();
  } else if (latest.hum >= 85 || latest.status === "HIGH_HUMIDITY") {
    systemBadge.classList.add("badge-warning");
    badgeStatusText.textContent = "HIGH MOISTURE";
    facilityStateIcon.textContent = "💧";
    facilityStateTitle.textContent = "Condensation Hazard Warning";
    facilityStateTitle.style.color = "var(--accent-amber)";
    statusDetailText.textContent = `High moisture level (${latest.hum}%). Mildew and condensation risks present.`;
    statusDetailBox.style.borderColor = "var(--accent-amber)";
    statusDetailBox.style.background = "rgba(245, 158, 11, 0.12)";
  } else {
    systemBadge.classList.add("badge-normal");
    badgeStatusText.textContent = "NORMAL";
    facilityStateIcon.textContent = "🌿";
    facilityStateTitle.textContent = "Climate Equilibrium Normal";
    facilityStateTitle.style.color = "#34d399";
    statusDetailText.textContent = "All parameters are balanced within safe biological and hardware limits.";
    statusDetailBox.style.borderColor = "rgba(16, 185, 129, 0.3)";
    statusDetailBox.style.background = "rgba(16, 185, 129, 0.08)";
  }

  // 4. Render Table & Charts
  renderTable();
  renderChart();
}

function renderTable() {
  const reversed = [...telemetryHistory].reverse().slice(0, 10);
  logCountBadge.textContent = `${telemetryHistory.length} Records in Cache`;
  tableBody.innerHTML = reversed.map(row => `
    <tr>
      <td><code>${row.time}</code></td>
      <td><strong>${row.device || "enviro-node-01"}</strong></td>
      <td>${row.loc || "Campus Greenhouse Lab"}</td>
      <td style="font-weight:700; color:var(--accent-cyan); font-size:0.875rem;">${row.temp.toFixed(1)} °C</td>
      <td style="font-weight:700; color:var(--accent-blue); font-size:0.875rem;">${row.hum.toFixed(1)} %</td>
      <td>${row.hi ? row.hi.toFixed(1) + " °C" : "—"}</td>
      <td>${getTableBadge(row.status)}</td>
    </tr>
  `).join("");
}

function renderChart() {
  const w = 900;
  const h = 260;
  const padX = 45;
  const padY = 25;
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
  const minT = 0, maxT = 50;
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

  // Closed area paths for translucent gradient fills below curves
  const baselineY = padY + chartH;
  const areaStringT = `${pathStringT} L ${pointsT[pointsT.length - 1].x.toFixed(1)} ${baselineY} L ${pointsT[0].x.toFixed(1)} ${baselineY} Z`;
  const areaStringH = `${pathStringH} L ${pointsH[pointsH.length - 1].x.toFixed(1)} ${baselineY} L ${pointsH[0].x.toFixed(1)} ${baselineY} Z`;

  pathTemp.setAttribute("d", pathStringT);
  pathHum.setAttribute("d", pathStringH);
  areaTemp.setAttribute("d", areaStringT);
  areaHum.setAttribute("d", areaStringH);

  // Glowing Vector Dots
  const dotsHtml = pointsT.map((pt, i) => `
    <circle cx="${pt.x.toFixed(1)}" cy="${pt.y.toFixed(1)}" r="4.5" fill="var(--accent-cyan)" />
    <circle cx="${pointsH[i].x.toFixed(1)}" cy="${pointsH[i].y.toFixed(1)}" r="4" fill="var(--accent-blue)" />
  `).join("");
  chartDots.innerHTML = dotsHtml;

  chartLatestTime.textContent = `Last reading recorded: ${telemetryHistory[telemetryHistory.length - 1].time}`;
}

function pushTelemetry(item) {
  telemetryHistory.push(item);
  if (telemetryHistory.length > 20) {
    telemetryHistory.shift();
  }
  renderDashboard(item);
}

// Scenario Buttons Logic
function setScenarioActive(btnId) {
  document.querySelectorAll(".scenario-card").forEach(c => c.classList.remove("active"));
  const btn = document.querySelector(btnId);
  if (btn) btn.classList.add("active");
}

function applyPreset(temp, hum, status, note, btnId) {
  setScenarioActive(btnId);
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
  connectionMsg.textContent = `Applied scenario preset: ${note}`;
  connectionMsg.className = "status-msg";
}

document.querySelector("#sim-normal").addEventListener("click", () => {
  applyPreset(24.5, 48.0, "NORMAL", "Optimal Greenhouse condition (24.5°C, 48%)", "#sim-normal");
  playChimeNormal();
});

document.querySelector("#sim-heat").addEventListener("click", () => {
  applyPreset(41.8, 84.0, "HEAT_ALERT", "Critical Heatwave event! (>41°C, 84% humidity)", "#sim-heat");
});

document.querySelector("#sim-freeze").addEventListener("click", () => {
  applyPreset(2.4, 32.0, "FREEZE_ALERT", "Cold wave / frost hazard (2.4°C, 32%)", "#sim-freeze");
});

document.querySelector("#sim-humid").addEventListener("click", () => {
  applyPreset(29.2, 92.0, "HIGH_HUMIDITY", "Tropical storm / high moisture (29.2°C, 92%)", "#sim-humid");
});

// Live Continuous Simulation Stream
const streamBtn = document.querySelector("#sim-stream");
const streamIcon = document.querySelector("#stream-icon");
const streamLabel = document.querySelector("#stream-label");
const streamSub = document.querySelector("#stream-sub");

streamBtn.addEventListener("click", () => {
  if (isStreaming) {
    clearInterval(streamInterval);
    isStreaming = false;
    streamIcon.textContent = "▶️";
    streamLabel.textContent = "Auto Live Stream";
    streamSub.textContent = "Ticks every 3s";
    streamBtn.classList.remove("active");
    connectionMsg.textContent = "Simulation stream paused.";
  } else {
    isStreaming = true;
    setScenarioActive("#sim-stream");
    streamIcon.textContent = "⏹️";
    streamLabel.textContent = "Stop Stream";
    streamSub.textContent = "Active (streaming)";
    streamBtn.classList.add("active");
    connectionMsg.textContent = "Streaming live simulated telemetry every 3 seconds.";

    streamInterval = setInterval(() => {
      const last = telemetryHistory[telemetryHistory.length - 1];
      const deltaT = (Math.random() - 0.48) * 0.9 + (25.0 - last.temp) * 0.05;
      const deltaH = (Math.random() - 0.48) * 1.6 + (50.0 - last.hum) * 0.05;

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

// Live AWS API Polling
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
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    envBadge.className = "badge badge-aws";
    envBadge.textContent = "AWS CONNECTED";
    activeEndpointDisplay.textContent = url;
    connectionMsg.textContent = "Connected to AWS API Gateway. Polling DynamoDB records in real time.";
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
  envBadge.className = "badge badge-demo";
  envBadge.textContent = "DEMO MODE";
  activeEndpointDisplay.textContent = "Local Rig (Demo Engine)";
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

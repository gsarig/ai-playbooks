import fs from 'fs';
import path from 'path';

const REGISTRY_FILE   = '_registry.json';
const ATTACHMENTS_DIR = '_attachments';
const HISTORY_DIR     = '_history';
const DASHBOARD_FILE  = 'Dashboard.md';

const MONTHS = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December',
];

function formatDate(isoDate) {
  const [year, month, day] = isoDate.split('-').map(Number);
  return `${MONTHS[month - 1]} ${day}, ${year}`;
}

// ---------------------------------------------------------------------------
// Registry
// ---------------------------------------------------------------------------

export function loadRegistry(vaultPath) {
  const p = path.join(vaultPath, REGISTRY_FILE);
  if (!fs.existsSync(p)) return {};
  return JSON.parse(fs.readFileSync(p, 'utf8'));
}

export function saveRegistry(vaultPath, registry) {
  fs.writeFileSync(
    path.join(vaultPath, REGISTRY_FILE),
    JSON.stringify(registry, null, 2)
  );
}

// ---------------------------------------------------------------------------
// Rescan queue  (stored as _rescanQueue inside _registry.json)
// ---------------------------------------------------------------------------

export function getRescanQueue(vaultPath) {
  const registry = loadRegistry(vaultPath);
  return registry._rescanQueue ?? [];
}

export function addToRescanQueue(vaultPath, plantId, photos, reason) {
  const registry = loadRegistry(vaultPath);
  const queue = registry._rescanQueue ?? [];
  queue.push({ plantId, photos, reason, addedAt: new Date().toISOString().slice(0, 10) });
  registry._rescanQueue = queue;
  saveRegistry(vaultPath, registry);
}

export function clearRescanQueue(vaultPath) {
  const registry = loadRegistry(vaultPath);
  delete registry._rescanQueue;
  saveRegistry(vaultPath, registry);
}

// ---------------------------------------------------------------------------
// History  (_history/<plantId>.json)
// Each entry: { date, healthStatus, healthScore, urgency, problems, photos, summary }
// ---------------------------------------------------------------------------

export function loadHistory(vaultPath, plantId) {
  const p = path.join(vaultPath, HISTORY_DIR, `${plantId}.json`);
  if (!fs.existsSync(p)) return [];
  return JSON.parse(fs.readFileSync(p, 'utf8'));
}

export function appendHistory(vaultPath, plantId, entry) {
  const histDir = path.join(vaultPath, HISTORY_DIR);
  fs.mkdirSync(histDir, { recursive: true });
  const p = path.join(histDir, `${plantId}.json`);
  const history = fs.existsSync(p) ? JSON.parse(fs.readFileSync(p, 'utf8')) : [];
  history.push(entry);
  fs.writeFileSync(p, JSON.stringify(history, null, 2));
}

// ---------------------------------------------------------------------------
// Plant ID generation
// ---------------------------------------------------------------------------

export function createPlantId(species, registry) {
  const base = species
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '');

  let n = 1;
  while (registry[`${base}-${String(n).padStart(2, '0')}`]) n++;
  return `${base}-${String(n).padStart(2, '0')}`;
}

// ---------------------------------------------------------------------------
// Photo handling
// ---------------------------------------------------------------------------

export function movePhotoToVault(sourcePath, vaultPath) {
  const attachmentsDir = path.join(vaultPath, ATTACHMENTS_DIR);
  fs.mkdirSync(attachmentsDir, { recursive: true });

  const stats = fs.statSync(sourcePath);
  const date = stats.birthtime > new Date(0) ? stats.birthtime : stats.mtime;
  const ts = date.toISOString().replace(/[-:T]/g, '').slice(0, 14);
  const ext = path.extname(sourcePath).toLowerCase() || '.jpg';
  const filename = `plants-${ts}${ext}`;
  const destPath = path.join(attachmentsDir, filename);

  let finalPath = destPath;
  let finalFilename = filename;
  if (fs.existsSync(destPath)) {
    const base = `plants-${ts}-${Date.now()}`;
    finalFilename = `${base}${ext}`;
    finalPath = path.join(attachmentsDir, finalFilename);
  }

  fs.renameSync(sourcePath, finalPath);
  return { filename: finalFilename, relativePath: `${ATTACHMENTS_DIR}/${finalFilename}` };
}

// ---------------------------------------------------------------------------
// Plant report
// ---------------------------------------------------------------------------

/**
 * @param {string}   vaultPath
 * @param {string}   plantId
 * @param {object}   plant          - registry entry for this plant
 * @param {object}   analysis       - Claude analysis result for this plant
 * @param {string[]} photoFilenames - vault filenames of all session photos showing this plant
 * @param {string}   scanDate       - ISO date string (YYYY-MM-DD)
 */
export function updatePlantReport(vaultPath, plantId, plant, analysis, photoFilenames, scanDate) {
  const plantDir = path.join(vaultPath, plantId);
  fs.mkdirSync(plantDir, { recursive: true });

  const reportPath = path.join(plantDir, 'report.md');
  const formattedDate = formatDate(scanDate);

  // Flags for detected changes
  const changeFlags = [];
  if (analysis.locationChange)  changeFlags.push('Location change detected');
  if (analysis.vesselChange)    changeFlags.push('Pot/vessel change detected');
  if (analysis.uncertaintyNote) changeFlags.push(`Uncertainty: ${analysis.uncertaintyNote}`);

  // Care callout — only when action is needed
  const careBlock = analysis.urgency !== 'None'
    ? `\n> [!${urgencyCallout(analysis.urgency)}] Care\n> ${analysis.care}\n`
    : `\n**Care:** ${analysis.care}\n`;

  const photoEmbeds = photoFilenames.map(f => `![[${f}]]`).join('\n');
  const photoLabel  = photoFilenames.length > 1
    ? `_${photoFilenames.length} photos from this session_\n`
    : '';

  const entry = [
    `### ${formattedDate}`,
    '',
    photoLabel + photoEmbeds,
    '',
    `**Health:** ${analysis.healthStatus}`,
    `**${analysis.summary}**`,
    careBlock,
    changeFlags.length > 0 ? changeFlags.map(f => `> [!warning] ${f}`).join('\n') + '\n' : null,
    '---',
  ].filter(l => l !== null).join('\n');

  if (fs.existsSync(reportPath)) {
    const existing = fs.readFileSync(reportPath, 'utf8');
    const marker   = '## History';
    const idx      = existing.indexOf(marker);
    if (idx !== -1) {
      const before = existing.slice(0, idx + marker.length);
      const after  = existing.slice(idx + marker.length);
      fs.writeFileSync(reportPath, `${before}\n\n${entry}${after}`);
    } else {
      fs.writeFileSync(reportPath, `${existing}\n\n${entry}`);
    }

    updateFrontmatter(reportPath, {
      last_seen:     scanDate,
      health_status: analysis.healthStatus,
      urgency:       analysis.urgency,
      location:      analysis.locationChange ? 'UNKNOWN — please update' : (plant.location ?? 'Unknown'),
      vessel:        analysis.vesselChange   ? 'UNKNOWN — please update' : (plant.vessel   ?? 'Unknown'),
    });
  } else {
    fs.writeFileSync(reportPath, buildFirstReport(plantId, plant, analysis, scanDate, formattedDate, entry));
  }
}

function buildFirstReport(plantId, plant, analysis, scanDate, formattedDate, timelineEntry) {
  const chartBlock = buildChartBlock(plantId);

  return `---
title: "${plant.commonName}"
species: "${plant.species}"
plant_id: "${plantId}"
first_seen: ${scanDate}
last_seen: ${scanDate}
health_status: ${analysis.healthStatus}
urgency: ${analysis.urgency}
location: "${plant.location ?? 'Unknown'}"
vessel: "${plant.vessel ?? 'Unknown'}"
last_watered: ${plant.lastWatered ?? ''}
watering_interval_days: ${plant.wateringIntervalDays ?? ''}
tags:
  - plant
  - ${plantId}
---

# ${plant.commonName}

*${plant.species}*

| Field | Value |
|---|---|
| First recorded | ${formattedDate} |
| Last recorded | ${formattedDate} |
| Health | ${analysis.healthStatus} |
| Location | ${plant.location ?? 'Unknown'} |
| Vessel | ${plant.vessel ?? 'Unknown'} |

## Health History

${chartBlock}

## History

${timelineEntry}
`;
}

function buildChartBlock(plantId) {
  // DataviewJS reads _history/<plantId>.json and renders a health trend chart
  // via the Obsidian Charts plugin (window.renderChart)
  return `\`\`\`dataviewjs
const plantId = dv.current().plant_id;
const histPath = \`_history/\${plantId}.json\`;
try {
  const raw = await app.vault.adapter.read(histPath);
  const history = JSON.parse(raw);
  if (history.length === 0) { dv.paragraph("_No data yet._"); return; }
  const labels = history.map(h => h.date);
  const scores = history.map(h => h.healthScore);
  window.renderChart({
    type: "line",
    data: {
      labels,
      datasets: [{
        label: "Health (1-5)",
        data: scores,
        backgroundColor: "rgba(75, 192, 100, 0.15)",
        borderColor: "rgba(75, 192, 100, 1)",
        borderWidth: 2,
        fill: true,
        tension: 0.3,
        pointRadius: 4,
      }]
    },
    options: {
      scales: { y: { min: 1, max: 5, ticks: { stepSize: 1 } } },
      plugins: { legend: { display: false } }
    }
  }, this.container);
} catch(e) {
  dv.paragraph("_No history data yet._");
}
\`\`\``;
}

function updateFrontmatter(reportPath, fields) {
  let content = fs.readFileSync(reportPath, 'utf8');
  for (const [key, value] of Object.entries(fields)) {
    const regex = new RegExp(`^(${key}:)(.*)$`, 'm');
    if (regex.test(content)) {
      content = content.replace(regex, `$1 ${value}`);
    } else {
      const closingFm = content.indexOf('\n---', content.indexOf('---') + 3);
      if (closingFm !== -1) {
        content = content.slice(0, closingFm) + `\n${key}: ${value}` + content.slice(closingFm);
      }
    }
  }
  fs.writeFileSync(reportPath, content);
}

function urgencyCallout(urgency) {
  switch (urgency) {
    case 'Urgent':   return 'danger';
    case 'Act Soon': return 'warning';
    case 'Watch':    return 'note';
    default:         return 'tip';
  }
}

// ---------------------------------------------------------------------------
// Dashboard
// ---------------------------------------------------------------------------

export function updateDashboard(vaultPath, registry, pendingWarnings) {
  const plants = Object.entries(registry).filter(([k]) => !k.startsWith('_'));
  const scanDate = new Date().toLocaleDateString('en-GB', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric',
  });

  const totalPlants   = plants.length;
  const totalPhotos   = plants.reduce((sum, [, p]) => sum + (p.photoCount ?? 0), 0);
  const needsAttention = plants.filter(([, p]) =>
    ['Fair', 'Poor', 'Critical'].includes(p.healthStatus)
  );

  const warningsBlock = pendingWarnings.length > 0
    ? [
        '> [!warning] Your attention is needed',
        '> The following items need clarification:',
        ...pendingWarnings.map(w => `> - ${w}`),
        '',
      ].join('\n')
    : '> [!success] All good\n> Nothing needs your attention right now.\n';

  const allPlantsQuery = `\`\`\`dataview
TABLE species AS "Species", health_status AS "Health", last_seen AS "Last recorded", location AS "Location"
FROM ""
WHERE contains(tags, "plant")
SORT last_seen DESC
\`\`\``;

  const attentionQuery = `\`\`\`dataview
TABLE species AS "Species", health_status AS "Health", urgency AS "Urgency", last_seen AS "Last recorded"
FROM ""
WHERE contains(tags, "plant") AND contains(list("Fair","Poor","Critical"), health_status)
SORT last_seen DESC
\`\`\``;

  const wateringQuery = `\`\`\`dataview
TABLE last_watered AS "Last watered", watering_interval_days AS "Interval (days)",
  (date(today) - date(last_watered)).days AS "Days since"
FROM ""
WHERE contains(tags, "plant")
SORT (date(today) - date(last_watered)).days DESC
\`\`\``;

  const content = `---
title: "Plant Dashboard"
tags:
  - dashboard
---

# Plant Dashboard

*Last updated: ${scanDate}*

${warningsBlock}

## Collection Summary

| | |
|---|---|
| Total plants | ${totalPlants} |
| Total photos | ${totalPhotos} |
| Need attention | ${needsAttention.length} |
| Last scan | ${scanDate} |

## All Plants

${allPlantsQuery}

## Need Attention

${needsAttention.length > 0 ? attentionQuery : '*All plants are in good condition.*'}

## Watering

${wateringQuery}

## Recent Activity

\`\`\`dataview
TABLE file.mtime AS "Updated", health_status AS "Health"
FROM ""
WHERE contains(tags, "plant")
SORT file.mtime DESC
LIMIT 5
\`\`\`
`;

  fs.writeFileSync(path.join(vaultPath, DASHBOARD_FILE), content);
}

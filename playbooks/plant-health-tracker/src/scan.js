import fs from 'fs';
import path from 'path';
import readline from 'readline';
import { analyzePhotos, MODELS } from './analyze.js';
import {
  loadRegistry,
  saveRegistry,
  createPlantId,
  movePhotoToVault,
  updatePlantReport,
  updateDashboard,
  loadHistory,
  appendHistory,
  getRescanQueue,
  addToRescanQueue,
  clearRescanQueue,
} from './vault.js';

// ---------------------------------------------------------------------------
// Config
// ---------------------------------------------------------------------------

const config = JSON.parse(fs.readFileSync(new URL('../config.json', import.meta.url)));

function windowsToWsl(winPath) {
  if (!winPath.match(/^[A-Za-z]:\\/)) return winPath; // already a POSIX path
  return winPath
    .replace(/^([A-Za-z]):\\/, (_, d) => `/mnt/${d.toLowerCase()}/`)
    .replace(/\\/g, '/');
}

const STAGING_PATH   = windowsToWsl(config.stagingPath);
const VAULT_PATH     = windowsToWsl(config.vaultPath);
const POLL_MS        = config.pollIntervalMs ?? 10_000;
const LANGUAGE       = config.reportLanguage ?? 'English';
const DEBOUNCE_MS    = 2 * 60 * 1000; // 2 minutes — wait for all session photos to land

const IMAGE_EXTS = new Set(['.jpg', '.jpeg', '.png', '.webp', '.gif']);

function isImage(filePath) {
  return IMAGE_EXTS.has(path.extname(filePath).toLowerCase());
}

function todayISO() {
  return new Date().toISOString().slice(0, 10);
}

// ---------------------------------------------------------------------------
// Process a session (batch of photos)
// ---------------------------------------------------------------------------

async function processSession(filePaths) {
  const existing = filePaths.filter(f => fs.existsSync(f));
  if (existing.length === 0) {
    console.log('  No files found.');
    return;
  }

  console.log(`\n  Processing ${existing.length} photo(s) as one session...`);

  // Brief wait for cloud sync to settle
  await new Promise(r => setTimeout(r, 2000));

  const registry = loadRegistry(VAULT_PATH);
  const scanDate  = todayISO();

  // Load history for all known plants
  const histories = {};
  for (const plantId of Object.keys(registry).filter(k => !k.startsWith('_'))) {
    histories[plantId] = loadHistory(VAULT_PATH, plantId);
  }

  // Analyze all photos together
  let result;
  try {
    result = await analyzePhotos(existing, registry, histories, VAULT_PATH, MODELS.standard, LANGUAGE);
  } catch (err) {
    console.error(`  Analysis failed: ${err.message}`);
    // Move all photos anyway so they don't block the next scan
    for (const f of existing) {
      try {
        const { filename } = movePhotoToVault(f, VAULT_PATH);
        console.log(`  Moved: _attachments/${filename} (no analysis)`);
      } catch (moveErr) {
        console.error(`  Failed to move ${path.basename(f)}: ${moveErr.message}`);
      }
    }
    updateDashboard(VAULT_PATH, registry, [
      `Analysis failed for session (${existing.length} photos): ${err.message}`,
    ]);
    return;
  }

  // Move all photos to vault — track original index → vault filename
  const vaultFilenames = [];
  for (const f of existing) {
    try {
      const { filename } = movePhotoToVault(f, VAULT_PATH);
      vaultFilenames.push(filename);
      console.log(`  Moved: ${path.basename(f)} → _attachments/${filename}`);
    } catch (moveErr) {
      console.error(`  Failed to move ${path.basename(f)}: ${moveErr.message}`);
      vaultFilenames.push(null); // keep index alignment
    }
  }

  const warnings = [...result.uncertainties];

  for (const analysis of result.plants) {
    const indices = Array.isArray(analysis.imageIndices) && analysis.imageIndices.length > 0
      ? analysis.imageIndices
      : [...vaultFilenames.keys()];

    const plantPhotos = indices
      .map(i => vaultFilenames[i])
      .filter(Boolean);

    let plantId = analysis.matchedId;

    if (analysis.isNew || !plantId) {
      plantId = createPlantId(analysis.species, registry);
      registry[plantId] = {
        species:        analysis.species,
        commonName:     analysis.commonName,
        firstSeen:      scanDate,
        lastSeen:       scanDate,
        healthStatus:   analysis.healthStatus,
        location:       null,
        vessel:         null,
        referencePhoto: plantPhotos[0] ? `_attachments/${plantPhotos[0]}` : null,
        photoCount:     0,
        trend:          'N/A',
      };
      console.log(`  New plant: ${plantId} (${analysis.species})`);

      if (analysis.confidence === 'low') {
        const reason = analysis.uncertaintyNote || 'Low identification confidence';
        warnings.push(
          `New plant registered as "${plantId}" (${analysis.species}) with LOW confidence — run \`npm run rescan\` for an Opus analysis.`
        );
        addToRescanQueue(VAULT_PATH, plantId, plantPhotos, reason);
      }
    } else {
      const existing = registry[plantId];
      const prevStatus = existing.healthStatus;

      registry[plantId] = {
        ...existing,
        lastSeen:     scanDate,
        healthStatus: analysis.healthStatus,
        location:     analysis.locationChange ? null : existing.location,
        vessel:       analysis.vesselChange   ? null : existing.vessel,
      };

      if (analysis.locationChange) {
        warnings.push(`Location change detected for ${plantId} — please update the location field.`);
      }
      if (analysis.vesselChange) {
        warnings.push(`Pot/vessel change detected for ${plantId} — please update the vessel field.`);
      }
      if (analysis.confidence === 'low') {
        const reason = analysis.uncertaintyNote || 'Low match confidence';
        warnings.push(
          `Low confidence match for ${plantId} — run \`npm run rescan\` for an Opus analysis.`
        );
        addToRescanQueue(VAULT_PATH, plantId, plantPhotos, reason);
      }

      const statuses = ['Critical', 'Poor', 'Fair', 'Good', 'Excellent'];
      const prev = statuses.indexOf(prevStatus);
      const curr = statuses.indexOf(analysis.healthStatus);
      registry[plantId].trend =
        curr > prev ? 'Improving' :
        curr < prev ? 'Declining' : 'Stable';

      console.log(`  Updated: ${plantId} — ${analysis.healthStatus} (${registry[plantId].trend})`);
    }

    registry[plantId].photoCount = (registry[plantId].photoCount ?? 0) + plantPhotos.length;

    appendHistory(VAULT_PATH, plantId, {
      date:         scanDate,
      healthStatus: analysis.healthStatus,
      healthScore:  analysis.healthScore,
      urgency:      analysis.urgency,
      problems:     analysis.problems ?? null,
      photos:       plantPhotos,
      summary:      analysis.summary,
    });

    updatePlantReport(VAULT_PATH, plantId, registry[plantId], analysis, plantPhotos, scanDate);
    console.log(`  Report updated: ${plantId}/report.md (${plantPhotos.length} photo(s))`);

    saveRegistry(VAULT_PATH, registry);
  }

  updateDashboard(VAULT_PATH, loadRegistry(VAULT_PATH), warnings);
  console.log('  Dashboard updated.');

  if (warnings.length > 0) {
    console.log('\n  Warnings — action required:');
    warnings.forEach(w => console.log(`    • ${w}`));
  }
}

// ---------------------------------------------------------------------------
// Collect all images currently in the staging folder
// ---------------------------------------------------------------------------

function collectImages() {
  if (!fs.existsSync(STAGING_PATH)) {
    console.error(`Staging folder not found: ${STAGING_PATH}`);
    process.exit(1);
  }
  return fs.readdirSync(STAGING_PATH)
    .map(f => path.join(STAGING_PATH, f))
    .filter(f => isImage(f) && fs.statSync(f).isFile());
}

// ---------------------------------------------------------------------------
// Manual scan mode
// ---------------------------------------------------------------------------

async function scanOnce() {
  const files = collectImages();
  if (files.length === 0) {
    console.log('No photos found in staging folder.');
    return;
  }
  console.log(`Found ${files.length} photo(s).`);
  await processSession(files);
  console.log('\nDone.');
}

// ---------------------------------------------------------------------------
// Watch mode with 2-minute debounce accumulator
// ---------------------------------------------------------------------------

async function watchFolder() {
  const { default: chokidar } = await import('chokidar');

  console.log(`Watching: ${STAGING_PATH}`);
  console.log(`Vault:    ${VAULT_PATH}`);
  console.log(`Debounce: ${DEBOUNCE_MS / 1000}s after the last new photo`);
  console.log('Press Ctrl+C to stop.\n');

  // Initial scan for anything already waiting
  await scanOnce();

  const pending = new Set();
  let debounceTimer = null;

  const flush = async () => {
    const batch = [...pending];
    pending.clear();
    debounceTimer = null;
    console.log(`\nSession: ${batch.length} photo(s)`);
    await processSession(batch);
  };

  const watcher = chokidar.watch(STAGING_PATH, {
    persistent:    true,
    ignoreInitial: true,
    usePolling:    true,        // required for OneDrive / cloud sync folders under WSL
    interval:      POLL_MS,
    awaitWriteFinish: {
      stabilityThreshold: 3000,
      pollInterval:       500,
    },
  });

  watcher.on('add', (filePath) => {
    if (!isImage(filePath)) return;
    console.log(`  New photo: ${path.basename(filePath)} (waiting for more...)`);
    pending.add(filePath);
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(flush, DEBOUNCE_MS);
  });

  watcher.on('error', err => console.error('Watcher error:', err));
}

// ---------------------------------------------------------------------------
// Rescan mode  (Opus, explicit approval required)
// ---------------------------------------------------------------------------

async function confirm(question) {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  return new Promise(resolve => {
    rl.question(question, answer => {
      rl.close();
      resolve(['y', 'yes'].includes(answer.trim().toLowerCase()));
    });
  });
}

async function rescan() {
  const queue = getRescanQueue(VAULT_PATH);

  if (queue.length === 0) {
    console.log('No items queued for rescan.');
    return;
  }

  console.log(`\nQueued for Opus rescan (${queue.length}):\n`);
  for (const item of queue) {
    console.log(`  • ${item.plantId}`);
    console.log(`    Reason: ${item.reason}`);
    console.log(`    Photos: ${item.photos.join(', ')}`);
    console.log(`    Queued: ${item.addedAt}`);
    console.log('');
  }

  console.log('Rescan uses claude-opus-4-6 (higher cost).');
  const ok = await confirm('Continue? (y/n): ');

  if (!ok) {
    console.log('Cancelled.');
    return;
  }

  console.log('\nStarting Opus rescan...');

  const registry = loadRegistry(VAULT_PATH);
  const scanDate  = todayISO();
  const allWarnings = [];

  for (const item of queue) {
    const existingPhotos = item.photos
      .map(f => path.join(VAULT_PATH, f))
      .filter(f => fs.existsSync(f));

    if (existingPhotos.length === 0) {
      console.log(`  ${item.plantId}: photos not found, skipping.`);
      continue;
    }

    console.log(`\n  Rescanning: ${item.plantId} (${existingPhotos.length} photo(s))...`);

    const rescanHistories = {};
    for (const plantId of Object.keys(registry).filter(k => !k.startsWith('_'))) {
      rescanHistories[plantId] = loadHistory(VAULT_PATH, plantId);
    }

    let result;
    try {
      result = await analyzePhotos(existingPhotos, registry, rescanHistories, VAULT_PATH, MODELS.thorough, LANGUAGE);
    } catch (err) {
      console.error(`  Failed: ${err.message}`);
      allWarnings.push(`Rescan failed for ${item.plantId}: ${err.message}`);
      continue;
    }

    for (const analysis of result.plants) {
      const targetId = analysis.matchedId ?? item.plantId;
      const plantPhotos = (Array.isArray(analysis.imageIndices) && analysis.imageIndices.length > 0
        ? analysis.imageIndices.map(i => item.photos[i])
        : item.photos
      ).filter(Boolean);

      if (registry[targetId]) {
        registry[targetId] = {
          ...registry[targetId],
          species:      analysis.species,
          commonName:   analysis.commonName,
          lastSeen:     scanDate,
          healthStatus: analysis.healthStatus,
        };
      }

      appendHistory(VAULT_PATH, targetId, {
        date:         scanDate,
        healthStatus: analysis.healthStatus,
        healthScore:  analysis.healthScore,
        urgency:      analysis.urgency,
        problems:     analysis.problems ?? null,
        photos:       plantPhotos,
        summary:      analysis.summary,
      });

      updatePlantReport(VAULT_PATH, targetId, registry[targetId] ?? {}, analysis, plantPhotos, scanDate);
      saveRegistry(VAULT_PATH, registry);
      console.log(`  Updated: ${targetId}/report.md`);
    }

    if (result.uncertainties.length > 0) {
      allWarnings.push(...result.uncertainties);
    }
  }

  clearRescanQueue(VAULT_PATH);
  updateDashboard(VAULT_PATH, loadRegistry(VAULT_PATH), allWarnings);
  console.log('\nRescan complete. Dashboard updated.');
}

// ---------------------------------------------------------------------------
// Entry point
// ---------------------------------------------------------------------------

const watchMode  = process.argv.includes('--watch');
const rescanMode = process.argv.includes('--rescan');

if (rescanMode) {
  rescan().catch(err => { console.error(err); process.exit(1); });
} else if (watchMode) {
  watchFolder().catch(err => { console.error(err); process.exit(1); });
} else {
  scanOnce().catch(err => { console.error(err); process.exit(1); });
}

import Anthropic from '@anthropic-ai/sdk';
import fs from 'fs';
import path from 'path';

const client = new Anthropic();

const MEDIA_TYPES = {
  '.jpg':  'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.png':  'image/png',
  '.webp': 'image/webp',
  '.gif':  'image/gif',
};

export const MODELS = {
  standard: 'claude-sonnet-4-6',
  thorough: 'claude-opus-4-6',
};

const HEALTH_SCORE = {
  Excellent: 5,
  Good:      4,
  Fair:      3,
  Poor:      2,
  Critical:  1,
};

function getMediaType(filePath) {
  return MEDIA_TYPES[path.extname(filePath).toLowerCase()] ?? 'image/jpeg';
}

function encodeImage(filePath) {
  return {
    type: 'image',
    source: {
      type: 'base64',
      media_type: getMediaType(filePath),
      data: fs.readFileSync(filePath).toString('base64'),
    },
  };
}

function buildHistoryContext(histories) {
  const entries = Object.entries(histories);
  if (entries.length === 0) return null;

  return entries.map(([id, history]) => {
    if (!history || history.length === 0) return null;
    const recent = history.slice(-5);
    const lines = recent.map(h =>
      `    ${h.date}: ${h.healthStatus} (${h.healthScore}/5)` +
      (h.urgency !== 'None' ? `, urgency: ${h.urgency}` : '') +
      (h.problems ? `, problems: ${h.problems}` : '')
    ).join('\n');
    return `  ${id} — last ${recent.length} entries:\n${lines}`;
  }).filter(Boolean).join('\n\n');
}

/**
 * Analyze a batch of photos (one session) against the known plant registry.
 *
 * @param {string[]} photoPaths    - absolute paths to the session photos (in order)
 * @param {object}   registry     - current plant registry
 * @param {object}   histories    - map of { plantId: historyEntry[] } for known plants
 * @param {string}   vaultPath    - absolute path to the vault (for reference photos)
 * @param {string}   [model]      - model override; defaults to MODELS.standard
 * @param {string}   [language]   - language for AI-generated text; defaults to "English"
 * @returns {{ plants: PlantAnalysis[], uncertainties: string[] }}
 */
export async function analyzePhotos(photoPaths, registry, histories, vaultPath, model = MODELS.standard, language = 'English') {
  const content = [];

  // Session photos
  for (let i = 0; i < photoPaths.length; i++) {
    content.push({
      type: 'text',
      text: `--- SESSION PHOTO ${i + 1} OF ${photoPaths.length} ---`,
    });
    content.push(encodeImage(photoPaths[i]));
  }

  // Reference photos for known plants
  const knownPlants = Object.entries(registry).filter(([k]) => !k.startsWith('_'));
  if (knownPlants.length > 0) {
    content.push({
      type: 'text',
      text: '\n--- REFERENCE PHOTOS FOR KNOWN PLANTS ---\nUse these to match session plants against known individuals.',
    });
    for (const [id, plant] of knownPlants) {
      if (plant.referencePhoto) {
        const refPath = path.join(vaultPath, plant.referencePhoto);
        if (fs.existsSync(refPath)) {
          content.push({ type: 'text', text: `\nReference for ${id} (${plant.species} / ${plant.commonName}):` });
          content.push(encodeImage(refPath));
        }
      }
    }
  }

  // Build registry + history context
  const registryContext = knownPlants.length > 0
    ? knownPlants.map(([id, p]) =>
        `- ${id}: ${p.species} (${p.commonName}), last health: ${p.healthStatus}, entries: ${p.photoCount ?? 0}`
      ).join('\n')
    : 'No registered plants yet.';

  const historyContext = buildHistoryContext(histories);

  content.push({
    type: 'text',
    text: `
You are a plant health monitoring assistant. Above you see ${photoPaths.length} photo(s) from one session (different angles, close-ups, wide shots, etc.).

Known plant registry:
${registryContext}
${historyContext ? `\nHealth history (structured data for comparison):\n${historyContext}` : ''}

Instructions:
1. Identify ALL distinct plants visible across the session photos.
2. For each plant, use ALL relevant photos for a complete analysis.
3. Match against known plants where possible (use reference photos and history).
4. Record which photos show each plant (imageIndices, 0-based).
5. Compare with health history to identify trends or changes.

Respond ONLY with valid JSON, no markdown, no explanation:
{
  "plants": [
    {
      "matchedId": "<id from registry, or null if new>",
      "species": "<scientific name>",
      "commonName": "<common name>",
      "isNew": <true|false>,
      "confidence": "<high|medium|low>",
      "imageIndices": [<0-based photo indices>],
      "healthStatus": "<Excellent|Good|Fair|Poor|Critical>",
      "healthScore": <integer 1-5: Critical=1, Poor=2, Fair=3, Good=4, Excellent=5>,
      "summary": "<one practical sentence about the plant's condition>",
      "observations": "<what you see: colour, leaves, soil, growth>",
      "problems": "<diseases, pests, deficiencies, stress — or null>",
      "care": "<specific care advice>",
      "urgency": "<None|Watch|Act Soon|Urgent>",
      "locationChange": <true|false>,
      "vesselChange": <true|false>,
      "uncertaintyNote": "<explain anything you are uncertain about, or empty string>"
    }
  ]
}

Write summary, observations, problems, care, and uncertaintyNote in ${language}.
Keep these fields in English: healthStatus, urgency, confidence, species, commonName, matchedId.
Never wrap the JSON in a code block.`,
  });

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 120_000);

  let response;
  try {
    response = await client.messages.create(
      { model, max_tokens: 4000, messages: [{ role: 'user', content }] },
      { signal: controller.signal }
    );
  } finally {
    clearTimeout(timeoutId);
  }

  const raw = response.content[0].text.trim();

  let parsed;
  try {
    parsed = JSON.parse(raw);
  } catch {
    const match = raw.match(/```(?:json)?\s*([\s\S]*?)```/);
    if (match) {
      parsed = JSON.parse(match[1].trim());
    } else {
      throw new Error(`Claude returned non-JSON response: ${raw.slice(0, 200)}`);
    }
  }

  // Ensure healthScore is always present even if Claude omits it
  for (const plant of parsed.plants) {
    if (!plant.healthScore) {
      plant.healthScore = HEALTH_SCORE[plant.healthStatus] ?? 3;
    }
  }

  const uncertainties = parsed.plants
    .filter(p => p.uncertaintyNote)
    .map(p => `${p.matchedId ?? p.species}: ${p.uncertaintyNote}`);

  return { plants: parsed.plants, uncertainties };
}

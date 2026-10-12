const fs = require('fs');
const path = require('path');

const MODELS_DIR = path.join(__dirname, '..', 'assets', 'models', 'model');
const OUTPUT = path.join(__dirname, '..', 'RtG-Preview', 'models.json');
const EMBEDDED_OUTPUT = path.join(__dirname, '..', 'RtG-Preview', 'models-manifest.js');

function readModelJSON(jsonPath) {
  let parsed;

  try {
    parsed = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
  } catch (error) {
    throw new Error(`Invalid JSON: ${error.message}`);
  }

  if (!Array.isArray(parsed) || !parsed[0] || typeof parsed[0] !== 'object') {
    throw new Error('Expected a non-empty JSON array whose first item is the model object');
  }

  return parsed[0];
}

function generateManifest() {
  const models = {};
  const folders = fs.readdirSync(MODELS_DIR, { withFileTypes: true })
    .filter(entry => entry.isDirectory())
    .map(entry => entry.name)
    .sort((a, b) => a.localeCompare(b));

  for (const folder of folders) {
    const modelDir = path.join(MODELS_DIR, folder);
    const jsonPath = path.join(modelDir, `${folder}.json`);

    if (!fs.existsSync(jsonPath)) {
      console.warn(`Missing JSON for ${folder}, skipping`);
      continue;
    }

    let model;
    try {
      model = readModelJSON(jsonPath);
    } catch (error) {
      console.warn(`Failed to read model ${folder}: ${error.message}`);
      continue;
    }

    const preview = model['RtG-Format']?.['RtG-Preview'] || {};
    const rawSize = preview.Size ?? {};
    const sizeMap = rawSize && typeof rawSize === 'object' && !Array.isArray(rawSize)
      ? rawSize
      : { default: rawSize };

    // These fields are at the model JSON root, not inside RtG-Preview.
    const defaultBranch = model['Default Branch'] ?? [`./${folder}.obj`];
    const mainObj = Array.isArray(defaultBranch) ? defaultBranch[0] : defaultBranch;

    if (typeof mainObj !== 'string' || !mainObj) {
      console.warn(`Invalid Default Branch for ${folder}, skipping`);
      continue;
    }

    const branchMap = model.Branches && typeof model.Branches === 'object'
      ? model.Branches
      : {};
    const branchesStart = model['Branches Start'] || {};
    const localPoints = model.LocalPoints || {};

    const branches = Object.entries(branchMap).map(([pointId, obj]) => ({
      pointId,
      obj,
      start: branchesStart[obj] ?? null,
      connectionPoint: localPoints[pointId] ?? null,
      size: sizeMap[obj] ?? sizeMap[`./${String(obj).replace(/^\.\//, '')}`] ?? sizeMap.default ?? 1
    }));

    models[folder] = {
      folder,
      obj: mainObj,
      json: `./${folder}.json`,
      hasBranches: branches.length > 0,
      size: sizeMap.default ?? 1,
      defaultBranch,
      branches
    };
  }

  const manifest = {
    version: '2.0',
    generated: new Date().toISOString(),
    models
  };

  fs.writeFileSync(OUTPUT, JSON.stringify(manifest, null, 2) + '\n');
  console.log(`Generated ${OUTPUT} with ${Object.keys(models).length} models`);

  generateEmbeddedManifest(manifest);
}

function generateEmbeddedManifest(manifest) {
  const jsContent = `// Embedded model manifest for RtG-Preview local (file://) use
// Generated: ${manifest.generated}
// This file should be loaded via <script> before preview.js

window.RtGEmbeddedManifest = ${JSON.stringify(manifest, null, 2)};
`;

  fs.writeFileSync(EMBEDDED_OUTPUT, jsContent);
  console.log(`Generated ${EMBEDDED_OUTPUT} for local use`);
}

generateManifest();

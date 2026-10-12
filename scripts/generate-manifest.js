const fs = require('fs');
const path = require('path');

const MODELS_DIR = path.join(__dirname, '..', 'assets', 'models', 'model');
const OUTPUT = path.join(__dirname, '..', 'RtG-Preview', 'models.json');
const EMBEDDED_OUTPUT = path.join(__dirname, '..', 'RtG-Preview', 'models-manifest.js');

function generateManifest() {
  const models = {};
  const folders = fs.readdirSync(MODELS_DIR, { withFileTypes: true })
    .filter(entry => entry.isDirectory())
    .map(entry => entry.name);

  for (const folder of folders) {
    const modelDir = path.join(MODELS_DIR, folder);
    const jsonPath = path.join(modelDir, `${folder}.json`);

    if (!fs.existsSync(jsonPath)) {
      console.warn(`Missing JSON for ${folder}, skipping`);
      continue;
    }

    let model;
    try {
      const parsed = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));

      if (!Array.isArray(parsed) || !parsed[0] || typeof parsed[0] !== 'object') {
        throw new Error('Expected an array containing a model object');
      }

      model = parsed[0];
    } catch (error) {
      console.warn(`Failed to parse JSON for ${folder}: ${error.message}`);
      continue;
    }

    const format = model['RtG-Format'] || {};
    const preview = format['RtG-Preview'] || {};
    const sizeMap = preview.Size || {};
    const branches = model.Branches || {};
    const branchesStart = model['Branches Start'] || {};
    const localPoints = model.LocalPoints || {};
    const defaultBranch = model['Default Branch'];

    if (!Array.isArray(defaultBranch) || defaultBranch.length === 0) {
      console.warn(`Missing or invalid Default Branch for ${folder}, skipping`);
      continue;
    }

    const mainObj = defaultBranch[0];

    if (typeof mainObj !== 'string' || !mainObj) {
      console.warn(`Invalid main OBJ path for ${folder}, skipping`);
      continue;
    }

    const branchEntries = Object.entries(branches).map(([pointId, obj]) => {
      if (typeof obj !== 'string') {
        console.warn(`Invalid branch path "${pointId}" in ${folder}`);
        return null;
      }

      return {
        pointId,
        obj,
        start: branchesStart[obj] || null,
        connectionPoint: localPoints[pointId] || null,
        size: sizeMap[obj] ?? sizeMap.default ?? 1
      };
    }).filter(Boolean);

    models[folder] = {
      folder,
      json: `./${folder}.json`,
      defaultBranch,
      obj: mainObj,
      size: sizeMap.default ?? 1,
      hasBranches: branchEntries.length > 0,
      branches: branchEntries
    };
  }

  const manifest = {
    version: '2.0',
    generated: new Date().toISOString(),
    models
  };

  fs.writeFileSync(OUTPUT, JSON.stringify(manifest, null, 2));
  console.log(`Generated ${OUTPUT} with ${Object.keys(models).length} models`);

  const embeddedContent = [
    '// Embedded model manifest for RtG-Preview local (file://) use',
    `// Generated: ${manifest.generated}`,
    'window.RtGEmbeddedManifest = ',
    JSON.stringify(manifest, null, 2),
    ';',
    ''
  ].join('\n');

  fs.writeFileSync(EMBEDDED_OUTPUT, embeddedContent);
  console.log(`Generated ${EMBEDDED_OUTPUT} for local use`);
}

generateManifest();
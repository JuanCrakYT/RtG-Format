const fs = require('fs');
const path = require('path');

const MODELS_DIR = path.join(__dirname, '..', 'assets', 'models', 'model');
const OUTPUT = path.join(__dirname, '..', 'RtG-Preview', 'models.json');
const EMBEDDED_OUTPUT = path.join(__dirname, '..', 'RtG-Preview', 'models-manifest.js');

function generateManifest() {
  const models = {};
  const folders = fs.readdirSync(MODELS_DIR, { withFileTypes: true })
    .filter(d => d.isDirectory())
    .map(d => d.name);
  
  for (const folder of folders) {
    const jsonPath = path.join(MODELS_DIR, folder, `${folder}.json`);
    if (!fs.existsSync(jsonPath)) {
      console.warn(`Missing JSON for ${folder}, skipping`);
      continue;
    }
    
    let json;
    try {
      json = JSON.parse(fs.readFileSync(jsonPath, 'utf8'))[0];
    } catch (e) {
      console.warn(`Failed to parse JSON for ${folder}: ${e.message}`);
      continue;
    }
    
    const hasSplit = fs.existsSync(path.join(MODELS_DIR, folder, 'split'));
    const preview = json['RtG-Format']?.['RtG-Preview'] || {};
    const size = preview.Size?.default ?? 1.0;
    const defaultBranch = preview['Default Branch'] || [`./${folder}.obj`];
    
    models[folder] = {
      folder,
      obj: `./${folder}.obj`,
      json: `./${folder}.json`,
      hasBranches: hasSplit,
      size,
      defaultBranch
    };
    
    if (hasSplit) {
      const branches = json.Branches || {};
      const branchesStart = json['Branches Start'] || {};
      const localPoints = json.LocalPoints || {};
      
      models[folder].branches = Object.entries(branches).map(([pointId, obj]) => ({
        pointId,
        obj,
        start: branchesStart[obj],
        connectionPoint: localPoints[pointId] || null
      }));
    }
  }
  
  const manifest = {
    version: '1.0',
    generated: new Date().toISOString(),
    models
  };
  
  fs.writeFileSync(OUTPUT, JSON.stringify(manifest, null, 2));
  console.log(`Generated ${OUTPUT} with ${Object.keys(models).length} models`);
  
  // Generate embedded manifest for local file:// use
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
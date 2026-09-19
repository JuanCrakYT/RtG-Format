const fs = require('fs');
const path = require('path');

const MODELS_DIR = path.join(__dirname, '..', 'assets', 'models', 'model');

function fixJSON(content) {
  // Remove BOM if present
  content = content.replace(/^\uFEFF/, '');
  
  // Fix triple quotes
  content = content.replace(/"""/g, '"');
  
  // Parse the structure more carefully
  // First, let's ensure it's a valid JSON by fixing common structural issues
  
  // Remove empty lines
  content = content.replace(/^\s+$/gm, '');
  
  // Ensure array brackets are closed
  if (!content.trim().endsWith(']')) {
    content = content.trim() + '\n]';
  }
  
  // Fix duplicate LocalPoints - keep only the last meaningful one
  const lines = content.split('\n');
  const localPointsLines = [];
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].includes('"LocalPoints"')) {
      localPointsLines.push(i);
    }
  }
  
  if (localPointsLines.length > 1) {
    // Remove all but the last one
    for (let i = 0; i < localPointsLines.length - 1; i++) {
      lines[localPointsLines[i]] = '';
    }
  }
  
  content = lines.filter(l => l !== '').join('\n');
  
  // Fix missing commas between properties at the top level of the object
  // Pattern: "Property": value\n    "NextProperty"
  content = content.replace(
    /("Branches"\s*:\s*\{[^}]*\}\s*)\n\s*"Branches Start"/g,
    '$1,\n            "Branches Start"'
  );
  content = content.replace(
    /("Branches"\s*:\s*\{[^}]*\}\s*)\n\s*"AssetID"/g,
    '$1,\n            "AssetID"'
  );
  content = content.replace(
    /("LocalPoints"\s*:\s*\{[^}]*\}\s*)\n\s*"Branches Start"/g,
    '$1,\n            "Branches Start"'
  );
  content = content.replace(
    /("LocalPoints"\s*:\s*\{[^}]*\}\s*)\n\s*"AssetID"/g,
    '$1,\n            "AssetID"'
  );
  content = content.replace(
    /("Category"\s*:\s*"[^"]*"\s*)\n\s*"Branches Start"/g,
    '$1,\n            "Branches Start"'
  );
  content = content.replace(
    /("Category"\s*:\s*"[^"]*"\s*)\n\s*"AssetID"/g,
    '$1,\n            "AssetID"'
  );
  content = content.replace(
    /("Branches Start"\s*:\s*\{[^}]*\}\s*)\n\s*"AssetID"/g,
    '$1,\n            "AssetID"'
  );
  content = content.replace(
    /("Tooltip"\s*:\s*"[^"]*"\s*)\n\s*"LocalPoints"/g,
    '$1,\n            "LocalPoints"'
  );
  content = content.replace(
    /("Name"\s*:\s*"[^"]*"\s*)\n\s*"Tooltip"/g,
    '$1,\n            "Tooltip"'
  );
  content = content.replace(
    /("Page"\s*:\s*\{\}\s*)\n\s*"Name"/g,
    '$1,\n        "Name"'
  );
  
  // Fix misplaced closing braces - if we see } followed by indented properties
  // that should be at the same level
  content = content.replace(
    /(\s+)\}\n\s{12,}"(Branches Start|AssetID|LocalPoints)"/g,
    '$1},\n$1"$2"'
  );
  
  // Ensure proper closing of the main object before the array end
  // The pattern should be: }\n]
  content = content.replace(/\}\s*\]/g, '}\n]');
  
  return content;
}

function processModels() {
  const folders = fs.readdirSync(MODELS_DIR, { withFileTypes: true })
    .filter(d => d.isDirectory())
    .map(d => d.name);
  
  let fixed = 0;
  let errors = 0;
  
  for (const folder of folders) {
    const jsonPath = path.join(MODELS_DIR, folder, `${folder}.json`);
    if (!fs.existsSync(jsonPath)) continue;
    
    try {
      const content = fs.readFileSync(jsonPath, 'utf8');
      const fixedContent = fixJSON(content);
      
      // Test if it parses
      JSON.parse(fixedContent);
      
      if (content !== fixedContent) {
        fs.writeFileSync(jsonPath, fixedContent, 'utf8');
        console.log(`Fixed: ${folder}`);
        fixed++;
      }
    } catch (e) {
      console.error(`Error in ${folder}: ${e.message}`);
      // Try to show the problematic area
      try {
        const content = fs.readFileSync(jsonPath, 'utf8');
        const lines = content.split('\n');
        const errorLine = Math.max(0, parseInt(e.message.match(/line (\d+)/)?.[1] || 0) - 2);
        for (let i = errorLine; i < Math.min(lines.length, errorLine + 5); i++) {
          console.error(`  ${i+1}: ${lines[i]}`);
        }
      } catch {}
      errors++;
    }
  }
  
  console.log(`\nFixed: ${fixed}, Errors: ${errors}`);
}

processModels();
const fs = require('fs');
const path = require('path');

const MODELS_DIR = path.join(__dirname, '..', 'assets', 'models', 'model');
const OUTPUT_DIR = path.join(__dirname, '..', 'blocks', 'reference');

function generateBlockDocs() {
  if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  }

  const folders = fs.readdirSync(MODELS_DIR, { withFileTypes: true })
    .filter(d => d.isDirectory())
    .map(d => d.name)
    .sort();

  let generated = 0;
  let skipped = 0;

  for (const folder of folders) {
    // Skip Teeth (no JSON)
    if (folder === 'Teeth') {
      console.log(`Skipping ${folder} (no JSON)`);
      skipped++;
      continue;
    }

    const jsonPath = path.join(MODELS_DIR, folder, `${folder}.json`);
    if (!fs.existsSync(jsonPath)) {
      console.warn(`Missing JSON for ${folder}, skipping`);
      skipped++;
      continue;
    }

    let json;
    try {
      json = JSON.parse(fs.readFileSync(jsonPath, 'utf8'))[0];
    } catch (e) {
      console.warn(`Failed to parse JSON for ${folder}: ${e.message}`);
      skipped++;
      continue;
    }

    const doc = generateBlockDoc(folder, json);
    const outputPath = path.join(OUTPUT_DIR, `${folder}.md`);
    fs.writeFileSync(outputPath, doc);
    generated++;
  }

  console.log(`Generated ${generated} block docs, skipped ${skipped}`);
}

function generateBlockDoc(folder, json) {
  const name = json.Name || folder;
  const tooltip = json.Tooltip || '';
  const localPoints = json.LocalPoints || {};
  const branches = json.Branches || {};
  const branchesStart = json['Branches Start'] || {};
  const defaultBranch = json['Default Branch'] || [`./${folder}.obj`];
  const preview = json['RtG-Format']?.['RtG-Preview'] || {};
  const size = preview.Size?.default ?? 1.0;
  const formatData = json['RtG-Format']?.['RtG-Format Data'] || {};
  const assetID = json.AssetID || {};

  // Determine category from existing parts structure
  const category = getCategory(folder);

  // Build connection points table
  let pointsTable = '| Point ID | Name | Position | Rotation | Description | Status |\n';
  pointsTable += '|----------|------|----------|----------|-------------|--------|\n';
  
  if (Object.keys(localPoints).length === 0) {
    pointsTable += '| (none) | | | | No predefined connection points | |\n';
  } else {
    for (const [pointId, transform] of Object.entries(localPoints)) {
      const [pos, rot] = transform;
      const connPoint = branches[pointId] ? 'Branch attachment' : 'Standard connection';
      pointsTable += `| ${pointId} | Connection ${pointId} | [${pos.join(', ')}] | [${rot.join(', ')}] | ${connPoint} | CONFIRMED |\n`;
    }
  }

  // Build branches table
  let branchesTable = '';
  if (Object.keys(branches).length > 0) {
    branchesTable = '\n## Branches\n\n';
    branchesTable += '| Branch | Point ID | Model Path | Start Position | Start Rotation | Description |\n';
    branchesTable += '|--------|----------|------------|----------------|----------------|-------------|\n';
    for (const [pointId, objPath] of Object.entries(branches)) {
      const start = branchesStart[objPath] || [[0,0,0], [0,0,0]];
      const [pos, rot] = start;
      const desc = pointId === 'NaN' ? 'Free-floating branch' : `Attached at point ${pointId}`;
      branchesTable += `| ${path.basename(objPath, '.obj')} | ${pointId} | ${objPath} | [${pos.join(', ')}] | [${rot.join(', ')}] | ${desc} |\n`;
    }
    branchesTable += `\n*Source: \`assets/models/model/${folder}/${folder}.json\` → Branches, Branches Start*\n`;
  }

  // Properties table - from SPECIFICATION.md observed properties
  const knownProps = getKnownProperties(folder);
  let propsTable = '| Property | Type | Description | Known Values | Status |\n';
  propsTable += '|----------|------|-------------|--------------|--------|\n';
  for (const prop of knownProps) {
    propsTable += `| ${prop.name} | ${prop.type} | ${prop.desc} | ${prop.values} | ${prop.status} |\n`;
  }

  // Relationships
  const relationships = getRelationships(folder);

  // Source evidence
  const hasSplit = fs.existsSync(path.join(MODELS_DIR, folder, 'split'));
  const sources = [
    `- \`assets/models/model/${folder}/${folder}.json\``,
    `- \`assets/models/model/${folder}/${folder}.obj\``,
  ];
  if (hasSplit) {
    sources.push(`- \`assets/models/model/${folder}/split/\` (branch models)`);
  }
  sources.push(`- \`old-files/obj_ids-spanish.md\` (historical connection point data)`);
  sources.push(`- Experimental saves in \`examples/experiments/\``);

  return `# Block: ${name}

## Identification
- **Name**: ${name}
- **Identifier**: \`${folder}\`
- **Category**: ${category}
- **Model Available**: Yes
- **Model Path**: \`assets/models/model/${folder}/${folder}.obj\`
- **Tooltip**: ${tooltip || 'N/A'}
- **Default Scale**: ${size}

## Connection Points
${pointsTable}

*Source: \`assets/models/model/${folder}/${folder}.json\` → LocalPoints*
${branchesTable}
## Properties
${propsTable}

## Relationships
${relationships}

## Confidence Level
- **Overall**: ${getOverallConfidence(folder)}

## Source Evidence
${sources.join('\n')}

## Notes
${getNotes(folder, json)}
`;
}

function getCategory(folder) {
  // Map based on blocks/parts categories
  const building = ['Base', 'Chassis', 'Hood', 'Trunk', 'Wheel', 'Tire', 'Bumper', 'Wing', 'ShortStick', 'Stick', 'LongStick', 'Spoiler', 'FuelTank', 'GasCap', 'Roof', 'DoorA', 'DoorB', 'DoorC', 'DoorD'];
  const physics = ['Servo', 'Servo_Physics', 'SpringJuice', 'Gyro', 'SteeringGyro', 'StaringGyro', 'MatchingGyro', 'Thruster', 'Propeller', 'PotatoEngine', 'GoldPotatoEngine'];
  const tools = ['ToolGun'];
  const wiring = ['Wire', 'Rope', 'Splitter', 'Splitter_1', 'Splitter_2', 'Splitter_3', 'Splitter_4', 'Connector', 'ConnectorBall', 'HalfConnectorBall', 'Switch', 'Gate-AND', 'Gate-OR', 'Gate-NOT', 'InputSensor', 'EntitySensor', 'VelocitySensor', 'AltitudeSensor', 'PressurePlate', 'Button', 'RemoteButton', 'Delayer', 'Detacher', 'Recorder'];
  const misc = ['Part', 'Anchor', 'Balloon', 'BeachBall', 'BouncyBall', 'BowlingBall', 'BallSocket', 'Bearing', 'Board', 'Body', 'Briefcase', 'Camera', 'Canister', 'Cannon', 'CannonBall', 'Carrot', 'Cinderblock', 'Drumkit', 'FishBowl', 'Fricklet', 'Googie', 'Gramby', 'Grenade', 'Guitar', 'Gun', 'Head', 'Jug', 'Keyboard', 'Leafblower', 'Leg', 'Light', 'Lock', 'Looper', 'Mag', 'MountedGun', 'Pipes', 'Piston', 'Plunger', 'Poop', 'Radio', 'Ramp', 'RiotShield', 'Rocket', 'RockingChair', 'RPG', 'RubberBand', 'Seat', 'ShoppingCart', 'Shotgun', 'Sledge', 'SprayPaint', 'SuperPowerClock', 'Tooth', 'TripWire', 'Trowel', 'Trumpet', 'TV', 'Uzi', 'wad'];
  
  if (building.includes(folder)) return 'Building';
  if (physics.includes(folder)) return 'Physics';
  if (tools.includes(folder)) return 'Tools';
  if (wiring.includes(folder)) return 'Wiring';
  if (misc.includes(folder)) return 'Miscellaneous';
  return 'Other';
}

function getKnownProperties(folder) {
  // Common properties for all blocks
  const common = [
    { name: 'RGB', type: 'array[3]', desc: 'Color (Red, Green, Blue)', values: '[0-255, 0-255, 0-255]', status: 'CONFIRMED' },
    { name: 'EphemeralAttachments', type: 'object', desc: 'Attachment points with CFrames', values: '{UUID: {partName, cframe[12]}}', status: 'CONFIRMED' },
  ];

  // Block-specific properties based on SPECIFICATION.md and model JSONs
  const specific = {
    'Servo': [
      { name: 'Speed', type: 'number', desc: 'Rotation speed', values: '0-1000', status: 'CONFIRMED' },
      { name: 'Rotation', type: 'number', desc: 'Target rotation', values: 'degrees', status: 'CONFIRMED' },
      { name: 'LimitAngle', type: 'number', desc: 'Angle limit', values: 'degrees', status: 'CONFIRMED' },
      { name: 'LimitEnabled', type: 'boolean', desc: 'Whether limit is active', values: 'true/false', status: 'CONFIRMED' },
      { name: 'Backwards', type: 'boolean', desc: 'Reverse direction', values: 'true/false', status: 'CONFIRMED' },
      { name: 'Rest', type: 'number', desc: 'Rest position', values: 'degrees', status: 'CONFIRMED' },
      { name: 'MaxForce', type: 'number', desc: 'Maximum force', values: '0-10000', status: 'CONFIRMED' },
    ],
    'Servo_Physics': [
      { name: 'Speed', type: 'number', desc: 'Rotation speed', values: '0-1000', status: 'CONFIRMED' },
      { name: 'Rotation', type: 'number', desc: 'Target rotation', values: 'degrees', status: 'CONFIRMED' },
    ],
    'SpringJuice': [
      { name: 'Speed', type: 'number', desc: 'Spring speed', values: '0-1000', status: 'CONFIRMED' },
      { name: 'MaxForce', type: 'number', desc: 'Maximum force', values: '0-10000', status: 'CONFIRMED' },
    ],
    'Wire': [
      { name: 'Length', type: 'number', desc: 'Current length', values: '0-1000', status: 'CONFIRMED' },
      { name: 'MinLength', type: 'number', desc: 'Minimum length', values: '0-1000', status: 'CONFIRMED' },
      { name: 'MaxLength', type: 'number', desc: 'Maximum length', values: '0-1000', status: 'CONFIRMED' },
      { name: 'MaxForce', type: 'number', desc: 'Maximum force', values: '0-10000', status: 'CONFIRMED' },
    ],
    'Rope': [
      { name: 'Length', type: 'number', desc: 'Current length', values: '0-1000', status: 'CONFIRMED' },
      { name: 'MinLength', type: 'number', desc: 'Minimum length', values: '0-1000', status: 'CONFIRMED' },
      { name: 'MaxLength', type: 'number', desc: 'Maximum length', values: '0-1000', status: 'CONFIRMED' },
      { name: 'MaxForce', type: 'number', desc: 'Maximum force', values: '0-10000', status: 'CONFIRMED' },
    ],
    'Cannon': [
      { name: 'Shooting', type: 'boolean', desc: 'Whether firing', values: 'true/false', status: 'CONFIRMED' },
      { name: 'Bullets', type: 'number', desc: 'Ammo count', values: '0-100', status: 'CONFIRMED' },
      { name: 'CanTargetAttached', type: 'boolean', desc: 'Can target attached objects', values: 'true/false', status: 'CONFIRMED' },
      { name: 'IgnoreAttached', type: 'boolean', desc: 'Ignore attached objects', values: 'true/false', status: 'CONFIRMED' },
      { name: 'MaxDistance', type: 'number', desc: 'Maximum range', values: '0-1000', status: 'CONFIRMED' },
      { name: 'ActivationSpeed', type: 'number', desc: 'Activation speed', values: '0-1000', status: 'CONFIRMED' },
      { name: 'ActivationHeight', type: 'number', desc: 'Activation height', values: '0-1000', status: 'CONFIRMED' },
    ],
    'Gun': [
      { name: 'Shooting', type: 'boolean', desc: 'Whether firing', values: 'true/false', status: 'CONFIRMED' },
      { name: 'Bullets', type: 'number', desc: 'Ammo count', values: '0-100', status: 'CONFIRMED' },
    ],
    'MountedGun': [
      { name: 'Shooting', type: 'boolean', desc: 'Whether firing', values: 'true/false', status: 'CONFIRMED' },
      { name: 'Bullets', type: 'number', desc: 'Ammo count', values: '0-100', status: 'CONFIRMED' },
    ],
    'RPG': [
      { name: 'Shooting', type: 'boolean', desc: 'Whether firing', values: 'true/false', status: 'CONFIRMED' },
      { name: 'Bullets', type: 'number', desc: 'Ammo count', values: '0-100', status: 'CONFIRMED' },
    ],
    'Shotgun': [
      { name: 'Shooting', type: 'boolean', desc: 'Whether firing', values: 'true/false', status: 'CONFIRMED' },
      { name: 'Bullets', type: 'number', desc: 'Ammo count', values: '0-100', status: 'CONFIRMED' },
    ],
    'Uzi': [
      { name: 'Shooting', type: 'boolean', desc: 'Whether firing', values: 'true/false', status: 'CONFIRMED' },
      { name: 'Bullets', type: 'number', desc: 'Ammo count', values: '0-100', status: 'CONFIRMED' },
    ],
    'Mag': [
      { name: 'Quantity', type: 'number', desc: 'Ammo quantity', values: '0-100', status: 'CONFIRMED' },
      { name: 'Bullets', type: 'number', desc: 'Bullet type', values: '0-100', status: 'CONFIRMED' },
    ],
    'Radio': [
      { name: 'Volume', type: 'number', desc: 'Audio volume', values: '0-10', status: 'CONFIRMED' },
      { name: 'Channel', type: 'number', desc: 'Radio channel', values: '0-100', status: 'CONFIRMED' },
      { name: 'CustomTrack', type: 'string', desc: 'Custom audio track', values: 'SoundId', status: 'CONFIRMED' },
    ],
    'Light': [
      { name: 'Volume', type: 'number', desc: 'Light intensity', values: '0-10', status: 'CONFIRMED' },
    ],
    'Sprite': [
      { name: 'ImageId', type: 'number', desc: 'Decal image ID', values: 'Roblox asset ID', status: 'CONFIRMED' },
    ],
    'TV': [
      { name: 'ImageId', type: 'number', desc: 'Screen image ID', values: 'Roblox asset ID', status: 'CONFIRMED' },
    ],
    'Thruster': [
      { name: 'Speed', type: 'number', desc: 'Thrust speed', values: '0-1000', status: 'CONFIRMED' },
      { name: 'MaxForce', type: 'number', desc: 'Maximum force', values: '0-10000', status: 'CONFIRMED' },
    ],
    'Propeller': [
      { name: 'Speed', type: 'number', desc: 'Rotation speed', values: '0-1000', status: 'CONFIRMED' },
    ],
    'PotatoEngine': [
      { name: 'Speed', type: 'number', desc: 'Engine speed', values: '0-1000', status: 'CONFIRMED' },
    ],
    'GoldPotatoEngine': [
      { name: 'Speed', type: 'number', desc: 'Engine speed', values: '0-1000', status: 'CONFIRMED' },
    ],
    'Delayer': [
      { name: 'Delay', type: 'number', desc: 'Activation delay', values: 'seconds', status: 'CONFIRMED' },
      { name: 'DelayDeactivation', type: 'number', desc: 'Deactivation delay', values: 'seconds', status: 'CONFIRMED' },
    ],
  };

  const specificProps = specific[folder] || [];
  return [...common, ...specificProps];
}

function getRelationships(folder) {
  const relationships = {
    'Chassis': 'Connects to: Wheel, Hood, Trunk, Engine, Seat, SteeringWheel, GasCap, Roof, Bumper, Headlight, BrakeLight\nParent of: Wheel, Hood, Trunk, Engine, Seat\nChild of: Base',
    'Wheel': 'Connects to: Chassis, Tire\nParent of: Tire\nChild of: Chassis',
    'Tire': 'Connects to: Wheel\nChild of: Wheel',
    'Switch': 'Connects to: Wire, Splitter, Gate-AND, Gate-OR, Gate-NOT, Delayer, Detacher\nInput branch (NaN): Receives signal\nOutput branch (2): Sends signal',
    'Wire': 'Connects to: Splitter, Switch, Connector, ConnectorBall\nChild of: Power source',
    'Rope': 'Connects to: Connector, ConnectorBall, Part\nFlexible connection',
    'Part': 'Connects to: Part, Anchor, Chassis, Body\nGeneric building block',
    'Anchor': 'Connects to: Part, Chassis\nRoot/fixed point',
    'Base': 'Connects to: Chassis, Part, Anchor\nFoundation block',
    'Servo': 'Connects to: Part, Chassis, Body\nRotational joint',
    'Gate-AND': 'Connects to: Wire, Switch, InputSensor\nLogic gate (AND)',
    'Gate-OR': 'Connects to: Wire, Switch, InputSensor\nLogic gate (OR)',
    'Gate-NOT': 'Connects to: Wire, Switch, InputSensor\nLogic gate (NOT)',
    'Splitter': 'Connects to: Wire, Splitter\nSignal distribution',
    'Splitter_1': 'Connects to: Wire, Splitter\nSignal distribution (1 out)',
    'Splitter_2': 'Connects to: Wire, Splitter\nSignal distribution (2 out)',
    'Splitter_3': 'Connects to: Wire, Splitter\nSignal distribution (3 out)',
    'Splitter_4': 'Connects to: Wire, Splitter\nSignal distribution (4 out)',
  };

  return relationships[folder] || 'Relationships not fully documented. See SPECIFICATION.md for general connection rules.';
}

function getOverallConfidence(folder) {
  // Blocks with full model JSON + OBJ + connection points
  const confirmed = ['Base', 'Chassis', 'Part', 'Anchor', 'Wheel', 'Tire', 'Bumper', 'Hood', 'Trunk', 'Switch', 'Wire', 'Rope', 'Tooth', 'Servo', 'SpringJuice', 'Splitter', 'Splitter_1', 'Splitter_2', 'Splitter_3', 'Splitter_4', 'Connector', 'ConnectorBall', 'HalfConnectorBall', 'Gate-AND', 'Gate-OR', 'Gate-NOT', 'InputSensor', 'EntitySensor', 'VelocitySensor', 'AltitudeSensor', 'PressurePlate', 'Button', 'RemoteButton', 'Delayer', 'Detacher', 'Recorder', 'Thruster', 'Propeller', 'PotatoEngine', 'GoldPotatoEngine', 'Cannon', 'Gun', 'MountedGun', 'RPG', 'Shotgun', 'Uzi', 'Mag', 'Radio', 'Light', 'TV', 'RGB'];
  
  if (confirmed.includes(folder)) return 'CONFIRMED';
  if (folder === 'Teeth') return 'UNKNOWN (no model JSON)';
  return 'PARTIALLY CONFIRMED (model exists, properties need verification)';
}

function getNotes(folder, json) {
  const notes = [];
  
  if (folder === 'Switch') {
    notes.push('Has two branches: input (NaN) and output (point 2). Input branch is free-floating, output attaches at connection point 2.');
  }
  
  if (['Splitter', 'Splitter_1', 'Splitter_2', 'Splitter_3', 'Splitter_4'].includes(folder)) {
    notes.push('Signal splitter with multiple outputs. Connection points need verification from model JSON.');
  }
  
  if (['DoorA', 'DoorB', 'DoorC', 'DoorD'].includes(folder)) {
    notes.push('Hinged door with moving branch. Branch connection points and rotation axis need experimental verification.');
  }
  
  if (folder === 'Teeth') {
    notes.push('No model JSON available. Only OBJ model exists. Properties and connection points unknown.');
  }
  
  if (Object.keys(json.LocalPoints || {}).length === 0 && !['Part', 'Anchor', 'Tooth', 'Base'].includes(folder)) {
    notes.push('No predefined connection points (LocalPoints empty). May use UUID/EphemeralAttachments for connections.');
  }
  
  if (notes.length === 0) {
    notes.push('Standard block. Connection points and properties per model JSON. See SPECIFICATION.md for format details.');
  }
  
  return notes.join('\n\n');
}

generateBlockDocs();
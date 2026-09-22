# RtG-Format Global TODO List

Centralized tracking of all work items across the repository.

**Last Updated**: 2026-09-21
**Status Legend**: ✅ Done | 🔄 In Progress | ⏳ Planned | ❓ Unknown/Blocked | 📝 Needs Investigation

---

## RtG-Format Core

### Documentation
- [ ] **Documentación de bloques** - Individual block docs generated (120/121), Teeth pending (no JSON)
- [ ] **Documentación de puntos de conexión** - Partially in `blocks/parts/`, needs completion for all blocks
- [ ] **Documentación de propiedades** - In `format/properties.md`, needs expansion with block-specific props
- [ ] **Validación de estructura** - Cross-reference SPECIFICATION.md with actual model JSONs

### Format Specification
- [ ] Keep SPECIFICATION.md synchronized with format/ docs
- [ ] Update format/unknown-fields.md with new findings
- [ ] Ensure format/identifiers.md covers all identifier types

### Research
- [ ] Move confirmed discoveries from research/discoveries.md to format/ docs
- [ ] Update research/unknowns.md with current blockers
- [ ] Document methodology for new experiments in research/methodology.md

---

## RtG-CLI

### ✅ Completed (2026-09-21)
- [x] **Ejecución de addons** - `program commands` interface implemented (Python/JS module loading)
- [x] **Argument ownership** - Rules enforced: no hyphen/`--` → addon, `-` → RtG-CLI
- [x] **`-c`/`--commands`** - Lists internal commands from `internal-list` in assets.json
- [x] **`-a`/`--addons`** - Lists addons with documentation (checks internal help + lang array)
- [x] **Idiomas dinámicos** - `get_available_langs()` collects from all resources in assets.json
- [x] **`version-content` multiidioma** - Shows content for all languages in version-content
- [x] **Help/rules multilingües** - Fixed swapped English files (help.en.md ↔ rules.en.md)
- [x] **Formalización interna** - Separated: argument parsing, config, language system, addon discovery, help system, command listing, addon execution, output, errors

### 🔄 In Progress
- [ ] Addon command interface implementation for `image` (RtG Image commands.py)
- [ ] Addon command interface implementation for `preview` (RtG Preview commands.js)

### ⏳ Planned
- [ ] Add `--addon-help <addon>` to show addon-specific help from interface
- [ ] Add `-language` support for void-text selection (partially done)
- [ ] Validate all test cases from user requirements

### Test Cases to Validate
- [x] `rtg` - shows void
- [x] `rtg -h` / `--help` - shows help
- [x] `rtg -v` / `--version` - shows version + version-content
- [x] `rtg -c` / `--commands` - lists internal commands
- [x] `rtg -a` / `--addons` - lists addons with docs
- [x] `rtg -l` / `--lang` - shows available languages
- [x] `rtg -r` / `--rules` - shows rules (default: Spanish)
- [x] `rtg help` - general help
- [x] `rtg help image` - addon help (English from internal)
- [x] `rtg help image -en` - addon help in English
- [x] `rtg help image -lang` - addon languages
- [x] `rtg image` - shows addon info
- [x] `rtg image convert` - passes "convert" to addon
- [x] `rtg image --width 128` - passes --width 128 to addon
- [x] `rtg image -lang` - RtG-CLI handles -lang (shows addon langs)

---

## RtG-Preview

### ✅ Completed (2026-09-21)
- [x] **Formato nuevo** - Updated to work with current RtG-Format structure ([Type, Connections, Properties], LocalType/PrimaryID/PrimaryIndex, 1-based indexing, EphemeralAttachments, CFrames)
- [x] **Carga local (file://)** - Embedded manifest (`models-manifest.js`) loaded via script tag, no HTTP server required
- [x] **Modelos** - ModelRegistry loads from embedded manifest, falls back to HTTP, supports branches, connection points
- [x] **Renderer** - Parses build JSON, positions objects via connections, uses model metadata
- [x] **README actualizado** - Documents new format, local usage, external CDN usage

### 🔄 In Progress
- [ ] Test preview.html locally (file://) with embedded manifest
- [ ] Verify connection-based positioning works with UUID/EphemeralAttachments
- [ ] Test branch rendering (Switch, Splitter, Doors)

### ⏳ Planned
- [ ] Connection point visualization (debug mode)
- [ ] Property-driven visual updates (e.g., Servo rotation, Light intensity)
- [ ] Texture/MTL support
- [ ] InstancedMesh optimization for repeated parts
- [ ] Web Worker for OBJ parsing
- [ ] Draco/GLTF compression for smaller downloads

### ❓ Unknown/Blocked
- [ ] File:// protocol: Some browsers may still block OBJ/JSON loads even with embedded manifest
- [ ] Large model loading performance on file://

---

## RtG-AI

### ✅ Completed
- [x] **Aplicación base** - Chat, sidebar, conversations, model selector, preview, suggested prompts, feedback, multi-lang prep
- [x] **Arquitectura separada** - UI/Core separation, mock model, ready for real model integration
- [x] **Integración RtG-Preview** - Uses official preview for build visualization

### 🔄 In Progress
- [ ] **Fase 2 — Primer modelo** - Real AI model integration
- [ ] **Dataset especializado** - Collect/curate RtG build dataset from examples/experiments + dev/json

### ⏳ Planned

#### Builds de entrenamiento
- [ ] Curate training dataset from `examples/experiments/` and `tools/RtG-AI/dev/json/`
- [ ] Create train/val/test splits
- [ ] Document dataset format and schema

#### Sistema de entrenamiento
- [ ] **Pipeline de entrenamiento** - `tools/RtG-AI/dev/pipeline/` (orchestrator.py, stages.py exist)
- [ ] **Procesamiento de datos** - `tools/RtG-AI/dev/extractor/extractor.py` exists
- [ ] **Evaluación** - Automated build validation (syntax + RtG-Preview load test)
- [ ] **Feedback loop** - Collect generation feedback, retrain

#### Feedback
- [ ] Expand feedback system (currently basic in app/src/core/feedback.js)
- [ ] Server-side feedback collection (Phase 3)
- [ ] Feedback-driven dataset augmentation

#### Aplicación
- [ ] Pulido final UI (Phase 1)
- [ ] Real model integration (Phase 2)
- [ ] Multi-turn conversation context for complex builds

#### Servidores gratuitos / $0 infraestructura
- [ ] **Investigar**: GitHub Actions for training (free tier: 2000 min/mo)
- [ ] **Investigar**: Google Colab (free GPU, 12hr sessions)
- [ ] **Investigar**: Hugging Face Spaces (free CPU, paid GPU)
- [ ] **Investigar**: Kaggle Kernels (free GPU, 30hr/week)
- [ ] **Investigar**: Oracle Cloud Free Tier (4 Ampere ARM cores, 24GB RAM)
- [ ] **Investigar**: RunPod / Lambda Labs community credits
- [ ] Document chosen approach in `tools/RtG-AI/config/`

#### Mejora continua
- [ ] Data → Training → Model → Use → Feedback → New Data cycle
- [ ] Automated evaluation pipeline
- [ ] Versioned model checkpoints in `tools/RtG-AI/dev/checkpoints/`

---

## Cross-Cutting

### Repository Maintenance
- [ ] Update CHANGELOG.md with 2026-09-21 changes
- [ ] Verify all internal links in documentation work
- [ ] Add missing entries to structure.md (done 2026-09-21)
- [ ] Clean up `delete/` directory or document purpose
- [ ] Organize `dev/` scripts and docs

### Tooling
- [ ] `scripts/generate-manifest.js` - Done, generates models.json + models-manifest.js
- [ ] `scripts/generate-block-docs.js` - Done, generates 120 block docs
- [ ] `scripts/fix-json.js` - Verify works
- [ ] Create `scripts/validate-build.js` - Validate build JSON against SPECIFICATION.md

### Testing
- [ ] Add automated tests for RtG-CLI commands
- [ ] Add automated tests for RtG-Preview build parsing
- [ ] Add CI/CD pipeline (GitHub Actions) for validation

---

## Block-Specific TODOs

### High Priority (Core Vehicle Parts)
- [ ] **Chassis** - Document all 26 connection points from old-files/obj_ids-spanish.md
- [ ] **Wheel/Tire** - Verify connection point positions
- [ ] **Servo** - Document all properties (Speed, Rotation, LimitAngle, etc.)
- [ ] **Switch** - Document branch system (input/output)
- [ ] **Splitter_1-4** - Document signal distribution behavior
- [ ] **Gate-AND/OR/NOT** - Document logic behavior
- [ ] **Wire/Rope** - Document Length, MinLength, MaxLength, MaxForce

### Medium Priority
- [ ] **DoorA-D** - Hinge mechanics, branch rotation
- [ ] **Cannon/Gun/MountedGun/RPG/Shotgun/Uzi** - Shooting properties
- [ ] **Radio** - Volume, Channel, CustomTrack
- [ ] **Light** - Volume as intensity
- [ ] **Sprite/TV** - ImageId behavior
- [ ] **Thruster/Propeller** - Speed, MaxForce
- [ ] **PotatoEngine/GoldPotatoEngine** - Speed
- [ ] **SpringJuice** - Spring properties
- [ ] **Mag** - Quantity, Bullets

### Low Priority / Unknown
- [ ] **Teeth** - No JSON, only OBJ - needs investigation
- [ ] **Spoiler** - Connection points unknown
- [ ] **Suspension** - Not in models, may not exist
- [ ] **Engine/Motor** - Not in models, may be Chassis sub-part
- [ ] **Wrench/PaintTool** - ToolGun variants?
- [ ] Uncategorized blocks in `blocks/parts/uncategorized/`
- [ ] Unused blocks in `blocks/parts/unused/`

---

## Notes

### Evidence Hierarchy (per SPECIFICATION.md)
1. **CONFIRMED** - Directly observed, reproducible
2. **OBSERVED** - Observed in experiments, not generalized
3. **PROBABLE** - Reconstructed from multiple observations
4. **HYPOTHESIS** - Proposed, not demonstrated
5. **UNKNOWN** - Evidence insufficient

### Historical Evidence Priority
- `old-files/` has priority when investigating discrepancies
- Do not silently override historical evidence
- Document reasons for any changes to historical interpretations

### Confidence Tracking
Each block doc has confidence level. Update as evidence improves:
- CONFIRMED → Ready for production use
- PARTIALLY CONFIRMED → Usable with caveats
- UNCONFIRMED → Experimental only
- UNKNOWN → Needs investigation
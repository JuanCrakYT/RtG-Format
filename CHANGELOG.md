# Changelog

## Unreleased

### Added

* Expanded and consolidated the current RtG save/build format specification.
* Added detailed documentation for:

  * JSON structure and object tuples.
  * Object indexing and parent references.
  * Connection fields and their meanings.
  * Object properties and property behavior.
  * Identifiers and UUID-based references.
  * `EphemeralAttachments` and CFrame-based spatial reconstruction.
  * Unknown and partially understood fields.
* Expanded the research documentation with methodology, discoveries, unresolved questions, and supporting evidence.
* Added and expanded research discoveries in `research/discoveries.md`.
* Expanded compression and encoding documentation.
* Added and updated reproducible examples and experimental documentation.
* Added additional documentation and organization under `blocks/`, `format/`, `research/`, `compression/`, `docs/`, `examples/`, and `assets/`.
* Added a documentation website under `page/`.
* Added GitHub Pages deployment configuration.
* Added documentation website version information (`1.0`).
* Added official RtG-Format branding, including the logo, banners, SVG assets, and rendered PNG assets.
* Added documentation guidance for agents working with the repository.

### Changed

* Improved the main README with a clearer project introduction, documentation map, quick-start paths, project status, research status, attribution, and historical-documentation guidance.
* Improved documentation structure and navigation, including beginner, technical, and research reading paths.
* Updated `structure.md` to reflect the reorganized repository structure.
* Reorganized the `examples/` directory documentation to clearly distinguish experiments, JSON examples, and preserved discarded material.
* Improved internal documentation links and references across the repository.
* Updated compression documentation to more accurately describe the encoding/compression pipeline.
* Updated the specification to better distinguish current technical documentation from historical material.
* Changed the specification status from `Experimental / Unofficial` to `Unreleased / Work in progress`.
* Updated and corrected historical and Spanish documentation where necessary.
* Updated repository metadata and ignore rules as part of the reorganization.

### Fixed

* Fixed multiple documentation and repository-structure issues.
* Fixed several recently identified bugs.
* Fixed issues involving `assets/README.md`.
* Fixed broken or incorrect internal documentation references.
* Fixed various language, formatting, and consistency issues.

### Preservation

* Preserved historical reverse-engineering material under `old-files/`.
* Preserved earlier specification versions and historical research as provenance rather than silently rewriting them.
* Kept the current consolidated documentation as the primary reference for the format.

## v0.406

* Historical research documents preserved in [`old-files/`](old-files/) (original author metadata retained in files there).

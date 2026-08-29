# Repository Structure
This document describes the current structure of the RtG-Format repository.

The tree below reflects the repository's current organization and is intended to help contributors and readers understand where documentation, research, assets, examples, tools, and website files are located.

## Text/Tree Format
```tree
RtG-Format/
│
├── README.md
├── SPECIFICATION.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── structure.md
├── assets/
│   ├─ images/
│   │  ├─ logo/
│   │  │  ├─ official-banners/
│   │  │  │  ├─ RtG-1.webp
│   │  │  │  ├─ RtG-2.webp
│   │  │  │  ├─ RtG-3.webp
│   │  │  │  ├─ RtG-4.webp
│   │  │  │  └─ RtG-5.webp
│   │  │  ├─ versions/
│   │  │  │  └─ v1/
│   │  │  │     ├─ RtG-Format-v1.png
│   │  │  │     └─ RtG-Format-v1.svg
│   │  │  ├─ RtG-Format-Background.svg
│   │  │  ├─ RtG-Format-Shape.svg
│   │  │  ├─ RtG-Format.png
│   │  │  └─ RtG-Format.svg
│   │  ├─ banner.jpeg
│   │  ├─ banner.png
│   │  └─ banner.svg
│   └─ README.md
│
├── page/
│   │
│   ├── index.html
│   │
│   ├── css/
│   │   ├── main.css
│   │   ├── layout.css
│   │   └── markdown.css
│   │
│   ├── js/
│   │   ├── app.js
│   │   ├── router.js
│   │   ├── github.js
│   │   ├── markdown.js
│   │   ├── mermaid.js
│   │   ├── base64.js
│   │   ├── navigation.js
│   │   └── utils.js
│   │
│   └── assets/
│       ├── logo.png
│       └── icons/
│
├── blocks/
│   ├── README.md
│   └── parts/
│        ├── building/
│        │    ├── imgs/
│        │    ├── parts-id.md
│        │    └── README.md
│        ├── miscellaneous/
│        │    ├── imgs/
│        │    ├── parts-id.md
│        │    └── README.md
│        ├── other/
│        │    ├── imgs/
│        │    ├── parts-id.md
│        │    └── README.md
│        ├── physics/
│        │    ├── imgs/
│        │    ├── parts-id.md
│        │    └── README.md
│        ├── tools/
│        │    ├── imgs/
│        │    ├── parts-id.md
│        │    └── README.md
│        ├── uncategorized/
│        │    ├── imgs/
│        │    ├── parts-id.md
│        │    └── README.md
│        ├── unused/
│        │    ├── imgs/
│        │    ├── parts-id.md
│        │    └── README.md
│        └── wiring/
│             ├── imgs/
│             ├── parts-id.md
│             └── README.md
│
├── format/
│   ├── README.md
│   ├── json-structure.md
│   ├── indexing.md
│   ├── properties.md
│   ├── identifiers.md
│   └── unknown-fields.md
│
├── compression/
│   ├── README.md
│   ├── overview.md
│   ├── encoding.md
│   └── examples-template.md
│
├── examples/
│   ├── README.md
│   ├── experiments/
│   │    ├── README.md
│   │    └── ...
│   ├── json-examples/
│   │    ├── README.md
│   │    └── ...
│   └── trash/
│        ├── README.md
│        └── ...
│
├── tools/
│   ├── README.md
│   └── agent/
│        ├── parts_diff.py
│        └── regenerate_parts.py
│
├── research/
│   ├── README.md
│   ├── methodology.md
│   ├── discoveries.md
│   └── unknowns.md
│
├── old-files/
│   ├── README.md
│   ├── obj_ids-spanish.md
│   └── RtG_Save_Format_Specification-spanish.md
│
└── docs/
    ├── README.md
    ├── getting-started.md
    ├── save-anatomy.md
    ├── building-system.md
    └── faq.md
```

# READ STRUCTURE

```tree
READ STRUCTURE
│
├── README.md
│   ├── # RtG Save Format — Reverse-Engineered Documentation
│   ├── ## What is RtG-Format?
│   │   └── ### What can you find here?
│   ├── ## Quick Start
│   ├── ## How the RtG Save System Works
│   ├── ## Documentation
│   │   ├── ### Format
│   │   ├── ### Blocks and Parts
│   │   ├── ### Compression and Encoding
│   │   ├── ### Examples
│   │   ├── ### Research
│   │   ├── ### Tools
│   │   └── ### Status
│   ├── ## Research Status
│   ├── ## Project Status
│   ├── ## Historical Documentation
│   ├── ## Attribution
│   ├── ## Credits
│   ├── ## Web Documentation
│   ├── ## Link Reference
│   └── ## Repository
│
├── SPECIFICATION.md
│   ├── # RtG Save Format Specification
│   ├── ## 1. Overview
│   ├── ## 2. Root Structure
│   ├── ## 3. Object Type
│   ├── ## 4. Connections
│   │   ├── ### 4.1 `LocalType`
│   │   ├── ### 4.2 `PrimaryID`
│   │   │   ├── #### Numeric connection point
│   │   │   └── #### UUID attachment reference
│   │   └── ### 4.3 `PrimaryIndex`
│   ├── ## 5. Object Ordering
│   ├── ## 6. Spatial Reconstruction
│   ├── ## 7. EphemeralAttachments
│   ├── ## 8. UUID Linking
│   ├── ## 9. Synthetic UUIDs
│   ├── ## 10. CFrame
│   ├── ## 11. Properties
│   │   └── ### 11.1 Property Categories
│   ├── ## 12. Missing Properties
│   ├── ## 13. Observed Properties
│   ├── ## 14. Loader Behavior
│   ├── ## 15. Validation and Failure Behavior
│   ├── ## 16. Coordinate and Attachment Behavior
│   ├── ## 17. Confirmed Discoveries
│   ├── ## 18. Hypotheses and Reconstructed Behavior
│   │   ├── ### 18.1 Loader Pipeline
│   │   └── ### 18.2 Sprite CFrame Behavior
│   ├── ## 19. Historical First Save (Optional)
│   ├── ## 20. Evidence and Confidence
│   │   ├── ### CONFIRMED
│   │   ├── ### OBSERVED
│   │   ├── ### PROBABLE
│   │   ├── ### HYPOTHESIS
│   │   └── ### UNKNOWN
│   └── ## 21. Related Documentation
│       └── ### Historical / Technical Reference
│
├── CHANGELOG.md
│   └── [headings]
│
├── CONTRIBUTING.md
│   └── [headings]
│
├── assets/
│   └── README.md
│       └── # Assets
│           ├── ## Directory Structure
│           ├── ## Images
│           │   ├── ### Banners
│           │   ├── ### Current RtG-Format Logo
│           │   ├── ### Official RtG Banners
│           │   └── ### Historical Logo Versions
│           ├── ## Asset Guidelines
│           └── ## Related Documentation
│
├── page/
│   └── [no Markdown structure]
│
├── blocks/
│   ├── README.md
│   │   └── [headings]
│   │
│   └── parts/
│       ├── building/
│       │   ├── README.md
│       │   │   └── [headings]
│       │   └── parts-id.md
│       │       └── [headings]
│       │
│       ├── miscellaneous/
│       │   ├── README.md
│       │   │   └── [headings]
│       │   └── parts-id.md
│       │       └── [headings]
│       │
│       ├── other/
│       │   ├── README.md
│       │   │   └── [headings]
│       │   └── parts-id.md
│       │       └── [headings]
│       │
│       ├── physics/
│       │   ├── README.md
│       │   │   └── [headings]
│       │   └── parts-id.md
│       │       └── [headings]
│       │
│       ├── tools/
│       │   ├── README.md
│       │   │   └── [headings]
│       │   └── parts-id.md
│       │       └── [headings]
│       │
│       ├── uncategorized/
│       │   ├── README.md
│       │   │   └── [headings]
│       │   └── parts-id.md
│       │       └── [headings]
│       │
│       ├── unused/
│       │   ├── README.md
│       │   │   └── [headings]
│       │   └── parts-id.md
│       │       └── [headings]
│       │
│       └── wiring/
│           ├── README.md
│           │   └── [headings]
│           └── parts-id.md
│               └── [headings]
│
├── format/
│   ├── README.md
│   │   ├── # Format Documentation
│   │   ├── ## Documents
│   │   ├── ## How These Documents Relate
│   │   ├── ## Related Documentation
│   │   └── ## Scope
│   ├── json-structure.md
│   │   └── [pending...]
│   ├── indexing.md
│   │   └── [pending...]
│   ├── properties.md
│   │   └── [pending...]
│   ├── identifiers.md
│   │   └── [pending...]
│   └── unknown-fields.md
│       └── [pending...]
│
├── compression/
│   ├── README.md
│   │   └── [pending...]
│   ├── overview.md
│   │   └── [pending...]
│   ├── encoding.md
│   │   └── [pending...]
│   └── examples-template.md
│       └── [pending...]
│
├── examples/
│   ├── README.md
│   │   └── [pending...]
│   ├── experiments/
│   │   └── README.md
│   │       └── [pending...]
│   ├── json-examples/
│   │   └── README.md
│   │       └── [pending...]
│   └── trash/
│       └── README.md
│           └── [pending...]
│
├── tools/
│   └── README.md
│       └── [pending...]
│
├── research/
│   ├── README.md
│   │   └── [pending...]
│   ├── methodology.md
│   │   └── [pending...]
│   ├── discoveries.md
│   │   └── [pending...]
│   └── unknowns.md
│       └── [pending...]
│
├── old-files/
│   ├── README.md
│   │   └── [headings]
│   ├── obj_ids-spanish.md
│   │   └── [headings]
│   └── RtG_Save_Format_Specification-spanish.md
│       └── [headings]
│
└── docs/
    ├── README.md
    │   ├── # Documentation
    │   └── ## Start Here
    │
    ├── getting-started.md
    │   ├── # Getting Started
    │   ├── ## Recommended Reading Order
    │   ├── ## After the Basics
    │   ├── ## Contributing
    │   └── ## Important Distinction
    │
    ├── save-anatomy.md
    │   ├── # Save Anatomy
    │   ├── ## Basic Structure
    │   │   ├── ### Type
    │   │   ├── ### Connections
    │   │   └── ### Properties
    │   ├── ## Object Relationships
    │   ├── ## Attachments and UUIDs
    │   ├── ## Encoding
    │   └── ## Where to Continue
    │
    ├── building-system.md
    │   ├── # Building System
    │   ├── ## Main Concepts
    │   ├── ## Parts and Object IDs
    │   ├── ## Format Representation
    │   ├── ## Attachments and Spatial Data
    │   └── ## Important Distinction
    │
    └── faq.md
        ├── # FAQ
        ├── ## What is this repository?
        ├── ## What is the current source of truth?
        ├── ## Why are there historical files?
        ├── ## Where are the Part IDs?
        ├── ## Where are the experiments?
        ├── ## Can I add an example JSON file?
        ├── ## Can experiments be deleted?
        ├── ## Where is encoding and compression documented?
        ├── ## Where are the tools?
        └── ## Is the project affiliated with Road To Gramby's?
```

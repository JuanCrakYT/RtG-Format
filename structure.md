# Structure

# Text/Tree format:
```tree
rtg-save-format/
│
├── README.md
├── SPECIFICATION.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
│
├── blocks/
│   ├── README.md
│   └── parts/
│        ├── building/
│        │    ├── parts-id.md
│        │    └── README.md
│        ├── miscellaneous/
│        │    ├── parts-id.md
│        │    └── README.md
│        ├── other/
│        │    ├── parts-id.md
│        │    └── README.md
│        ├── physics/
│        │    ├── parts-id.md
│        │    └── README.md
│        ├── tools/
│        │    ├── parts-id.md
│        │    └── README.md
│        ├── uncategorized/
│        │    ├── parts-id.md
│        │    └── README.md
│        ├── unused/
│        │    ├── parts-id.md
│        │    └── README.md
│        └── wiring/
│             ├── parts-id.md
│             └── README.md
│
├── format/
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
│        └── README.md
│
├── tools/
│   ├── README.md
│   └── agent/
│        ├── parts_diff.py
│        └── regenerate_parts.py
│
├── research/
│   ├── methodology.md
│   ├── discoveries.md
│   └── unknowns.md
│
├── old-files/
│   ├── structure.md
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

## Mermaid format

```mermaid
flowchart TD
    ROOT["📁 rtg-save-format"]

    ROOT --> ROOT_DOCS["📄 README.md"]
    ROOT --> SPEC["📄 SPECIFICATION.md"]
    ROOT --> CHANGELOG["📄 CHANGELOG.md"]
    ROOT --> CONTRIBUTING["📄 CONTRIBUTING.md"]
    ROOT --> LICENSE["📄 LICENSE"]

    ROOT --> BLOCKS["📁 blocks"]
    BLOCKS --> BLOCKS_README["📄 README.md"]
    BLOCKS --> PARTS["📁 parts"]

    PARTS --> BUILDING["📁 building"]
    PARTS --> MISC["📁 miscellaneous"]
    PARTS --> OTHER["📁 other"]
    PARTS --> PHYSICS["📁 physics"]
    PARTS --> TOOLS_PARTS["📁 tools"]
    PARTS --> UNCATEGORIZED["📁 uncategorized"]
    PARTS --> UNUSED["📁 unused"]
    PARTS --> WIRING["📁 wiring"]

    BUILDING --> BUILDING_ID["📄 parts-id.md"]
    BUILDING --> BUILDING_README["📄 README.md"]

    MISC --> MISC_ID["📄 parts-id.md"]
    MISC --> MISC_README["📄 README.md"]

    OTHER --> OTHER_ID["📄 parts-id.md"]
    OTHER --> OTHER_README["📄 README.md"]

    PHYSICS --> PHYSICS_ID["📄 parts-id.md"]
    PHYSICS --> PHYSICS_README["📄 README.md"]

    TOOLS_PARTS --> TOOLS_PARTS_ID["📄 parts-id.md"]
    TOOLS_PARTS --> TOOLS_PARTS_README["📄 README.md"]

    UNCATEGORIZED --> UNCATEGORIZED_ID["📄 parts-id.md"]
    UNCATEGORIZED --> UNCATEGORIZED_README["📄 README.md"]

    UNUSED --> UNUSED_ID["📄 parts-id.md"]
    UNUSED --> UNUSED_README["📄 README.md"]

    WIRING --> WIRING_ID["📄 parts-id.md"]
    WIRING --> WIRING_README["📄 README.md"]

    ROOT --> FORMAT["📁 format"]
    FORMAT --> JSON["📄 json-structure.md"]
    FORMAT --> INDEXING["📄 indexing.md"]
    FORMAT --> PROPERTIES["📄 properties.md"]
    FORMAT --> IDENTIFIERS["📄 identifiers.md"]
    FORMAT --> UNKNOWN["📄 unknown-fields.md"]

    ROOT --> COMPRESSION["📁 compression"]
    COMPRESSION --> COMP_README["📄 README.md"]
    COMPRESSION --> OVERVIEW["📄 overview.md"]
    COMPRESSION --> ENCODING["📄 encoding.md"]
    COMPRESSION --> EXAMPLES_TEMPLATE["📄 examples-template.md"]

    ROOT --> EXAMPLES["📁 examples"]
    EXAMPLES --> EXAMPLES_README["📄 README.md"]
    EXAMPLES --> EXPERIMENTS["📁 experiments"]
    EXAMPLES --> JSON_EXAMPLES["📁 json-examples"]
    EXAMPLES --> TRASH["📁 trash"]

    EXPERIMENTS --> EXP_README["📄 README.md"]
    EXPERIMENTS --> EXP_OTHER["📄 ..."]

    JSON_EXAMPLES --> JSON_EXP_README["📄 README.md"]
    JSON_EXAMPLES --> JSON_EXP_OTHER["📄 ..."]

    TRASH --> TRASH_README["📄 README.md"]

    ROOT --> TOOLS["📁 tools"]
    TOOLS --> TOOLS_README["📄 README.md"]
    TOOLS --> AGENT["📁 agent"]
    AGENT --> PARTS_DIFF["🐍 parts_diff.py"]
    AGENT --> REGENERATE["🐍 regenerate_parts.py"]

    ROOT --> RESEARCH["📁 research"]
    RESEARCH --> METHODOLOGY["📄 methodology.md"]
    RESEARCH --> DISCOVERIES["📄 discoveries.md"]
    RESEARCH --> UNKNOWNS["📄 unknowns.md"]

    ROOT --> OLD["📁 old-files"]
    OLD --> OLD_STRUCTURE["📄 structure.md"]
    OLD --> SPANISH_IDS["📄 obj_ids-spanish.md"]
    OLD --> SPANISH_SPEC["📄 RtG_Save_Format_Specification-spanish.md"]

    ROOT --> DOCS["📁 docs"]
    DOCS --> DOCS_README["📄 README.md"]
    DOCS --> GETTING_STARTED["📄 getting-started.md"]
    DOCS --> SAVE_ANATOMY["📄 save-anatomy.md"]
    DOCS --> BUILDING_SYSTEM["📄 building-system.md"]
    DOCS --> FAQ["📄 faq.md"]

    classDef root fill:#4a5568,color:#ffffff,stroke:#2d3748,stroke-width:3px;
    classDef folder fill:#2b6cb0,color:#ffffff,stroke:#2c5282,stroke-width:2px;
    classDef file fill:#edf2f7,color:#1a202c,stroke:#a0aec0;
    classDef python fill:#fefcbf,color:#744210,stroke:#d69e2e;

    class ROOT root;

    class BLOCKS,PARTS,BUILDING,MISC,OTHER,PHYSICS,TOOLS_PARTS folder;
    class UNCATEGORIZED,UNUSED,WIRING,FORMAT,COMPRESSION folder;
    class EXAMPLES,EXPERIMENTS,JSON_EXAMPLES,TRASH folder;
    class TOOLS,AGENT,RESEARCH,OLD,DOCS folder;

    class ROOT_DOCS,SPEC,CHANGELOG,CONTRIBUTING,LICENSE file;
    class BLOCKS_README,BUILDING_ID,BUILDING_README file;
    class MISC_ID,MISC_README,OTHER_ID,OTHER_README file;
    class PHYSICS_ID,PHYSICS_README,TOOLS_PARTS_ID,TOOLS_PARTS_README file;
    class UNCATEGORIZED_ID,UNCATEGORIZED_README file;
    class UNUSED_ID,UNUSED_README,WIRING_ID,WIRING_README file;
    class JSON,INDEXING,PROPERTIES,IDENTIFIERS,UNKNOWN file;
    class COMP_README,OVERVIEW,ENCODING,EXAMPLES_TEMPLATE file;
    class EXAMPLES_README,EXP_README,EXP_OTHER file;
    class JSON_EXP_README,JSON_EXP_OTHER,TRASH_README file;
    class TOOLS_README,METHODOLOGY,DISCOVERIES,UNKNOWNS file;
    class OLD_STRUCTURE,SPANISH_IDS,SPANISH_SPEC file;
    class DOCS_README,GETTING_STARTED,SAVE_ANATOMY,BUILDING_SYSTEM,FAQ file;

    class PARTS_DIFF,REGENERATE python;
```
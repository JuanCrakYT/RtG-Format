# Experiments

This folder is intended to hold real save experiments and curated minimal builds used for tests and demonstrations.

Rules
- Do NOT create or add fabricated saves. Only include JSON files with provenance and evidence.
- If an experiment can't be loaded, add a `README.md` and explain why
- The experiments can't be deleted, instead, move experiment folder to: `examples/trash/`
- All the experiments need a folder on `examples/experiments/` with this structure:
```tree
<name>/
│
├── README.md
├── objective.md
├── example.json (no notes, add notes on `objective.md` or `README.md`)
└── other/
    ├── README.md
    └── ...
```
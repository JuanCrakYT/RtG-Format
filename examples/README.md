# Examples and Experiments Folder

This folder is intended to hold real save experiments, examples and curated minimal builds used for tests and demonstrations.

Rules
- Do NOT create or add fabricated saves. Only include JSON files with provenance and evidence.
- If an experiment doesn't work (load error), on the `README.md` explain why (that `README.md` contains the results after load with an error) or delete that experiment folder.
- All the experiments need a folder on `examples/experiments/` with this structure:
```tree
<name>/
│
├── README.md
├── objetive.md
├── example.json (no notes, add notes on `objetive.md` or `README.md`)
└── other/
    ├── README.md
    └── ...
```
- All the examples need a folder on `examples/json-examples/` with this structure:
```tree
<name>/
│
├── README.md
├── example.json (no notes, add notes on `README.md`)
└── images-videos/
    ├── presentation.png
    └── ...
```
- The videos in the examples can't last more than 30 seconds
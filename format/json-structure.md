# JSON structure (observed)

Status: Partially documented

Confirmed observations
- Top-level: JSON Array. Each element is a 3-element tuple: `[Type, Connections, Properties]` (CONFIRMED).
- `Type`: String identifier of the object template (e.g. `"Part"`, `"Sprite"`, `"Chassis"`) (OBSERVED).
- `Connections`: Array of 0..N connection tuples. Each connection tuple is `[TipoLocal, PuntoPadre, ÍndicePadre]` (CONFIRMED).
- `Properties`: Open dictionary of key -> value pairs; unknown keys are tolerated (CONFIRMED).

Example (historic observation):
```
[
  ["Base", [], {}],
  ["Part", [["1","5",1]], {"RGB":[255,0,0]}]
]
```

Guidance
- Do not assume additional wrapper metadata unless observed.
- Document any deviations here with source evidence.

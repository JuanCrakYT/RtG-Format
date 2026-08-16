# Unused Parts — Notes from Wiki

> Source: Road to Gramby's Wiki (wiki-only notes). Historical file preserved in `old-files/obj_ids-spanish.md` — entries may be present there; check original.

The wiki lists the following as unused parts. These are noted here but not assumed as part of the active format.

| Name              | Wiki Data                      | Status             | Notes                                                                                      |
| ----------------- | ------------------------------ | ------------------ | ------------------------------------------------------------------------------------------ |
| Body              | Base64 sharecode shown on wiki | UNCONFIRMED (wiki) | Source: Road to Gramby's Wiki; see `old-files/obj_ids-spanish.md` for historical mentions. |
| Fricklet          | Base64 sharecode shown on wiki | UNCONFIRMED (wiki) | Source: Road to Gramby's Wiki.                                                             |
| Super Power Clock | Base64 sharecode shown on wiki | UNCONFIRMED (wiki) | Source: Road to Gramby's Wiki.                                                             |

Source evidence: Road to Gramby's Wiki; treat as wiki-only unless `old-files/obj_ids-spanish.md` contains explicit IDs.

# Data
The wiki contains the Base64 sharecode:
```text
WyJCb2R5IiwgW10sIFtdXQ==
WyJGcmlja2xldCIsIFtdLCBbXV0=
WyJTdXBlclBvd2VyQ2xvY2siLCBbXSwgW11d
```
Or as individual entries:
```json
["Body", [], []]
["Fricklet", [], []]
["SuperPowerClock", [], []]
```
Joined:
```json
[
  ["Body", [], []],
  ["Fricklet", [], []],
  ["SuperPowerClock", [], []]
]
```
> **Warning:** When encoding as `Base64`, do not include spaces; use a single line instead. Example:
```json
[["Body", [], []],["Fricklet", [], []],["SuperPowerClock", [], []]]
```
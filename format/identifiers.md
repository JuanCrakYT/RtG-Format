# Identifiers

This file collects object type identifiers and other ID systems (connection point IDs, UUIDs).

Guidelines
- Do not invent mappings between numeric IDs and semantic names. When an ID is historical-only, mark it `UNCONFIRMED` and point to `old-files/obj_ids-spanish.md`.

UUID behavior (summary)
- UUIDs are used as keys for `EphemeralAttachments` and as connection references inside `Connections` tuples (CONFIRMED).

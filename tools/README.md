# Agent Tools

This directory contains automation tools used to maintain and validate repository data.
These tools are intended for repository maintenance and migration tasks. They are **not required to understand or use the RtG save/build format**.

## Tools

### `parts_diff.py`

**Status:** Incomplete / Postponed

Tool for comparing part/object data during repository maintenance.
It is currently not part of the active documentation workflow.

### `regenerate_parts.py`

**Status:** Incomplete / Postponed

Tool intended to regenerate or update organized part data from repository sources.
It is currently not part of the active documentation workflow.

## Migration Data

### `migration_diff.json`

`migration_diff.json` is a generated verification report associated with the migration of historical object/connection-point data into the current organized references.
It records the source used for the migration and compares the historical and migrated data.

Example:

```json
{
  "source": "old-files/obj_ids-spanish.md",
  "counts": {
    "historical_sections": 44,
    "historical_rows": 105,
    "migrated_rows": 105,
    "historical_no_point_objects": 62
  },
  "missing_rows": [],
  "extra_rows": [],
  "historical_duplicate_rows": 0,
  "migrated_duplicate_rows": 0,
  "historical_files_modified": 0,
  "invented_rows": 0
}
```

### Report Fields

| Field                                | Meaning                                                                   |
| ------------------------------------ | ------------------------------------------------------------------------- |
| `source`                             | Historical file used as the migration source.                             |
| `counts.historical_sections`         | Number of sections found in the historical source.                        |
| `counts.historical_rows`             | Number of historical rows detected.                                       |
| `counts.migrated_rows`               | Number of rows present in the migrated data.                              |
| `counts.historical_no_point_objects` | Historical objects without an associated connection point.                |
| `missing_rows`                       | Rows present historically but missing from the migrated data.             |
| `extra_rows`                         | Rows present in the migrated data but not found in the historical source. |
| `historical_duplicate_rows`          | Duplicate rows detected in the historical source.                         |
| `migrated_duplicate_rows`            | Duplicate rows detected in the migrated data.                             |
| `historical_files_modified`          | Number of historical source files modified during the migration.          |
| `invented_rows`                      | Rows introduced without corresponding historical source data.             |

An empty `missing_rows`, `extra_rows`, and `invented_rows` list indicates that the migration did not report missing, additional, or invented rows.

## Important

`migration_diff.json` is **verification data**, not a specification of the RtG save/build format.

The historical source remains preserved under [`../../old-files/`](../../old-files/), while the current organized object references are maintained under [`../../blocks/`](../../blocks/).
Because the associated agent tools are incomplete/postponed, this directory should not be treated as a primary entry point for understanding the format.

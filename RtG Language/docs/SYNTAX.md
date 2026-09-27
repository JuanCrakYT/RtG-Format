# Syntax

An RtG-Language source starts with `rtg 2.0;`. It may declare `schema`, one or more `object` sections, and `output`. Objects contain `properties`, `attachment`, `instance`, and `connect` declarations. Connections use `connect child -> parent { localType: N; point: N|uuid("..."); }`.

# Schema contract

`schema.json` defines the envelope for project-supplied metadata. It is not an authoritative list of RtG-Format blocks, properties, `localType` values, or connection points. Those values must come from verified observations or another declared source of truth.

The initial compiler will load this metadata before validating instances and connections. Until that loader exists, this file remains deliberately generic.

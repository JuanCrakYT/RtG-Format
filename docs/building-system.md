# Building System

This document explains how the RtG building system relates to the serialized RtG save/build format.

The building system creates objects, connections, properties, and spatial relationships that are later represented in the save data.

## Main Concepts

The format is primarily concerned with:

- Objects and Parts
- Object IDs
- Connection points
- Parent references
- Properties
- UUIDs
- `EphemeralAttachments`
- CFrame data

These concepts are documented in more detail throughout the repository.

## Parts and Object IDs

See [`../blocks/`](../blocks/) for the organized Part documentation and object ID references.

The historical ID research is preserved in:

[`../old-files/obj_ids-spanish.md`](../old-files/obj_ids-spanish.md)

The current organized Part reference is:

[`../blocks/parts/parts-id.md`](../blocks/parts/parts-id.md)

## Format Representation

The serialized object structure is documented under:

- [`../format/json-structure.md`](../format/json-structure.md)
- [`../format/indexing.md`](../format/indexing.md)
- [`../format/properties.md`](../format/properties.md)
- [`../format/identifiers.md`](../format/identifiers.md)

The consolidated technical reference is [`../SPECIFICATION.md`](../SPECIFICATION.md).

## Attachments and Spatial Data

RtG can use object references, UUIDs, `EphemeralAttachments`, and CFrame data to represent spatial relationships.

See:

- [`../format/identifiers.md`](../format/identifiers.md)
- [`../research/discoveries.md`](../research/discoveries.md)
- [`../old-files/RtG_Save_Format_Specification-spanish.md`](../old-files/RtG_Save_Format_Specification-spanish.md)

## Important Distinction

The building system describes how objects are created and connected in the game.

The RtG save/build format describes how those objects and relationships are serialized.

Do not assume that a behavior visible in the building system is automatically part of the RtG save/build format unless it is supported by evidence.

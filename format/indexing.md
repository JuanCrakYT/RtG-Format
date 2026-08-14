# Indexing

Confirmed
- RtG uses positional indices within the top-level JSON array to reference parent objects (CONFIRMED).
- The array order is significant; reordering elements breaks references (CONFIRMED).

Important note
- Historical documents indicate usage of indices starting from `1` in some descriptions; however evidence within saved JSON examples uses zero-based numeric positions in the array samples. Treat indexing carefully during verification: mark any indexing convention as `CONFIRMED` only when derived from a raw save file.

References
- See `old-files/RtG_Save_Format_Specification-spanish.md` and `research/discoveries.md` for contextual evidence.

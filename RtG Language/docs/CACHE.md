# Cache

Each project may have one optional, regenerable `.rtgcache` file. It is not a directory and is shared by the project's `.rtg` files. Its future invalidation inputs include source hashes, schema hash, compiler version, and cache format version. Deleting it must remain safe.

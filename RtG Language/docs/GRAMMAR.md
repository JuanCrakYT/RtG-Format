# Grammar

```text
file = header, schema?, object*, output?;
header = "rtg", version, ";";
instance = "instance", string, "as", identifier, property_block?, ";";
connection = "connect", identifier, "->", identifier, "{", "localType", ":", integer, ";", "point", ":", (integer | "uuid", "(", uuid, ")"), ";", "}";
attachment = "attachment", uuid, "on", identifier, "{", "partName", ":", string, ";", "cframe", ":", number_array, ";", "}";
```

The full normative grammar is maintained in `README.md`.

# Compiler

The planned pipeline is lexer → parser/AST → resolver → compiler → RtG-Format. The resolver will validate identifiers, schema metadata, connections, properties and attachments before the compiler emits a JSON build. This package currently defines only its module boundaries; it does not compile source yet.

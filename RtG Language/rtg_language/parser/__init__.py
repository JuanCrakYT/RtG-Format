"""Parser for RtG-Language 2.0."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional
from pathlib import Path

from ..lexer import Token, TokenType, tokenize
from .ast import (
    File, SchemaDecl, ObjectDecl, PropertiesDecl,
    AttachmentDecl, InstanceDecl, ConnectionDecl, OutputDecl,
)
from ..diagnostics import (
    DiagnosticCollector,
    Codes,
    SourceLocation,
    Severity,
    make_diagnostic,
)


class ParseError(Exception):
    """Exception raised during parsing with diagnostic information."""
    def __init__(self, diagnostic: DiagnosticCollector):
        self.diagnostic = diagnostic
        super().__init__(str(diagnostic))


@dataclass
class TokenStream:
    """Token stream with lookahead capability."""
    tokens: list[Token]
    position: int = 0

    def peek(self, offset: int = 0) -> Token:
        idx = self.position + offset
        if idx < len(self.tokens):
            return self.tokens[idx]
        return self.tokens[-1]  # EOF token

    def advance(self) -> Token:
        token = self.peek()
        if token.type != TokenType.EOF:
            self.position += 1
        return token

    def expect(self, *types: TokenType) -> Token:
        token = self.peek()
        if token.type in types:
            return self.advance()
        expected = " or ".join(t.value for t in types)
        raise self._make_error(
            Codes.PARSE_EXPECTED_TOKEN,
            f"Expected {expected}, got {token.type.value}",
            token.location,
        )

    def expect_value(self, token_type: TokenType) -> Any:
        token = self.expect(token_type)
        return token.value

    def check(self, *types: TokenType) -> bool:
        return self.peek().type in types

    def match(self, *types: TokenType) -> bool:
        if self.check(*types):
            self.advance()
            return True
        return False

    def _make_error(self, code: str, message: str, location: SourceLocation) -> ParseError:
        collector = DiagnosticCollector()
        collector.add(make_diagnostic(code, message, Severity.ERROR, location))
        return ParseError(collector)

    def synchronize(self, *sync_types: TokenType) -> None:
        """Synchronize to next statement after error."""
        while not self.check(TokenType.EOF):
            if self.peek().type in sync_types:
                return
            if self.peek(-1).type == TokenType.SEMICOLON:
                return
            self.advance()

    def skip_newlines(self) -> None:
        """Skip NEWLINE tokens."""
        while self.check(TokenType.NEWLINE):
            self.advance()


class Parser:
    """Recursive descent parser for RtG-Language."""

    def __init__(self, tokens: list[Token], source: str, file: str):
        self.stream = TokenStream(tokens)
        self.source = source
        self.file = file
        self.diagnostics = DiagnosticCollector()

    def parse(self) -> tuple[Optional[File], DiagnosticCollector]:
        """Parse the token stream into an AST."""
        try:
            ast = self._parse_file()
            if self.diagnostics.has_errors():
                return None, self.diagnostics
            return ast, self.diagnostics
        except ParseError as e:
            self.diagnostics.diagnostics.extend(e.diagnostic.diagnostics)
            return None, self.diagnostics

    def _parse_file(self) -> File:
        # Skip leading newlines
        self.stream.skip_newlines()
        
        # Parse header: rtg 2.0;
        self.stream.expect(TokenType.RTG)
        version_token = self.stream.expect(TokenType.STRING, TokenType.NUMBER)
        version = str(version_token.value)
        self.stream.expect(TokenType.SEMICOLON)
        self.stream.skip_newlines()

        # Optional schema
        schema = None
        if self.stream.match(TokenType.SCHEMA):
            schema = self._parse_schema()
        self.stream.skip_newlines()

        # Zero or more objects
        objects = []
        while self.stream.match(TokenType.OBJECT):
            objects.append(self._parse_object())
            self.stream.skip_newlines()

        # Optional output
        output = None
        if self.stream.match(TokenType.OUTPUT):
            output = self._parse_output()

        self.stream.skip_newlines()
        self.stream.expect(TokenType.EOF)

        return File(
            version=version,
            schema=schema,
            objects=tuple(objects),
            output=output,
            location=SourceLocation(self.file, 1, 1, 0),
        )

    def _parse_schema(self) -> SchemaDecl:
        start_loc = self.stream.peek().location
        self.stream.expect(TokenType.LBRACE)
        self.stream.expect(TokenType.SOURCE)
        self.stream.expect(TokenType.COLON)
        source = self.stream.expect_value(TokenType.STRING)
        self.stream.expect(TokenType.SEMICOLON)
        self.stream.expect(TokenType.RBRACE)
        return SchemaDecl(source=source, location=start_loc)

    def _parse_object(self) -> ObjectDecl:
        start_loc = self.stream.peek().location
        name = self.stream.expect_value(TokenType.STRING)
        self.stream.expect(TokenType.LBRACE)
        self.stream.skip_newlines()

        properties = None
        attachments = []
        instances = []
        connections = []

        while not self.stream.check(TokenType.RBRACE, TokenType.EOF):
            self.stream.skip_newlines()
            
            # Check for closing brace explicitly
            if self.stream.check(TokenType.RBRACE):
                break
                
            if self.stream.match(TokenType.PROPERTIES):
                properties = self._parse_properties()
            elif self.stream.match(TokenType.ATTACHMENT):
                attachments.append(self._parse_attachment())
            elif self.stream.match(TokenType.INSTANCE):
                instances.append(self._parse_instance())
            elif self.stream.match(TokenType.CONNECT):
                connections.append(self._parse_connection())
            else:
                token = self.stream.peek()
                self.diagnostics.add(make_diagnostic(
                    Codes.PARSE_UNEXPECTED_TOKEN,
                    f"Unexpected token in object: {token.type.value}",
                    Severity.ERROR,
                    token.location,
                    ("Expected: properties, attachment, instance, or connect",)
                ))
                self.stream.advance()
            
            # Consume optional trailing semicolon after each block
            self.stream.skip_newlines()
            self.stream.match(TokenType.SEMICOLON)

        self.stream.skip_newlines()
        self.stream.expect(TokenType.RBRACE)

        return ObjectDecl(
            name=name,
            properties=properties,
            attachments=tuple(attachments),
            instances=tuple(instances),
            connections=tuple(connections),
            location=start_loc,
        )

    def _parse_properties(self, expect_semicolon: bool = True) -> PropertiesDecl:
        start_loc = self.stream.peek().location
        self.stream.expect(TokenType.LBRACE)
        props: dict[str, Any] = {}

        while not self.stream.check(TokenType.RBRACE, TokenType.EOF):
            # Property key must be a string
            key_token = self.stream.expect(TokenType.STRING)
            key = key_token.value
            self.stream.expect(TokenType.COLON)
            value = self._parse_json_value()
            props[key] = value

            # Accept both COMMA and SEMICOLON as separators
            if not (self.stream.match(TokenType.COMMA) or self.stream.match(TokenType.SEMICOLON)):
                break

        self.stream.expect(TokenType.RBRACE)
        if expect_semicolon:
            self.stream.skip_newlines()
            # Make trailing semicolon optional
            self.stream.match(TokenType.SEMICOLON)

        return PropertiesDecl(properties=props, location=start_loc)

    def _parse_json_value(self) -> Any:
        """Parse a JSON-like value (string, number, bool, null, array, object)."""
        token = self.stream.peek()

        if token.type == TokenType.STRING:
            return self.stream.advance().value
        elif token.type == TokenType.NUMBER:
            return self.stream.advance().value
        elif token.type == TokenType.IDENTIFIER:
            ident = self.stream.advance().value
            if ident == "true":
                return True
            elif ident == "false":
                return False
            elif ident == "null":
                return None
            else:
                self.diagnostics.add(make_diagnostic(
                    Codes.PARSE_INVALID_SYNTAX,
                    f"Unexpected identifier in value: {ident}",
                    Severity.ERROR,
                    token.location,
                ))
                return None
        elif token.type == TokenType.LBRACKET:
            return self._parse_json_array()
        elif token.type == TokenType.LBRACE:
            return self._parse_json_object()
        else:
            self.diagnostics.add(make_diagnostic(
                Codes.PARSE_INVALID_SYNTAX,
                f"Unexpected token in value: {token.type.value}",
                Severity.ERROR,
                token.location,
            ))
            self.stream.advance()
            return None

    def _parse_json_array(self) -> list[Any]:
        self.stream.expect(TokenType.LBRACKET)
        values = []
        while not self.stream.check(TokenType.RBRACKET, TokenType.EOF):
            values.append(self._parse_json_value())
            if not self.stream.match(TokenType.COMMA):
                break
        self.stream.expect(TokenType.RBRACKET)
        return values

    def _parse_json_object(self) -> dict[str, Any]:
        self.stream.expect(TokenType.LBRACE)
        obj = {}
        while not self.stream.check(TokenType.RBRACE, TokenType.EOF):
            key_token = self.stream.expect(TokenType.STRING)
            self.stream.expect(TokenType.COLON)
            obj[key_token.value] = self._parse_json_value()
            if not self.stream.match(TokenType.COMMA):
                break
        self.stream.expect(TokenType.RBRACE)
        return obj

    def _parse_attachment(self) -> AttachmentDecl:
        start_loc = self.stream.peek().location
        # Accept both UUID_LITERAL and STRING for UUID
        if self.stream.check(TokenType.UUID_LITERAL):
            uuid = self.stream.expect_value(TokenType.UUID_LITERAL)
        elif self.stream.check(TokenType.STRING):
            uuid = self.stream.expect_value(TokenType.STRING)
        else:
            token = self.stream.peek()
            self.diagnostics.add(make_diagnostic(
                Codes.PARSE_INVALID_SYNTAX,
                f"Expected UUID or string for attachment, got {token.type.value}",
                Severity.ERROR,
                token.location,
            ))
            uuid = ""
        self.stream.expect(TokenType.ON)
        parent = self.stream.expect_value(TokenType.IDENTIFIER)
        self.stream.expect(TokenType.LBRACE)
        self.stream.skip_newlines()

        self.stream.expect(TokenType.PARTNAME)
        self.stream.expect(TokenType.COLON)
        part_name = self.stream.expect_value(TokenType.STRING)
        self.stream.expect(TokenType.SEMICOLON)
        self.stream.skip_newlines()

        self.stream.expect(TokenType.CFRAME)
        self.stream.expect(TokenType.COLON)
        cframe = self._parse_number_array()
        self.stream.expect(TokenType.SEMICOLON)
        self.stream.skip_newlines()

        self.stream.expect(TokenType.RBRACE)

        # Validate cframe length
        if len(cframe) != 12:
            self.diagnostics.add(make_diagnostic(
                Codes.PARSE_INVALID_CFRAME,
                f"CFrame must have exactly 12 values, got {len(cframe)}",
                Severity.ERROR,
                start_loc,
                ("Provide 12 numbers: x, y, z, r1-r9",)
            ))

        return AttachmentDecl(
            uuid=uuid,
            parent=parent,
            part_name=part_name,
            cframe=tuple(cframe),
            location=start_loc,
        )

    def _parse_number_array(self) -> list[float]:
        """Parse an array of numbers: [1, 2, 3]"""
        self.stream.expect(TokenType.LBRACKET)
        values = []
        while not self.stream.check(TokenType.RBRACKET, TokenType.EOF):
            token = self.stream.expect(TokenType.NUMBER)
            values.append(float(token.value))
            if not self.stream.match(TokenType.COMMA):
                break
        self.stream.expect(TokenType.RBRACKET)
        return values

    def _parse_instance(self) -> InstanceDecl:
        start_loc = self.stream.peek().location
        type_name = self.stream.expect_value(TokenType.STRING)
        self.stream.expect(TokenType.AS)
        identifier = self.stream.expect_value(TokenType.IDENTIFIER)

        properties = None
        if self.stream.match(TokenType.LBRACE):
            # Inline properties for this instance - could be direct properties or "properties { ... }"
            self.stream.position -= 1  # Go back to parse as properties block
            self.stream.expect(TokenType.LBRACE)
            self.stream.skip_newlines()
            
            # Check if it's a "properties" keyword block or direct properties
            if self.stream.match(TokenType.PROPERTIES):
                properties = self._parse_properties(expect_semicolon=False)
            else:
                # Direct properties: { "key": value; ... }
                self.stream.position -= 1  # Go back to start of properties
                properties = self._parse_properties(expect_semicolon=False)
            
            self.stream.skip_newlines()
            self.stream.expect(TokenType.RBRACE)
            self.stream.skip_newlines()
            # Consume trailing semicolon if present
            self.stream.match(TokenType.SEMICOLON)
        elif self.stream.match(TokenType.PROPERTIES):
            properties = self._parse_properties()
        else:
            self.stream.expect(TokenType.SEMICOLON)

        return InstanceDecl(
            type_name=type_name,
            identifier=identifier,
            properties=properties,
            location=start_loc,
        )

    def _parse_connection(self) -> ConnectionDecl:
        start_loc = self.stream.peek().location
        child = self.stream.expect_value(TokenType.IDENTIFIER)
        self.stream.expect(TokenType.ARROW)
        parent = self.stream.expect_value(TokenType.IDENTIFIER)
        self.stream.expect(TokenType.LBRACE)
        self.stream.skip_newlines()

        # localType: N;
        self.stream.expect(TokenType.LOCALTYPE)
        self.stream.expect(TokenType.COLON)
        local_type = int(self.stream.expect_value(TokenType.NUMBER))
        self.stream.expect(TokenType.SEMICOLON)
        self.stream.skip_newlines()

        # point: N; or point: uuid("...");
        self.stream.expect(TokenType.POINT)
        self.stream.expect(TokenType.COLON)

        point: Union[int, str]
        if self.stream.match(TokenType.UUID):
            self.stream.expect(TokenType.LPAREN)
            # Accept both UUID_LITERAL and STRING for UUID
            if self.stream.check(TokenType.UUID_LITERAL):
                uuid = self.stream.expect_value(TokenType.UUID_LITERAL)
            elif self.stream.check(TokenType.STRING):
                uuid = self.stream.expect_value(TokenType.STRING)
            else:
                token = self.stream.peek()
                self.diagnostics.add(make_diagnostic(
                    Codes.PARSE_INVALID_UUID,
                    f"Expected UUID or string in uuid(), got {token.type.value}",
                    Severity.ERROR,
                    token.location,
                ))
                uuid = ""
            self.stream.expect(TokenType.RPAREN)
            point = uuid
        else:
            point = int(self.stream.expect_value(TokenType.NUMBER))

        self.stream.expect(TokenType.SEMICOLON)
        self.stream.skip_newlines()
        self.stream.expect(TokenType.RBRACE)

        return ConnectionDecl(
            child=child,
            parent=parent,
            local_type=local_type,
            point=point,
            location=start_loc,
        )

    def _parse_output(self) -> OutputDecl:
        start_loc = self.stream.peek().location
        self.stream.expect(TokenType.LBRACE)
        self.stream.skip_newlines()

        file_path = ""
        source = None

        if self.stream.match(TokenType.FILE):
            self.stream.expect(TokenType.COLON)
            file_path = self.stream.expect_value(TokenType.STRING)
            self.stream.expect(TokenType.SEMICOLON)
            self.stream.skip_newlines()

        if self.stream.match(TokenType.SOURCE):
            self.stream.expect(TokenType.COLON)
            source = self.stream.expect_value(TokenType.STRING)
            self.stream.expect(TokenType.SEMICOLON)
            self.stream.skip_newlines()

        self.stream.skip_newlines()
        self.stream.expect(TokenType.RBRACE)

        return OutputDecl(
            file=file_path,
            source=source,
            location=start_loc,
        )


def parse(source: str, file: str = "<unknown>") -> tuple[Optional[File], DiagnosticCollector]:
    """Parse source code into AST."""
    tokens, lex_diagnostics = tokenize(source, file)
    if lex_diagnostics.has_errors():
        return None, lex_diagnostics

    parser = Parser(tokens, source, file)
    return parser.parse()
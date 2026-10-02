"""Lexer for RtG-Language 2.0."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Any
from pathlib import Path

from ..diagnostics import (
    DiagnosticCollector,
    Codes,
    SourceLocation,
    Severity,
    make_diagnostic,
)


class TokenType(str, Enum):
    """Token types for RtG-Language."""
    # Keywords
    RTG = "RTG"
    SCHEMA = "SCHEMA"
    OBJECT = "OBJECT"
    INSTANCE = "INSTANCE"
    AS = "AS"
    CONNECT = "CONNECT"
    LOCALTYPE = "LOCALTYPE"
    POINT = "POINT"
    UUID = "UUID"
    PROPERTIES = "PROPERTIES"
    ATTACHMENT = "ATTACHMENT"
    ON = "ON"
    PARTNAME = "PARTNAME"
    CFRAME = "CFRAME"
    OUTPUT = "OUTPUT"
    SOURCE = "SOURCE"
    FILE = "FILE"

    # Literals
    STRING = "STRING"
    NUMBER = "NUMBER"
    IDENTIFIER = "IDENTIFIER"
    UUID_LITERAL = "UUID_LITERAL"

    # Symbols
    SEMICOLON = "SEMICOLON"
    COLON = "COLON"
    ARROW = "ARROW"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    COMMA = "COMMA"
    DOT = "DOT"
    EQUALS = "EQUALS"

    # Special
    EOF = "EOF"
    NEWLINE = "NEWLINE"


@dataclass(frozen=True)
class Token:
    """A single token with position information."""
    type: TokenType
    value: Any
    location: SourceLocation

    def __str__(self) -> str:
        return f"{self.type}({self.value!r}) at {self.location}"


# Keywords mapping
KEYWORDS = {
    "rtg": TokenType.RTG,
    "schema": TokenType.SCHEMA,
    "object": TokenType.OBJECT,
    "instance": TokenType.INSTANCE,
    "as": TokenType.AS,
    "connect": TokenType.CONNECT,
    "localType": TokenType.LOCALTYPE,
    "point": TokenType.POINT,
    "uuid": TokenType.UUID,
    "properties": TokenType.PROPERTIES,
    "attachment": TokenType.ATTACHMENT,
    "on": TokenType.ON,
    "partName": TokenType.PARTNAME,
    "cframe": TokenType.CFRAME,
    "output": TokenType.OUTPUT,
    "source": TokenType.SOURCE,
    "file": TokenType.FILE,
}

# Single-character tokens
SIMPLE_TOKENS = {
    ";": TokenType.SEMICOLON,
    ":": TokenType.COLON,
    "{": TokenType.LBRACE,
    "}": TokenType.RBRACE,
    "[": TokenType.LBRACKET,
    "]": TokenType.RBRACKET,
    "(": TokenType.LPAREN,
    ")": TokenType.RPAREN,
    ",": TokenType.COMMA,
    ".": TokenType.DOT,
    "=": TokenType.EQUALS,
}

# Regex patterns
UUID_PATTERN = re.compile(r'\{[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\}')
NUMBER_PATTERN = re.compile(r'-?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?')
IDENTIFIER_PATTERN = re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*')
STRING_PATTERN = re.compile(r'"(?:[^"\\]|\\.)*"')


class Lexer:
    """Lexer for RtG-Language source code."""

    def __init__(self, source: str, file: str = "<unknown>"):
        self.source = source
        self.file = file
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: list[Token] = []
        self.diagnostics = DiagnosticCollector()

    def lex(self) -> tuple[list[Token], DiagnosticCollector]:
        """Tokenize the source code."""
        while self.position < len(self.source):
            self._lex_token()
        self.tokens.append(Token(TokenType.EOF, None, self._current_location()))
        return self.tokens, self.diagnostics

    def _current_location(self) -> SourceLocation:
        return SourceLocation(self.file, self.line, self.column, self.position)

    def _advance(self, count: int = 1) -> None:
        for _ in range(count):
            if self.position < len(self.source):
                if self.source[self.position] == '\n':
                    self.line += 1
                    self.column = 1
                else:
                    self.column += 1
                self.position += 1

    def _peek(self, offset: int = 0) -> str:
        pos = self.position + offset
        if pos < len(self.source):
            return self.source[pos]
        return '\0'

    def _peek_n(self, n: int) -> str:
        end = min(self.position + n, len(self.source))
        return self.source[self.position:end]

    def _lex_token(self) -> None:
        start_loc = self._current_location()
        char = self._peek()

        # Skip whitespace (but not newlines for potential significant newlines)
        if char in ' \t\r':
            self._advance()
            return

        # Newline
        if char == '\n':
            self.tokens.append(Token(TokenType.NEWLINE, '\n', start_loc))
            self._advance()
            return

        # Comment (// ...)
        if char == '/' and self._peek(1) == '/':
            self._lex_comment(start_loc)
            return

        # String literal
        if char == '"':
            self._lex_string(start_loc)
            return

        # UUID literal {xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx}
        if char == '{':
            uuid_match = UUID_PATTERN.match(self.source[self.position:])
            if uuid_match:
                uuid_str = uuid_match.group(0)
                self.tokens.append(Token(TokenType.UUID_LITERAL, uuid_str, start_loc))
                self._advance(len(uuid_str))
                return
            # Single brace
            self.tokens.append(Token(TokenType.LBRACE, '{', start_loc))
            self._advance()
            return

        # Number literal
        if char.isdigit() or (char == '-' and self._peek(1).isdigit()) or (char == '.' and self._peek(1).isdigit()):
            self._lex_number(start_loc)
            return

        # Arrow ->
        if char == '-' and self._peek(1) == '>':
            self.tokens.append(Token(TokenType.ARROW, '->', start_loc))
            self._advance(2)
            return

        # Identifier or keyword
        if char.isalpha() or char == '_':
            self._lex_identifier(start_loc)
            return

        # Simple tokens
        if char in SIMPLE_TOKENS:
            self.tokens.append(Token(SIMPLE_TOKENS[char], char, start_loc))
            self._advance()
            return

        # Unknown character
        self.diagnostics.add(make_diagnostic(
            Codes.LEX_INVALID_CHAR,
            f"Invalid character: {char!r}",
            Severity.ERROR,
            start_loc,
            ("Remove or replace the invalid character",)
        ))
        self._advance()

    def _lex_comment(self, start_loc: SourceLocation) -> None:
        """Lex a single-line comment."""
        while self.position < len(self.source) and self._peek() != '\n':
            self._advance()
        # Don't include the newline, let the main loop handle it

    def _lex_string(self, start_loc: SourceLocation) -> None:
        """Lex a string literal with escape sequences."""
        self._advance()  # Skip opening quote
        content_start = self.position

        while self.position < len(self.source):
            char = self._peek()
            if char == '\n':
                self.diagnostics.add(make_diagnostic(
                    Codes.LEX_UNTERMINATED_STRING,
                    "Unterminated string literal",
                    Severity.ERROR,
                    start_loc,
                    ("Close the string with a quote",)
                ))
                break
            if char == '"':
                # End of string
                content = self.source[content_start:self.position]
                # Process escape sequences
                try:
                    value = bytes(content, 'utf-8').decode('unicode_escape')
                except UnicodeDecodeError:
                    value = content
                    self.diagnostics.add(make_diagnostic(
                        Codes.LEX_INVALID_CHAR,
                        f"Invalid escape sequence in string",
                        Severity.WARNING,
                        SourceLocation(self.file, self.line, self.column, self.position),
                    ))
                self.tokens.append(Token(TokenType.STRING, value, start_loc))
                self._advance()  # Skip closing quote
                return
            if char == '\\':
                self._advance(2)  # Skip escape sequence
            else:
                self._advance()

        # If we exited the loop without finding closing quote
        if self.position >= len(self.source):
            self.diagnostics.add(make_diagnostic(
                Codes.LEX_UNTERMINATED_STRING,
                "Unterminated string literal at end of file",
                Severity.ERROR,
                start_loc,
                ("Close the string with a quote",)
            ))

    def _lex_number(self, start_loc: SourceLocation) -> None:
        """Lex a number literal (integer or float)."""
        match = NUMBER_PATTERN.match(self.source[self.position:])
        if not match:
            self.diagnostics.add(make_diagnostic(
                Codes.LEX_INVALID_NUMBER,
                f"Invalid number format",
                Severity.ERROR,
                start_loc,
            ))
            self._advance()
            return

        num_str = match.group(0)
        self._advance(len(num_str))

        # Parse as int or float
        try:
            if '.' in num_str or 'e' in num_str.lower():
                value = float(num_str)
            else:
                value = int(num_str)
        except ValueError:
            self.diagnostics.add(make_diagnostic(
                Codes.LEX_INVALID_NUMBER,
                f"Invalid number: {num_str}",
                Severity.ERROR,
                start_loc,
            ))
            value = 0

        self.tokens.append(Token(TokenType.NUMBER, value, start_loc))

    def _lex_identifier(self, start_loc: SourceLocation) -> None:
        """Lex an identifier or keyword."""
        match = IDENTIFIER_PATTERN.match(self.source[self.position:])
        if not match:
            self._advance()
            return

        ident = match.group(0)
        self._advance(len(ident))

        # Check for keywords (case-sensitive)
        token_type = KEYWORDS.get(ident, TokenType.IDENTIFIER)
        self.tokens.append(Token(token_type, ident, start_loc))


def tokenize(source: str, file: str = "<unknown>") -> tuple[list[Token], DiagnosticCollector]:
    """Convenience function to tokenize source."""
    lexer = Lexer(source, file)
    return lexer.lex()
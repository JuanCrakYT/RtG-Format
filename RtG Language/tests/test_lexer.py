"""Tests for RtG-Language lexer."""

import pytest
from rtg_language.lexer import tokenize, TokenType


def test_lexer_basic():
    """Test basic tokenization."""
    source = 'rtg "2.0";'
    tokens, diagnostics = tokenize(source, "test.rtg")
    
    assert not diagnostics.has_errors()
    assert tokens[0].type == TokenType.RTG
    assert tokens[1].type == TokenType.STRING
    assert tokens[1].value == "2.0"
    assert tokens[2].type == TokenType.SEMICOLON
    assert tokens[3].type == TokenType.EOF


def test_lexer_object():
    """Test object tokenization."""
    source = '''
    rtg "2.0";
    object "Test" {
        instance "Chassis" as chassis;
    }
    '''
    tokens, diagnostics = tokenize(source, "test.rtg")
    
    assert not diagnostics.has_errors()
    token_types = [t.type for t in tokens]
    assert TokenType.OBJECT in token_types
    assert TokenType.STRING in token_types
    assert TokenType.LBRACE in token_types
    assert TokenType.INSTANCE in token_types
    assert TokenType.AS in token_types
    assert TokenType.IDENTIFIER in token_types
    assert TokenType.RBRACE in token_types


def test_lexer_uuid():
    """Test UUID literal tokenization."""
    source = '{12345678-1234-1234-1234-123456789012}'
    tokens, diagnostics = tokenize(source, "test.rtg")
    
    assert not diagnostics.has_errors()
    assert tokens[0].type == TokenType.UUID_LITERAL
    assert tokens[0].value == '{12345678-1234-1234-1234-123456789012}'


def test_lexer_number():
    """Test number tokenization."""
    source = '123 -456 3.14 -2.5 1e10'
    tokens, diagnostics = tokenize(source, "test.rtg")
    
    assert not diagnostics.has_errors()
    numbers = [t for t in tokens if t.type == TokenType.NUMBER]
    assert len(numbers) == 5
    assert numbers[0].value == 123
    assert numbers[1].value == -456
    assert numbers[2].value == 3.14
    assert numbers[3].value == -2.5
    assert numbers[4].value == 1e10


def test_lexer_string():
    """Test string tokenization."""
    source = '"hello world" "with \\"quotes\\""'
    tokens, diagnostics = tokenize(source, "test.rtg")
    
    assert not diagnostics.has_errors()
    strings = [t for t in tokens if t.type == TokenType.STRING]
    assert len(strings) == 2
    assert strings[0].value == 'hello world'
    assert strings[1].value == 'with "quotes"'


def test_lexer_comment():
    """Test comment handling."""
    source = 'rtg "2.0"; // this is a comment\nobject "Test" {}'
    tokens, diagnostics = tokenize(source, "test.rtg")
    
    assert not diagnostics.has_errors()
    # Comment should be skipped, not produce tokens
    token_types = [t.type for t in tokens if t.type != TokenType.NEWLINE and t.type != TokenType.EOF]
    assert TokenType.RTG in token_types
    assert TokenType.OBJECT in token_types


def test_lexer_invalid_char():
    """Test invalid character detection."""
    source = 'rtg "2.0"; @invalid'
    tokens, diagnostics = tokenize(source, "test.rtg")
    
    assert diagnostics.has_errors()
    errors = diagnostics.get_errors()
    assert any(e.code == "LEX001" for e in errors)


def test_lexer_unterminated_string():
    """Test unterminated string detection."""
    source = 'rtg "2.0"; object "Test" { properties { "key": "unterminated }'
    tokens, diagnostics = tokenize(source, "test.rtg")
    
    assert diagnostics.has_errors()
    errors = diagnostics.get_errors()
    assert any(e.code == "LEX002" for e in errors)


def test_lexer_location_tracking():
    """Test that tokens have correct location info."""
    source = 'rtg "2.0";\nobject "Test" {}'
    tokens, diagnostics = tokenize(source, "test.rtg")
    
    assert not diagnostics.has_errors()
    # First token at line 1
    assert tokens[0].location.line == 1
    assert tokens[0].location.column == 1
    # object at line 2
    obj_token = next(t for t in tokens if t.type == TokenType.OBJECT)
    assert obj_token.location.line == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
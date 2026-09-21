"""
rtg_lang.py — Reference implementation (lexer + parser + compiler) for the
"Road to Gramby's format" (RtG) language — github.com/JuanCrakYT/RtG-Format.

Pipeline:
  source (.rtg) --tokenize--> tokens --parse--> AST --compile--> flat build
  array (the real RtG-Format runtime shape) --write--> .json / .txt / cache

The "flat build array" is the actual target format you showed me from a
real build:

    [
      ["Splitter_3", [["3","4",13], ["5","3",5], ...], {"RGB":[255,0,0]}],
      ["Servo",      [["1","2",10]],                    {...props...}],
      ["Connector",  [["5","2",20]],                     []],
      ...
    ]

Each entry is one CREATED instance, in `create`-statement order:
  - entry[0]  = the part's type name (e.g. "Part", "Connector", "Servo").
  - entry[1]  = list of [a, b, parent_id] connection triples:
        a         = local connection type from `-a(b)->`, as a STRING.
                    (None/omitted "default" case — exact default string
                    is still unconfirmed, see ASSUMPTIONS below.)
        b         = attachment point id from `(b)`, as a STRING.
        parent_id = 1-indexed position of the TARGET instance in this
                    same flat array (confirmed from your real build:
                    e.g. id 22 pointed at the 22nd/last entry).
  - entry[2]  = resolved properties: `global_properties` merged with any
                per-instance override from `track/properties` (which
                wins on key conflicts). If the merged result is empty,
                it's serialized as `[]` (matching your real build,
                where props-less entries show `[]`, not `{}`).

ASSUMPTIONS still open (flag these back to me / JuanCrakYT to confirm):
  * The exact string used for `a` when `-（b)->`/`-(b)->` omits the local
    type (i.e. what "default local type" serializes to). Currently kept
    as Python `None` in the AST and passed through as `null` if it
    reaches JSON — NOT yet guessing a specific default string.
  * How the `-a{[x,y,z],[...]}->` *structured* point form (offset +
    orientation instead of a plain `(b)` id) serializes in the flat
    array — no example of that shape was in the real build you sent, so
    it currently comes through as a raw object instead of a string.
  * Whether a `create` target can ever point at an instance in a
    DIFFERENT Object (cross-Object references). Not implemented — each
    Object's connections currently resolve only against instances
    created within that same Object.
  * The precise rule for the cross-Object index "offset" when several
    Objects share one output file: implemented here as "concatenate in
    `Order` order, each next Object's internal parent ids shifted by
    the running count of instances written so far for that file" — per
    your description, but not yet checked against a real multi-Object
    build.

Usage:
    python rtg_lang.py file.rtg [--ast] [--no-write]
"""

from __future__ import annotations

import base64
import json
import os
import re
import sys
from dataclasses import dataclass
from typing import Any


# --------------------------------------------------------------------------
# 1. Comment stripping (string-literal aware)
# --------------------------------------------------------------------------

def strip_comments(src: str) -> str:
    out = []
    i, n = 0, len(src)
    in_string = False
    while i < n:
        c = src[i]
        if in_string:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(src[i + 1])
                i += 2
                continue
            if c == '"':
                in_string = False
            i += 1
            continue
        if c == '"':
            in_string = True
            out.append(c)
            i += 1
            continue
        if c == "/" and i + 1 < n and src[i + 1] == "/":
            while i < n and src[i] not in "\r\n":
                i += 1
            continue
        out.append(c)
        i += 1
    return "".join(out)


# --------------------------------------------------------------------------
# 2. Tokenizer
# --------------------------------------------------------------------------

TOKEN_SPEC = [
    ("WS", r"[ \t\r\n]+"),
    ("STRING", r'"(?:\\.|[^"\\])*"'),
    ("ARROW2", r"-->"),
    ("ARROW1", r"->"),
    ("MINUS", r"-"),
    ("NUMBER", r"\d+(?:\.\d+)?"),
    ("LBRACKET", r"\["),
    ("RBRACKET", r"\]"),
    ("LBRACE", r"\{"),
    ("RBRACE", r"\}"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("COLON", r":"),
    ("SEMI", r";"),
    ("COMMA", r","),
    ("IDENT", r"[A-Za-z_][A-Za-z0-9_\-]*"),
]
TOKEN_RE = re.compile("|".join(f"(?P<{n}>{p})" for n, p in TOKEN_SPEC))

BLOCK_KEYWORDS = {
    "Order", "Object", "global_properties", "track", "object", "properties",
    "UUID", "note-names", "create", "output", "visualize",
}


@dataclass
class Token:
    type: str
    value: Any
    pos: int


def tokenize(src: str) -> list[Token]:
    tokens: list[Token] = []
    i, n = 0, len(src)
    while i < n:
        m = TOKEN_RE.match(src, i)
        if not m:
            raise SyntaxError(f"Unexpected character {src[i]!r} at offset {i}")
        kind = m.lastgroup
        text = m.group()
        if kind == "WS":
            i = m.end()
            continue
        if kind == "STRING":
            value = json.loads(text)
        elif kind == "NUMBER":
            value = float(text) if "." in text else int(text)
        else:
            value = text
        tokens.append(Token(kind, value, i))
        i = m.end()
    tokens.append(Token("EOF", None, n))
    return tokens


# --------------------------------------------------------------------------
# 3. Token stream helper
# --------------------------------------------------------------------------

class TokenStream:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0

    def peek(self, offset: int = 0) -> Token:
        idx = min(self.pos + offset, len(self.tokens) - 1)
        return self.tokens[idx]

    def next(self) -> Token:
        tok = self.tokens[self.pos]
        if tok.type != "EOF":
            self.pos += 1
        return tok

    def at_end(self) -> bool:
        return self.peek().type == "EOF"

    def expect(self, type_: str, value: Any = None) -> Token:
        tok = self.peek()
        if tok.type != type_ or (value is not None and tok.value != value):
            raise SyntaxError(
                f"Expected {type_}{'' if value is None else ' ' + repr(value)} "
                f"but got {tok.type} {tok.value!r} at offset {tok.pos}"
            )
        return self.next()

    def skip_semis(self) -> None:
        while self.peek().type == "SEMI":
            self.next()

    def is_ident(self, value: str) -> bool:
        tok = self.peek()
        return tok.type == "IDENT" and tok.value == value


# --------------------------------------------------------------------------
# 4. Generic JSON-literal parser (works directly on our token stream, so
#    global_properties / track-properties bodies don't need special
#    raw-text handling — they're just JSON-shaped tokens).
# --------------------------------------------------------------------------

def parse_json_from_tokens(ts: TokenStream) -> Any:
    tok = ts.peek()
    if tok.type == "LBRACE":
        ts.next()
        obj: dict[str, Any] = {}
        if ts.peek().type != "RBRACE":
            while True:
                key = ts.expect("STRING").value
                ts.expect("COLON")
                obj[key] = parse_json_from_tokens(ts)
                if ts.peek().type == "COMMA":
                    ts.next()
                    continue
                break
        ts.expect("RBRACE")
        return obj
    if tok.type == "LBRACKET":
        ts.next()
        arr: list[Any] = []
        if ts.peek().type != "RBRACKET":
            while True:
                arr.append(parse_json_from_tokens(ts))
                if ts.peek().type == "COMMA":
                    ts.next()
                    continue
                break
        ts.expect("RBRACKET")
        return arr
    if tok.type == "STRING":
        ts.next()
        return tok.value
    if tok.type == "MINUS":
        ts.next()
        return -ts.expect("NUMBER").value
    if tok.type == "NUMBER":
        ts.next()
        return tok.value
    if tok.type == "IDENT" and tok.value in ("true", "false", "null"):
        ts.next()
        return {"true": True, "false": False, "null": None}[tok.value]
    raise SyntaxError(f"Unexpected token in JSON literal: {tok}")


# --------------------------------------------------------------------------
# 5. Block extraction helpers (nested-block aware, compact-`{}` aware)
# --------------------------------------------------------------------------

def _skip_nested_block(ts: TokenStream, collected: list[Token]) -> None:
    collected.append(ts.next())  # the keyword itself
    if ts.peek().type == "LBRACE":
        collected.append(ts.next())
        depth = 1
        while depth > 0:
            tok = ts.peek()
            if tok.type == "EOF":
                raise SyntaxError("Unexpected EOF while looking for matching '}'")
            if tok.type == "LBRACE":
                depth += 1
            elif tok.type == "RBRACE":
                depth -= 1
            collected.append(ts.next())
        while ts.peek().type == "SEMI":
            collected.append(ts.next())
        return
    while True:
        tok = ts.peek()
        if tok.type == "EOF":
            raise SyntaxError("Unexpected EOF while looking for matching 'end'")
        if tok.type == "IDENT" and tok.value in BLOCK_KEYWORDS:
            _skip_nested_block(ts, collected)
            continue
        if tok.type == "IDENT" and tok.value == "end":
            collected.append(ts.next())
            while ts.peek().type == "SEMI":
                collected.append(ts.next())
            return
        collected.append(ts.next())


def collect_until_matching_end(ts: TokenStream) -> list[Token]:
    collected: list[Token] = []
    while True:
        tok = ts.peek()
        if tok.type == "EOF":
            raise SyntaxError("Unexpected EOF while looking for matching 'end'")
        if tok.type == "IDENT" and tok.value in BLOCK_KEYWORDS:
            _skip_nested_block(ts, collected)
            continue
        if tok.type == "IDENT" and tok.value == "end":
            ts.next()
            ts.skip_semis()
            return collected
        collected.append(ts.next())


def collect_until_matching_brace(ts: TokenStream) -> list[Token]:
    depth = 1
    collected: list[Token] = []
    while True:
        tok = ts.peek()
        if tok.type == "EOF":
            raise SyntaxError("Unexpected EOF while looking for matching '}'")
        if tok.type == "LBRACE":
            depth += 1
        elif tok.type == "RBRACE":
            depth -= 1
            if depth == 0:
                ts.next()
                ts.skip_semis()
                return collected
        collected.append(ts.next())


# --------------------------------------------------------------------------
# 6. Grammar-specific sub-parsers (operate on a flat token slice)
# --------------------------------------------------------------------------

def parse_ref(ts: TokenStream) -> dict:
    ts.expect("LBRACKET")
    name = ts.expect("STRING").value
    ts.expect("COLON")
    index = ts.expect("NUMBER").value
    ts.expect("RBRACKET")
    return {"type": name, "index": int(index)}


def parse_signed_number(ts: TokenStream):
    sign = 1
    if ts.peek().type == "MINUS":
        ts.next()
        sign = -1
    return sign * ts.expect("NUMBER").value


def parse_number_array(ts: TokenStream) -> list:
    ts.expect("LBRACKET")
    values = []
    if ts.peek().type != "RBRACKET":
        values.append(parse_signed_number(ts))
        while ts.peek().type == "COMMA":
            ts.next()
            values.append(parse_signed_number(ts))
    ts.expect("RBRACKET")
    return values


def parse_track_object(tokens: list[Token]) -> dict[str, int]:
    ts = TokenStream(tokens + [Token("EOF", None, -1)])
    counts: dict[str, int] = {}
    while ts.peek().type == "STRING":
        name = ts.next().value
        ts.expect("COLON")
        count = ts.expect("NUMBER").value
        counts[name] = int(count)
        if ts.peek().type == "SEMI":
            ts.next()
    return counts


def parse_track_uuid(tokens: list[Token]) -> list[dict]:
    ts = TokenStream(tokens + [Token("EOF", None, -1)])
    groups = []
    while ts.peek().type == "LBRACKET":
        root = parse_ref(ts)
        if ts.is_ident("by"):
            ts.next()
        ts.expect("LBRACE")
        members = []
        while ts.peek().type == "LBRACKET":
            ts.next()
            part_name = ts.expect("STRING").value
            mult = 1
            tok = ts.peek()
            if tok.type == "IDENT" and re.fullmatch(r"x\d+", tok.value):
                mult = int(tok.value[1:])
                ts.next()
            ts.expect("RBRACKET")
            members.append({"part": part_name, "count": mult})
            if ts.peek().type == "COMMA":
                ts.next()
        ts.expect("RBRACE")
        groups.append({"root": root, "members": members})
        if ts.peek().type == "SEMI":
            ts.next()
    return groups


def parse_track_properties(tokens: list[Token]) -> dict[str, dict]:
    """`["Chassis":1] { "RGB":[0,255,0] }` — per-instance property
    overrides. Priority over `global_properties` (per JuanCrakYT)."""
    ts = TokenStream(tokens + [Token("EOF", None, -1)])
    overrides: dict[str, dict] = {}
    while ts.peek().type == "LBRACKET":
        ref = parse_ref(ts)
        props = parse_json_from_tokens(ts)
        overrides[f'{ref["type"]}:{ref["index"]}'] = props
        if ts.peek().type == "SEMI":
            ts.next()
    return overrides


def parse_track(tokens: list[Token]) -> dict:
    ts = TokenStream(tokens + [Token("EOF", None, -1)])
    result: dict[str, Any] = {"object": {}, "UUID": [], "properties": {}}
    while not ts.at_end():
        tok = ts.peek()
        if tok.type != "IDENT" or tok.value not in ("object", "UUID", "properties"):
            raise SyntaxError(f"Unexpected token in track: {tok}")
        kw = ts.next().value
        if ts.peek().type == "LBRACE":
            ts.next()
            body = collect_until_matching_brace(ts)
        else:
            body = collect_until_matching_end(ts)
        if kw == "object":
            result["object"] = parse_track_object(body)
        elif kw == "UUID":
            result["UUID"] = parse_track_uuid(body)
        else:
            result["properties"] = parse_track_properties(body)
    return result


def parse_note_names(tokens: list[Token]) -> list[dict]:
    ts = TokenStream(tokens + [Token("EOF", None, -1)])
    notes = []
    while ts.peek().type == "LBRACKET":
        ref = parse_ref(ts)
        ts.expect("ARROW2")
        label = ts.expect("STRING").value
        notes.append({"ref": ref, "label": label})
        if ts.peek().type == "SEMI":
            ts.next()
    return notes


def parse_create(tokens: list[Token]) -> list[dict]:
    ts = TokenStream(tokens + [Token("EOF", None, -1)])
    statements = []
    while ts.peek().type == "LBRACKET":
        ref = parse_ref(ts)
        if ts.peek().type == "SEMI" or ts.at_end():
            statements.append({"op": "instantiate", "ref": ref})
        else:
            # `-a(b)->` : the leading '-' is a literal delimiter, NOT a
            # sign. `a` (local connection type) is OPTIONAL: `-(b)->`
            # means "use the default local type".
            ts.expect("MINUS")
            local_type = None
            if ts.peek().type == "NUMBER":
                local_type = int(ts.next().value)
            tok = ts.peek()
            if tok.type == "LPAREN":
                ts.next()
                point_id = int(ts.expect("NUMBER").value)
                ts.expect("RPAREN")
            elif tok.type == "LBRACE":
                ts.next()
                offset = parse_number_array(ts)
                ts.expect("COMMA")
                orientation = parse_number_array(ts)
                ts.expect("RBRACE")
                point_id = {"offset": offset, "orientation": orientation}
            else:
                raise SyntaxError(f"Unexpected connector params at {tok}")
            ts.expect("ARROW1")
            target = parse_ref(ts)
            statements.append({
                "op": "connect",
                "ref": ref,
                "local_type": local_type,
                "point_id": point_id,
                "target": target,
            })
        if ts.peek().type == "SEMI":
            ts.next()
    return statements


def parse_output(tokens: list[Token]) -> dict:
    ts = TokenStream(tokens + [Token("EOF", None, -1)])
    cache_path = None
    files = []
    while not ts.at_end():
        if ts.is_ident("cache"):
            ts.next()
            ts.expect("LPAREN")
            cache_path = ts.expect("STRING").value
            ts.expect("RPAREN")
        elif ts.peek().type == "STRING":
            files.append(ts.next().value)
        else:
            raise SyntaxError(f"Unexpected token in output: {ts.peek()}")
        if ts.peek().type == "SEMI":
            ts.next()
    return {"cache": cache_path, "files": files}


# --------------------------------------------------------------------------
# 7. Top-level parser
# --------------------------------------------------------------------------

def parse_object_body(kw: str, tokens: list[Token]) -> Any:
    if kw == "track":
        return parse_track(tokens)
    if kw == "note-names":
        return parse_note_names(tokens)
    if kw == "create":
        return parse_create(tokens)
    if kw == "output":
        return parse_output(tokens)
    if kw == "visualize":
        return {"raw": tokens}
    raise SyntaxError(f"Unknown section keyword: {kw}")


def parse_source(src: str) -> dict:
    clean = strip_comments(src)
    tokens = tokenize(clean)
    ts = TokenStream(tokens)

    ts.expect("IDENT", "Order")
    order = []
    while ts.peek().type == "STRING":
        order.append(ts.next().value)
        if ts.peek().type == "SEMI":
            ts.next()
    ts.expect("IDENT", "end")
    ts.skip_semis()

    objects = []
    while not ts.at_end():
        ts.expect("IDENT", "Object")
        ts.expect("LPAREN")
        name = ts.expect("STRING").value
        ts.expect("RPAREN")
        sections: dict[str, Any] = {}
        while not (ts.peek().type == "IDENT" and ts.peek().value == "end"):
            kw_tok = ts.expect("IDENT")
            kw = kw_tok.value
            if kw not in BLOCK_KEYWORDS or kw in ("Order", "Object"):
                raise SyntaxError(f"Unexpected section keyword {kw!r}")
            if kw == "global_properties":
                sections["global_properties"] = parse_json_from_tokens(ts)
                ts.expect("IDENT", "end")
                ts.skip_semis()
                continue
            if ts.peek().type == "LBRACE":
                ts.next()
                body_tokens = collect_until_matching_brace(ts)
            else:
                body_tokens = collect_until_matching_end(ts)
            sections[kw] = parse_object_body(kw, body_tokens)
        ts.expect("IDENT", "end")
        ts.skip_semis()
        objects.append({"name": name, "sections": sections})

    return {"order": order, "objects": objects}


# --------------------------------------------------------------------------
# 8. Compiler: AST -> the real RtG-Format flat build array
# --------------------------------------------------------------------------

def ref_key(ref: dict) -> str:
    return f'{ref["type"]}:{ref["index"]}'


def merge_properties(global_props: dict, track_props: dict, key: str) -> Any:
    merged = {**global_props, **track_props.get(key, {})}
    return merged if merged else []


def compile_object(obj: dict) -> tuple[list[list], dict[str, int]]:
    """Returns (entries, index_by_ref) where `entries` is this Object's
    OWN flat build array (parent ids are LOCAL to this Object — 1-indexed
    — the caller applies the cross-Object offset before concatenating)."""
    sections = obj["sections"]
    global_props = sections.get("global_properties", {})
    track = sections.get("track", {"object": {}, "UUID": [], "properties": {}})
    create = sections.get("create", [])
    track_props = track.get("properties", {})

    # Assign 1-indexed ids in `create`-statement order (first time a ref
    # appears as the LHS of a create statement).
    index_by_ref: dict[str, int] = {}
    order_of_refs: list[dict] = []
    for stmt in create:
        key = ref_key(stmt["ref"])
        if key not in index_by_ref:
            index_by_ref[key] = len(order_of_refs) + 1
            order_of_refs.append(stmt["ref"])

    connections_by_ref: dict[str, list] = {key: [] for key in index_by_ref}
    for stmt in create:
        if stmt["op"] != "connect":
            continue
        src_key = ref_key(stmt["ref"])
        tgt_key = ref_key(stmt["target"])
        if tgt_key not in index_by_ref:
            raise ValueError(
                f"create target {tgt_key} was never instantiated with its "
                f"own `[{tgt_key}];` statement in Object(\"{obj['name']}\")"
            )
        a = "" if stmt["local_type"] is None else str(stmt["local_type"])
        point = stmt["point_id"]
        b = str(point) if not isinstance(point, dict) else point  # see ASSUMPTIONS
        connections_by_ref[src_key].append([a, b, index_by_ref[tgt_key]])

    entries = []
    for ref in order_of_refs:
        key = ref_key(ref)
        entries.append([
            ref["type"],
            connections_by_ref[key],
            merge_properties(global_props, track_props, key),
        ])
    return entries, index_by_ref


def compile_program(ast: dict) -> dict[str, list[list]]:
    """Returns {output_file_path: flat_build_array}, applying the
    cross-Object offset when several Objects write to the same file
    (concatenated in `Order` declaration order)."""
    order = ast["order"]
    objects_by_name = {o["name"]: o for o in ast["objects"]}
    ordered_objects = [objects_by_name[n] for n in order if n in objects_by_name]
    ordered_objects += [o for o in ast["objects"] if o["name"] not in order]

    files: dict[str, list[list]] = {}
    running_offset: dict[str, int] = {}
    for obj in ordered_objects:
        out_section = obj["sections"].get("output")
        if not out_section:
            continue
        entries, _ = compile_object(obj)
        for rel_path in out_section.get("files", []):
            offset = running_offset.get(rel_path, 0)
            shifted = [
                [name, [[a, b, pid + offset] for a, b, pid in conns], props]
                for name, conns, props in entries
            ]
            files.setdefault(rel_path, []).extend(shifted)
            running_offset[rel_path] = offset + len(entries)
    return files


# --------------------------------------------------------------------------
# 9. Output writer
# --------------------------------------------------------------------------

def write_outputs(ast: dict, source_path: str) -> list[str]:
    written = []
    compiled = compile_program(ast)

    for rel_path, data in compiled.items():
        root, ext = os.path.splitext(rel_path)
        ext = ext.lower()
        os.makedirs(os.path.dirname(rel_path) or ".", exist_ok=True)
        if ext in (".json", ""):
            target = rel_path if ext else rel_path + ".json"
            with open(target, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            written.append(target)
        elif ext == ".txt":
            payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
            with open(rel_path, "w", encoding="utf-8") as f:
                f.write(base64.b64encode(payload).decode("ascii"))
            written.append(rel_path)
        else:
            raise ValueError(f"Unsupported output extension {ext!r} for {rel_path}")

    for obj in ast["objects"]:
        out_section = obj["sections"].get("output")
        if not out_section or not out_section.get("cache"):
            continue
        cache_dir = out_section["cache"]
        os.makedirs(cache_dir, exist_ok=True)
        cache_file = os.path.join(cache_dir, f'{obj["name"]}.rtg-cache')
        with open(cache_file, "w", encoding="utf-8") as f:
            f.write(f"source: {os.path.abspath(source_path)}\n")
        written.append(cache_file)

    return written


# --------------------------------------------------------------------------
# 10. CLI
# --------------------------------------------------------------------------

def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: python rtg_lang.py file.rtg [--ast] [--no-write]")
        return 1
    path = argv[1]
    show_ast = "--ast" in argv
    do_write = "--no-write" not in argv

    with open(path, "r", encoding="utf-8") as f:
        src = f.read()

    ast = parse_source(src)
    if show_ast:
        print(json.dumps(ast, ensure_ascii=False, indent=2))

    compiled = compile_program(ast)
    print(json.dumps(compiled, ensure_ascii=False, indent=2))

    if do_write:
        for w in write_outputs(ast, path):
            print(f"wrote: {w}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

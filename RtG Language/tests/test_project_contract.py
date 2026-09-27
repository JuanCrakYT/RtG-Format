import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_json_artifacts_are_valid():
    for relative in (
        "package.json",
        "extension/language-configuration.json",
        "extension/syntaxes/rtg-language.tmLanguage.json",
        "extension/snippets/rtg-language.json",
        "schema/schema.json",
        "data.json",
    ):
        with (ROOT / relative).open(encoding="utf-8") as source:
            json.load(source)


def test_extension_associates_rtg_files():
    manifest = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    assert manifest["contributes"]["languages"][0]["extensions"] == [".rtg"]


def test_new_examples_use_the_v2_header():
    for example in (ROOT / "examples").glob("*.rtg"):
        if not example.name.startswith("example"):
            assert example.read_text(encoding="utf-8").startswith("rtg 2.0;")

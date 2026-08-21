import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / "old-files" / "obj_ids-spanish.md"
PARTS = ROOT / "blocks" / "parts"

CATEGORIES = {
    "building": {"Chassis", "Wheel", "Tire", "Bumper", "Hood", "Trunk", "Wing", "ShortStick", "Stick", "LongStick", "Spoiler", "FuelTank"},
    "physics": {"Cannon", "Propeller", "Bearing", "Leg", "StaringGyro", "Piston", "Servo", "Servo_Physics", "Anchor", "BallSocket", "MatchingGyro"},
    "wiring": {"Button", "InputSensor", "AltitudeSensor", "VelocitySensor", "Switch", "TripWire", "RemoteButton", "PressurePlate", "Detacher", "EntitySensor", "Looper", "Gate-AND", "Gate-OR", "Gate-NOT", "Wire"},
    "tools": {"RPG", "Uzi", "Briefcase"},
    "uncategorized": {"Body", "YibYib"},
}

SECTION_RE = re.compile(r"^###\s+(\d+)\.\s+(.+)$", re.MULTILINE)
ROW_RE = re.compile(r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|", re.MULTILINE)
NO_POINTS_RE = re.compile(r"^\s*\d+\.\s+(.+?)\s*$", re.MULTILINE)


def parse_source():
    text = OLD.read_text(encoding="utf-8")
    matches = list(SECTION_RE.finditer(text))
    sections = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[match.end():end]
        rows = [{"id": int(row.group(1)), "name": row.group(2).strip(), "side": row.group(3).strip(), "description": row.group(4).strip()} for row in ROW_RE.finditer(block)]
        sections.append({"number": int(match.group(1)), "name": match.group(2).strip(), "rows": rows})
    no_points_start = text.index("## Objetos sin puntos de conexión propios")
    no_points = [name for name in NO_POINTS_RE.findall(text[no_points_start:]) if not name.startswith("El objeto")]
    return sections, no_points


def category_for(name):
    for category, names in CATEGORIES.items():
        if name in names:
            return category
    return "uncategorized"


def render_section(section):
    heading = section["name"] if section["number"] == 1 else f"{section['name']} (source section {section['number']})"
    lines = [f"## {heading}", "", "| ID | Name | Side | Description | Status | Source / Evidence |", "| --- | --- | --- | --- | --- | --- |"]
    for row in section["rows"]:
        lines.append(f"| {row['id']} | {row['name']} | {row['side']} | {row['description']} | CONFIRMED | old-files/obj_ids-spanish.md — {section['name']} table |")
    return "\n".join(lines)


def render_category(category, sections):
    title = category.replace("-", " ").title()
    lines = [f"# {title} Parts — Connection Point IDs", "", "> Fuente histórica: `old-files/obj_ids-spanish.md`", "> Estado: todos los datos migrados están confirmados según la actualización española.", "> La clasificación por categoría es organizativa; las tablas reproducen la evidencia histórica.", ""]
    lines.append("\n\n".join(render_section(section) for section in sections) if sections else "No hay tablas de IDs propias asignadas a esta categoría en el archivo histórico.")
    return "\n".join(lines).rstrip() + "\n"


def render_index(sections, no_points):
    lines = ["# Parts — índice histórico migrado", "", "> Fuente: `old-files/obj_ids-spanish.md`", "> Estado: datos confirmados según la actualización española.", "> Este índice conserva todas las secciones con IDs y la lista histórica de objetos sin puntos propios.", "", "## Secciones migradas", "", "| Sección | Categoría | Filas de IDs |", "| --- | --- | ---: |"]
    lines.extend(f"| {section['name']} | {category_for(section['name'])} | {len(section['rows'])} |" for section in sections)
    lines.extend(["", "## Objetos sin puntos de conexión propios", "", "| Nombre | Estado | Fuente / Evidencia |", "| --- | --- | --- |"])
    lines.extend(f"| {name} | CONFIRMED | old-files/obj_ids-spanish.md — lista de objetos sin puntos propios |" for name in no_points)
    return "\n".join(lines).rstrip() + "\n"


def audit(sections, no_points):
    old_rows = [(section["name"], row["id"], row["name"], row["side"], row["description"]) for section in sections for row in section["rows"]]
    new_rows = []
    for path in sorted(PARTS.glob("*/parts-id.md")):
        for row in ROW_RE.finditer(path.read_text(encoding="utf-8")):
            new_rows.append((path.as_posix(), int(row.group(1)), row.group(2).strip(), row.group(3).strip(), row.group(4).strip()))
    old_keys = Counter((row[1], row[2], row[3], row[4]) for row in old_rows)
    new_keys = Counter((row[1], row[2], row[3], row[4]) for row in new_rows)
    missing = [list(key) for key, count in (old_keys - new_keys).items() for _ in range(count)]
    extra = [list(key) for key, count in (new_keys - old_keys).items() for _ in range(count)]
    return {"source": "old-files/obj_ids-spanish.md", "counts": {"historical_sections": len(sections), "historical_rows": len(old_rows), "migrated_rows": len(new_rows), "historical_no_point_objects": len(no_points)}, "missing_rows": missing, "extra_rows": extra, "historical_duplicate_rows": sum(count - 1 for count in old_keys.values() if count > 1), "migrated_duplicate_rows": sum(count - 1 for count in new_keys.values() if count > 1), "historical_files_modified": 0, "invented_rows": len(extra)}


def main():
    sections, no_points = parse_source()
    by_category = {category: [] for category in CATEGORIES}
    for category in ("miscellaneous", "other", "unused"):
        by_category[category] = []
    for section in sections:
        by_category.setdefault(category_for(section["name"]), []).append(section)
    for category, category_sections in by_category.items():
        (PARTS / category / "parts-id.md").write_text(render_category(category, category_sections), encoding="utf-8")
    (PARTS / "parts-id.md").write_text(render_index(sections, no_points), encoding="utf-8")
    report = audit(sections, no_points)
    (PARTS / "migration_diff.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

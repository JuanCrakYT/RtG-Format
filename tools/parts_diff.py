import re
import glob
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / 'old-files' / 'obj_ids-spanish.md'
NEW_GLOB = ROOT / 'blocks' / 'parts' / '**' / 'parts-id.md'

section_re = re.compile(r'^###\s*(?:\d+\.)?\s*(.+)$', re.MULTILINE)
row_re = re.compile(r'^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|', re.MULTILINE)

def parse_old(path):
    text = path.read_text(encoding='utf-8')
    sections = []
    # find all sections
    matches = list(section_re.finditer(text))
    for i, m in enumerate(matches):
        name = m.group(1).strip()
        start = m.end()
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        block = text[start:end]
        rows = []
        for r in row_re.finditer(block):
            id_ = int(r.group(1))
            col_name = r.group(2).strip()
            side = r.group(3).strip()
            rows.append({'id': id_, 'name': col_name, 'side': side})
        sections.append({'section': name, 'rows': rows})
    return sections


def parse_new(glob_pattern):
    files = glob.glob(str(glob_pattern), recursive=True)
    records = []
    for f in files:
        text = Path(f).read_text(encoding='utf-8')
        # extract table rows with numeric id
        for r in row_re.finditer(text):
            id_ = int(r.group(1))
            col_name = r.group(2).strip()
            side = r.group(3).strip()
            records.append({'file': str(Path(f).relative_to(ROOT)), 'id': id_, 'name': col_name, 'side': side})
        # also extract listed historical names ("(listed historically)" rows)
        list_re = re.compile(r'^\|\s*\(listed historically\)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|', re.MULTILINE)
        for r in list_re.finditer(text):
            name = r.group(1).strip()
            side = r.group(2).strip()
            records.append({'file': str(Path(f).relative_to(ROOT)), 'id': None, 'name': name, 'side': side})
    return records


def canonical(rec):
    return (rec.get('name') or '').strip().lower(), rec.get('id')


def main():
    old = parse_old(OLD)
    new = parse_new(NEW_GLOB)

    old_recs = []
    for s in old:
        sect_name = s['section']
        if s['rows']:
            for r in s['rows']:
                rec = {'section': sect_name, 'id': r['id'], 'name': r['name'], 'side': r['side']}
                old_recs.append(rec)
        else:
            # sections with no rows are ignored here
            pass

    # map by canonical key
    old_map = {canonical(r): r for r in old_recs}
    new_map = {canonical(r): r for r in new}

    missing = []
    for k, r in old_map.items():
        if k not in new_map:
            missing.append(r)

    extra = []
    for k, r in new_map.items():
        if k not in old_map:
            extra.append(r)

    # duplicates: same canonical name+id appears multiple times in old or new
    def find_duplicates(recs):
        seen = {}
        dups = []
        for r in recs:
            key = canonical(r)
            seen.setdefault(key, 0)
            seen[key] += 1
        for k, v in seen.items():
            if v > 1:
                dups.append({'name': k[0], 'count': v})
        return dups

    duplicates_old = find_duplicates(old_recs)
    duplicates_new = find_duplicates(new)

    out = {
        'counts': {
            'old_total_rows': len(old_recs),
            'new_total_rows': len(new),
            'old_sections': len(old),
            'new_files': len(set(r['file'] for r in new)),
        },
        'missing_in_new': missing,
        'extra_in_new': extra,
        'duplicates_old': duplicates_old,
        'duplicates_new': duplicates_new,
    }

    out_path = ROOT / 'blocks' / 'parts' / 'migration_diff.json'
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding='utf-8')
    print('Wrote', out_path)

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Update processed monsters metadata with parsed names and family info.

Usage:
  python update_processed_with_parsed.py \
    <processed.json> <parsed.json> <monsterFamilies.json>

This will overwrite the processed.json file with updated name.en and
family fields when a parsed entry matches by id.
"""
import sys
import json
from typing import Dict, List


def load_families(families_list: List[Dict]) -> Dict[str, Dict]:
    # Map english lower name -> family entry
    m = {}
    for f in families_list:
        names = f.get('name') or []
        if len(names) > 1 and names[1]:
            key = names[1].strip().lower()
            m[key] = {
                'id': f.get('id'),
                'names': {
                    'fr': names[0] if len(names) > 0 else None,
                    'en': names[1] if len(names) > 1 else None,
                    'es': names[2] if len(names) > 2 else None,
                    'pt': names[3] if len(names) > 3 else None,
                }
            }
    return m


def main(argv):
    if len(argv) < 4:
        print('Usage: update_processed_with_parsed.py processed.json parsed.json monsterFamilies.json')
        return 2

    processed_path = argv[1]
    parsed_path = argv[2]
    families_path = argv[3]

    with open(processed_path, 'r', encoding='utf-8') as f:
        processed = json.load(f)

    with open(parsed_path, 'r', encoding='utf-8') as f:
        parsed = json.load(f)

    with open(families_path, 'r', encoding='utf-8') as f:
        families = json.load(f)

    family_map = load_families(families)

    monsters = processed.get('monsters') or []
    monsters_by_id = {m.get('monster_id'): m for m in monsters if isinstance(m, dict) and 'monster_id' in m}

    updated_name = 0
    updated_family = 0
    updated_gfx = 0

    for entry in parsed:
        pid = entry.get('id')
        if not pid:
            continue
        try:
            mid = int(pid)
        except Exception:
            continue

        monster = monsters_by_id.get(mid)
        if not monster:
            continue

        # Update name.en
        p_name = entry.get('name')
        if p_name:
            # ensure monster['name'] exists
            if 'name' not in monster or not isinstance(monster['name'], dict):
                monster['name'] = {}
            if monster['name'].get('en') != p_name:
                monster['name']['en'] = p_name
                updated_name += 1

        # Update gfx_id if available
        p_gfx = entry.get('gfx_id')
        if p_gfx and (not monster.get('gfx_id') or str(monster.get('gfx_id')) != str(p_gfx)):
            monster['gfx_id'] = p_gfx
            updated_gfx += 1

        # Update family: try to find family id by english name
        p_family = entry.get('family')
        if p_family:
            key = str(p_family).strip().lower()
            fam = family_map.get(key)
            if fam:
                # build family object similar to existing structure
                newfam = {
                    'id': fam['id'],
                    'names': fam['names'],
                    'match': True,
                    'candidate_ids': [fam['id']]
                }
                # compare existing family id
                old_fam = monster.get('family')
                old_id = old_fam.get('id') if isinstance(old_fam, dict) else None
                if old_id != fam['id']:
                    monster['family'] = newfam
                    updated_family += 1

    # Write back processed JSON (overwrite)
    with open(processed_path, 'w', encoding='utf-8') as f:
        json.dump(processed, f, ensure_ascii=False, indent=2)

    print(f'Updated names: {updated_name}, families: {updated_family}, gfx_id: {updated_gfx}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))

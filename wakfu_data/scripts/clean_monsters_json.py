#!/usr/bin/env python3
"""
Clean the parsed monsters JSON by removing header rows and entries without id/gfx_id.

Usage:
  python clean_monsters_json.py input.json output.json

This script keeps entries where:
 - name exists and is not blank and not equal to 'name' (case-insensitive)
 - and at least one of id or gfx_id is present
"""
import sys
import json
from typing import List, Dict


def clean_monsters(data: List[Dict]) -> List[Dict]:
    out = []
    for x in data:
        # skip non-dict entries
        if not isinstance(x, dict):
            continue
        name = x.get('name')
        if not name:
            continue
        if not str(name).strip():
            continue
        if str(name).strip().lower() == 'name':
            continue
        if not (x.get('id') or x.get('gfx_id')):
            continue
        out.append(x)
    return out


def main(argv):
    if len(argv) < 3:
        print('Usage: python clean_monsters_json.py input.json output.json')
        return 2
    inp = argv[1]
    outp = argv[2]
    with open(inp, 'r', encoding='utf-8') as f:
        data = json.load(f)
    cleaned = clean_monsters(data)
    with open(outp, 'w', encoding='utf-8') as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)
    print(f'IN {len(data)} OUT {len(cleaned)}')
    if cleaned:
        print(json.dumps(cleaned[:10], ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))

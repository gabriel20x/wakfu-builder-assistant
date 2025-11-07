#!/usr/bin/env python3
"""
Simple extractor for monster tables like the example provided.

Usage:
  python parse_monsters_table.py input.html output.json

It does not require external libraries and attempts to be robust for
the table structure described: image cell (with <img src> and a JSON
<script> containing the "linker-query-datas" id), name link <a>,
family in <td class="item-type"> and level in <td class="item-level">.

Only rows where the <a> contains visible text (the monster name) are
included.
"""
import sys
import re
import json
from typing import List, Dict


def parse_html_to_monsters(html: str) -> List[Dict]:
    # Split into rows (<tr> ... </tr>) — conservative, non-greedy
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", html, flags=re.S | re.I)
    out = []

    for row in rows:
        # Find the JSON <script> that contains linker-query-datas and extract id
        script_jsons = re.findall(r"<script[^>]*type=[\"']application/json[\"'][^>]*>(.*?)</script>", row, flags=re.S | re.I)
        monster_id = None
        for sj in script_jsons:
            if 'linker-query-datas' in sj or 'linker-id' in sj:
                # attempt to find "id":"NUMBER" pattern
                m = re.search(r'"id"\s*:\s*"?(\d+)"?', sj)
                if m:
                    monster_id = m.group(1)
                    break

        # Find the gfx id from the <img src=".../NUMBER.png">
        m = re.search(r"<img[^>]+src=[\"'][^\"']*(?:/|%2F)([0-9]+)\.png[\"']", row, flags=re.I)
        gfx_id = m.group(1) if m else None

        # Find the <a ...>NAME</a>
        m = re.search(r"<a[^>]*>(.*?)</a>", row, flags=re.S | re.I)
        name = None
        if m:
            # strip HTML tags inside and whitespace
            name_text = re.sub(r"<[^>]+>", "", m.group(1)).strip()
            if name_text:
                name = name_text

        if not name:
            # per instructions, skip rows without visible name
            continue

        # family
        m = re.search(r"<td[^>]*class=[\"']?item-type[\"']?[^>]*>(.*?)</td>", row, flags=re.S | re.I)
        family = re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else None

        # level
        m = re.search(r"<td[^>]*class=[\"']?item-level[\"']?[^>]*>(.*?)</td>", row, flags=re.S | re.I)
        level = re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else None

        item = {
            "id": monster_id,
            "gfx_id": gfx_id,
            "name": name,
            "family": family,
            "level": level,
        }
        out.append(item)

    return out


def main(argv):
    if len(argv) < 3:
        print("Usage: python parse_monsters_table.py input.html output.json")
        return 2

    input_path = argv[1]
    output_path = argv[2]

    with open(input_path, 'r', encoding='utf-8') as f:
        html = f.read()

    monsters = parse_html_to_monsters(html)

    # write output JSON (overwrite)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(monsters, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(monsters)} monsters to {output_path}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))

"""
Utility script to consolidate monster data coming from community dumps.

Inputs (under wakfu_data/gamedata_1.90.1.43/community-data/):
- monsterDrops.json         → source for monster IDs that drop items
- monsterFamilies.json      → localized family names (FR/EN/ES/PT)
- en_monsters_stats_data.json → provides monster name (EN) and level range text

Output:
- wakfu_data/processed/monsters_metadata.json
  [{
      "monster_id": 5314,
      "name": {"en": "Cap'n Atcha"},
      "gfx_id": null,
      "family": {
          "id": 893,
          "names": {"fr": "...", "en": "...", "es": "...", "pt": "..."},
          "match": true
      },
      "level_min": 0,
      "level_max": 1
  }, ...]

Run:
    python worker/create_monster_metadata.py
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ROOT_DIR = Path(__file__).resolve().parents[1]
GAMEDATA_DIR = ROOT_DIR / "wakfu_data" / "gamedata_1.90.1.43"
COMMUNITY_DIR = GAMEDATA_DIR / "community-data"
OUTPUT_DIR = ROOT_DIR / "wakfu_data" / "processed"
OUTPUT_FILE = OUTPUT_DIR / "monsters_metadata.json"
SCRAP_DIR = COMMUNITY_DIR / "ScrapData_items"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def parse_level_range(level_text: Optional[str]) -> Tuple[Optional[int], Optional[int]]:
    """
    Parse strings like:
      "Level : 0 to 1"
      "Level : 215"
      "Level : 1 "
    Return (min_level, max_level) as integers when possible.
    """
    if not level_text:
        return None, None

    numbers = re.findall(r"\d+", level_text)
    if not numbers:
        return None, None

    min_level = int(numbers[0])
    max_level = int(numbers[-1])
    return min_level, max_level


def build_family_lookup(families: List[dict]) -> Dict[str, List[dict]]:
    """
    Build a lookup map using the English name (case-insensitive) as key.
    """
    lookup: Dict[str, List[dict]] = {}
    for entry in families:
        names = entry.get("name") or []
        if len(names) >= 2 and names[1]:
            lookup.setdefault(names[1].lower(), []).append(entry)
    return lookup


def build_scrap_monster_lookup() -> Dict[int, dict]:
    """
    Iterate over ScrapData_items files to gather monster names per language.
    Structure:
        {
            monster_id: {
                "names": {"en": "Gobball", "fr": "Bouftou"},
                "items": {2021, 2022, ...}
            },
            ...
        }
    """
    lookup: Dict[int, dict] = {}
    if not SCRAP_DIR.exists():
        return lookup

    scrap_files = sorted(SCRAP_DIR.glob("*.json"))
    for file_path in scrap_files:
        data = load_json(file_path)
        for item in data:
            item_id = item.get("id")
            droprates = item.get("droprates") or {}
            for lang, drops in droprates.items():
                if not isinstance(drops, dict):
                    continue
                for monster_name, drop_info in drops.items():
                    monster_id = drop_info.get("monster_id")
                    if not monster_id:
                        continue
                    try:
                        monster_id_int = int(monster_id)
                    except (TypeError, ValueError):
                        continue

                    entry = lookup.setdefault(
                        monster_id_int,
                        {"names": {}, "items": set()},
                    )
                    entry["names"][lang] = monster_name
                    if item_id:
                        entry["items"].add(item_id)

    # Convert sets to sorted lists for JSON serialization
    for entry in lookup.values():
        entry["items"] = sorted(entry["items"])

    return lookup


def main():
    print("🔎 Loading source data...")

    stats_path = COMMUNITY_DIR / "en_monsters_stats_data.json"
    scrap_lookup = build_scrap_monster_lookup()

    if not stats_path.exists():
        print("❌ Missing file:", stats_path)
        print("   Please restore the community monster stats dump before regenerating metadata.")
        return

    monster_drops = load_json(COMMUNITY_DIR / "monsterDrops.json")
    monster_stats = load_json(stats_path)

    families_path = COMMUNITY_DIR / "monsterFamilies.json"
    if families_path.exists():
        monster_families = load_json(families_path)
        families_lookup = build_family_lookup(monster_families)
    else:
        print("⚠️ monsterFamilies.json not found. Family information will be marked as unmatched.")
        families_lookup = {}

    drops_ids = {int(entry["id"]) for entry in monster_drops if entry.get("id") is not None}
    stats_by_id = {
        int(entry["monster_id"]): entry
        for entry in monster_stats
        if entry.get("monster_id") is not None
    }

    print(f"• Monsters in drops file: {len(drops_ids)}")
    print(f"• Monsters in stats file: {len(stats_by_id)}")
    print(f"• Families available: {len(families_lookup)}")

    missing_in_stats = sorted([monster_id for monster_id in drops_ids if monster_id not in stats_by_id])
    if missing_in_stats:
        print(f"⚠️ Monsters present in drops but missing in stats data: {len(missing_in_stats)}")
    else:
        print("✅ Every dropped monster has an entry in the stats file.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    enriched = []
    family_miss_counter = defaultdict(int)
    family_ambiguous_counter = defaultdict(list)

    for monster_id in sorted(drops_ids):
        stats_entry = stats_by_id.get(monster_id)
        monster_name = None
        family_name_en = None
        level_min = None
        level_max = None

        if stats_entry:
            monster_name = stats_entry.get("monster_name") or None
            family_name_en = stats_entry.get("monster_famille") or None
            level_min, level_max = parse_level_range(stats_entry.get("monster_level"))

        family_entry = None
        family_candidates: List[dict] = []
        if family_name_en:
            family_candidates = families_lookup.get(family_name_en.lower(), [])
            if family_candidates:
                # Prefer exact text match
                for candidate in family_candidates:
                    candidate_names = candidate.get("name") or []
                    en_candidate = candidate_names[1] if len(candidate_names) > 1 else None
                    if en_candidate == family_name_en:
                        family_entry = candidate
                        break

                if not family_entry:
                    # Fallback to first candidate when duplicates exist
                    family_entry = family_candidates[0]

                if len(family_candidates) > 1:
                    family_ambiguous_counter[family_name_en].extend(
                        [c.get("id") for c in family_candidates if c.get("id") is not None]
                    )
            else:
                family_miss_counter[family_name_en] += 1

        family_payload = None
        if family_entry:
            names = family_entry.get("name") or []
            family_payload = {
                "id": family_entry.get("id"),
                "names": {
                    "fr": names[0] if len(names) > 0 else None,
                    "en": names[1] if len(names) > 1 else None,
                    "es": names[2] if len(names) > 2 else None,
                    "pt": names[3] if len(names) > 3 else None,
                },
                "match": True,
            }
            if len(family_candidates) > 1:
                candidate_ids = sorted({c.get("id") for c in family_candidates if c.get("id") is not None})
                family_payload["candidate_ids"] = candidate_ids
        else:
            family_payload = {
                "id": None,
                "names": {"en": family_name_en} if family_name_en else {},
                "match": False,
            }

        # Resolve names from scrap data and stats
        name_payload: Dict[str, Optional[str]] = {}
        scrap_entry = scrap_lookup.get(monster_id)
        if scrap_entry:
            for lang, value in scrap_entry["names"].items():
                name_payload[lang] = value
        if monster_name:
            name_payload.setdefault("en", monster_name)

        # Normalize: remove empty values
        name_payload = {lang: value for lang, value in name_payload.items() if value}

        enrichment_notes = {}
        if scrap_entry:
            enrichment_notes["item_sources"] = scrap_entry["items"]

        monster_record = {
            "monster_id": monster_id,
            "name": name_payload,
            "gfx_id": None,
            "family": family_payload,
            "level_min": level_min,
            "level_max": level_max,
            "notes": enrichment_notes if enrichment_notes else None,
        }

        enriched.append(monster_record)

    output_payload = {
        "meta": {
            "source_version": "1.90.1.43",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "monsters_in_drops": len(drops_ids),
            "monsters_enriched": len(enriched),
            "missing_in_stats": len(missing_in_stats),
            "families_unmatched": len(family_miss_counter),
            "families_ambiguous": len(family_ambiguous_counter),
        },
        "monsters": enriched,
    }

    # Attach metadata YAML for cross-checking
    metadata_path = ROOT_DIR / "wakfu_data" / "processed" / "monsters_metadata.yaml"
    if metadata_path.exists():
        metadata_path.unlink()
    metadata_path.write_text(
        "# Compact YAML view of monster metadata for manual audits.\n"
        "# Use create_monster_metadata.py to regenerate JSON/YAML.\n",
        encoding="utf-8"
    )
    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(output_payload, f, ensure_ascii=False, indent=2)

    print(f"✅ Monsters metadata written to {OUTPUT_FILE.relative_to(ROOT_DIR)}")

    if missing_in_stats:
        sample = missing_in_stats[:10]
        print(f"   Missing monster IDs (sample): {sample}")

    if family_miss_counter:
        print("⚠️ Families that could not be matched:")
        for name, count in sorted(family_miss_counter.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"   • {name}  (monsters: {count})")
    else:
        print("✅ All monster families matched successfully.")

    if family_ambiguous_counter:
        print("ℹ️ Families with multiple candidates (showing up to 10):")
        for name, ids in list(family_ambiguous_counter.items())[:10]:
            print(f"   • {name} → candidates {sorted(set(ids))}")


if __name__ == "__main__":
    main()


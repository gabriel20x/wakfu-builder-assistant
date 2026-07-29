"""
Build static data for the 100% frontend version of Wakfu Builder Assistant.

Replaces the worker + PostgreSQL pipeline: reads raw Ankama gamedata JSON,
community data and manual metadata, and emits compact JSON files consumed
directly by the frontend (frontend/public/data/).

Usage:
    python scripts/build_static_data.py [--version 1.92.1.59]

Outputs:
    frontend/public/data/items.json         - processed equipment items (API ItemResponse shape)
    frontend/public/data/meta.json          - gamedata version, counts, monster types
    frontend/public/data/runes.json         - enchantment runes (engarces): color, values, restrictions
    frontend/public/data/sublimations.json  - sublimation scrolls with localized effect templates
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WAKFU_DATA = REPO_ROOT / "wakfu_data"

# ---------------------------------------------------------------------------
# Stat extraction (ported from worker/fetch_and_load.py extract_equipment_stats,
# extended with penalty Action IDs that the old pipeline silently dropped)
# ---------------------------------------------------------------------------

STAT_MAP = {
    # Core stats
    20: "HP",
    31: "AP",
    41: "MP",
    57: "MP_Penalty",
    1020: "WP",
    191: "WP",
    # Critical
    150: "Critical_Hit",
    96: "Critical_Mastery",
    97: "Critical_Mastery",
    149: "Critical_Mastery",
    162: "Critical_Resistance",
    988: "Critical_Resistance",
    # Damage and healing
    122: "Healing_Mastery",
    1023: "Healing_Mastery",
    1058: "Heals_Performed",
    # Elemental Masteries
    120: "Elemental_Mastery",
    130: "Fire_Mastery",
    131: "Water_Mastery",
    132: "Earth_Mastery",
    133: "Air_Mastery",
    171: "Initiative",
    1068: "Multi_Element_Mastery",
    # Elemental Resistances
    80: "Elemental_Resistance",
    82: "Fire_Resistance",
    83: "Water_Resistance",
    84: "Earth_Resistance",
    85: "Air_Resistance",
    151: "Water_Resistance",
    152: "Earth_Resistance",
    153: "Air_Resistance",
    160: "Range_or_Elemental_Res",  # contextual
    1069: "Random_Elemental_Resistance",
    # Position Masteries
    166: "Rear_Mastery",
    1052: "Melee_Mastery",
    175: "Dodge_or_Berserk",  # contextual
    1053: "Distance_Mastery",
    1055: "Armor_or_Berserk",  # contextual
    # Resistances
    167: "Rear_Resistance",
    71: "Rear_Resistance",
    # Movement and positioning
    173: "Lock",
    180: "Lock_or_Rear_Mastery",  # contextual
    181: "Rear_Mastery_Penalty",
    184: "Control",
    875: "Block",
    832: "Control",
    # Penalties (negative stats)
    21: "HP_Penalty",
    168: "Critical_Hit_Penalty",
    174: "Lock_Penalty",
    176: "Dodge_Penalty",
    192: "WP_Penalty",
    # Other
    193: "Prospecting",
    # Armor
    1056: "Armor_Received",
    26: "Armor_or_Healing",  # contextual
    # Force of Will
    177: "Force_Of_Will",
    # Percentages
    39: "Heals_Received_or_Armor_Given",  # contextual
    # Special effects - skip
    304: None,
    400: None,
    # Additional
    123: "Dodge",
    124: "Lock",
    125: "Initiative",
    # --- Penalty Action IDs missing from the legacy pipeline ---
    40: None,                        # generic scripted effect, not a stat
    56: "AP_Penalty",                # -N max AP
    90: "Elemental_Resistance_Penalty",
    98: "Water_Resistance_Penalty",
    100: "Elemental_Resistance_Penalty",
    161: "Range_Penalty",
    172: "Initiative_Penalty",
    876: "Block_Penalty",
    1059: "Melee_Mastery_Penalty",
    1060: "Distance_Mastery_Penalty",
    1061: "Berserk_Mastery_Penalty",
    1062: "Critical_Resistance_Penalty",
    1063: "Rear_Resistance_Penalty",
    2001: None,                      # % harvesting quantity, not a combat stat
}

PENALTIES = {
    "HP_Penalty": "HP",
    "Critical_Hit_Penalty": "Critical_Hit",
    "Lock_Penalty": "Lock",
    "Dodge_Penalty": "Dodge",
    "Rear_Mastery_Penalty": "Rear_Mastery",
    "WP_Penalty": "WP",
    "MP_Penalty": "MP",
    "AP_Penalty": "AP",
    "Elemental_Resistance_Penalty": "Elemental_Resistance",
    "Water_Resistance_Penalty": "Water_Resistance",
    "Range_Penalty": "Range",
    "Initiative_Penalty": "Initiative",
    "Block_Penalty": "Block",
    "Melee_Mastery_Penalty": "Melee_Mastery",
    "Distance_Mastery_Penalty": "Distance_Mastery",
    "Berserk_Mastery_Penalty": "Berserk_Mastery",
    "Critical_Resistance_Penalty": "Critical_Resistance",
    "Rear_Resistance_Penalty": "Rear_Resistance",
}

RARITY_MAP = {1: 1, 2: 3, 3: 4, 4: 5, 5: 6, 6: 6, 7: 7}

RARITY_SCORES = {0: 0, 1: 5, 2: 10, 3: 15, 4: 30, 5: 50, 6: 45, 7: 40}

# ---------------------------------------------------------------------------
# Enchantment system (engarces): runes and sublimations
# ---------------------------------------------------------------------------

SUBLIMATION_TYPE_ID = 812   # itemTypeId of sublimation scrolls
RUNE_TYPE_ID = 811          # itemTypeId of enchantment runes (shards)
STATE_ACTION_ID = 304       # equipEffect action "applies a state"

# itemProperties.json: 19 = EPIC_GEMMABLE, 20 = RELIC_GEMMABLE (special PvP gear
# that grants the epic/relic sublimation slot without being epic/relic rarity)
EPIC_GEMMABLE_PROP = 19
RELIC_GEMMABLE_PROP = 20

# Deprecated runes still present in gamedata but removed from the live game
# (single-target / area mastery were merged into the other mastery runes)
DEPRECATED_RUNE_IDS = {27095, 27096}

# Per-rune-level stat values. Gamedata only ships the shard leveling curves,
# not the stat amounts, so these come from Wakforge (MIT, Tmktahu/wakforge
# src/models/useStats.js) which hardcodes the same in-game tables.
RUNE_VALUES_MASTERY = [1, 3, 4, 6, 7, 10, 15, 19, 24, 30, 33]
RUNE_VALUES_RESISTANCE = [2, 5, 7, 10, 12, 15, 17, 20, 22, 25, 27]
RUNE_VALUES_DODGE_LOCK = [3, 6, 9, 12, 15, 21, 30, 39, 48, 60, 66]
RUNE_VALUES_ELEM_MASTERY = [1, 2, 3, 4, 5, 7, 10, 13, 16, 20, 22]
RUNE_VALUES_INITIATIVE = [2, 4, 6, 8, 10, 14, 20, 26, 32, 40, 44]
RUNE_VALUES_HEALTH = [4, 8, 12, 16, 20, 28, 40, 52, 64, 80, 88]

# rune item_id -> (stat key in useStats.js vocabulary, per-level values)
RUNE_DEFS = {
    27094: ("Elemental_Mastery", RUNE_VALUES_ELEM_MASTERY),
    27097: ("Melee_Mastery", RUNE_VALUES_MASTERY),
    27098: ("Distance_Mastery", RUNE_VALUES_MASTERY),
    27099: ("Berserk_Mastery", RUNE_VALUES_MASTERY),
    27100: ("Critical_Mastery", RUNE_VALUES_MASTERY),
    27101: ("Rear_Mastery", RUNE_VALUES_MASTERY),
    27102: ("Lock", RUNE_VALUES_DODGE_LOCK),
    27103: ("Dodge", RUNE_VALUES_DODGE_LOCK),
    27104: ("Initiative", RUNE_VALUES_INITIATIVE),
    27105: ("Fire_Resistance", RUNE_VALUES_RESISTANCE),
    27106: ("Water_Resistance", RUNE_VALUES_RESISTANCE),
    27107: ("Earth_Resistance", RUNE_VALUES_RESISTANCE),
    27108: ("Air_Resistance", RUNE_VALUES_RESISTANCE),
    27109: ("HP", RUNE_VALUES_HEALTH),
    27110: ("Healing_Mastery", RUNE_VALUES_MASTERY),
}

# shardsParameters.doubleBonusPosition raw ids -> equipment slot keys
RAW_SLOT_IDS = {
    0: "HEAD",
    3: "SHOULDERS",
    4: "NECK",
    5: "CHEST",
    7: "LEFT_HAND",
    8: "RIGHT_HAND",
    10: "BELT",
    12: "LEGS",
    13: "BACK",
    15: "FIRST_WEAPON",
}

# "stackable up to level N" in the scroll description (es/en), used for max_stack
MAX_STACK_PATTERNS = [
    re.compile(r"nivel de (\d+)"),
    re.compile(r"level of (\d+)"),
]


def load_json(path: Path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"WARNING: missing {path}")
        return []


def extract_equipment_stats(item_data: dict, slot: str = None) -> dict:
    stats = {}
    effects = item_data.get("definition", {}).get("equipEffects", [])

    for effect in effects:
        effect_def = effect.get("effect", {}).get("definition", {})
        action_id = effect_def.get("actionId")
        params = effect_def.get("params", [])

        if action_id == 1068 and len(params) >= 3:
            mastery_value = params[0]
            num_elements = int(params[2]) if len(params) > 2 else 0
            stat_key = f"Multi_Element_Mastery_{num_elements}"
            stats[stat_key] = stats.get(stat_key, 0) + mastery_value
            continue
        if action_id == 1069 and len(params) >= 3:
            resist_value = params[0]
            num_elements = int(params[2]) if len(params) > 2 else 0
            stat_key = f"Random_Elemental_Resistance_{num_elements}"
            stats[stat_key] = stats.get(stat_key, 0) + resist_value
            continue

        stat_name = STAT_MAP.get(action_id)
        if not stat_name or not params:
            continue
        stat_value = params[0]

        # Contextual stats (same rules as legacy pipeline)
        if stat_name == "Range_or_Elemental_Res":
            range_slots = ["FIRST_WEAPON", "SECOND_WEAPON", "HEAD", "NECK", "SHOULDERS"]
            stat_name = "Range" if slot in range_slots else "Elemental_Resistance"
        elif stat_name == "Heals_Received_or_Armor_Given":
            stat_name = "Armor_Given" if slot in ["NECK", "SHOULDERS"] else "Heals_Received"
        elif stat_name == "Lock_or_Rear_Mastery":
            stat_name = "Rear_Mastery" if slot == "NECK" else "Lock"
        elif stat_name == "Dodge_or_Berserk":
            if slot in ["FIRST_WEAPON", "HEAD", "SHOULDERS", "SECOND_WEAPON"]:
                stat_name = "Dodge" if stat_value < 250 else "Berserk_Mastery"
            else:
                stat_name = "Dodge" if stat_value < 100 else "Berserk_Mastery"
        elif stat_name == "Armor_or_Berserk":
            stat_name = "Armor_Given" if stat_value <= 50 else "Berserk_Mastery"
        elif stat_name == "Armor_or_Healing":
            stat_name = "Healing_Mastery" if slot == "BACK" else "Armor_Received"

        if stat_name in PENALTIES:
            stat_name = PENALTIES[stat_name]
            stat_value = -stat_value

        stats[stat_name] = stats.get(stat_name, 0) + stat_value

    return stats


def calculate_difficulty(level, rarity, is_epic, is_relic, source_type):
    difficulty = min(20.0, level / 245.0 * 20.0)
    difficulty += RARITY_SCORES.get(rarity, 5)
    if is_epic:
        difficulty += 20
    if is_relic:
        difficulty += 25
    if source_type == "harvest":
        difficulty += 3
    elif source_type == "recipe":
        difficulty += 8
    elif source_type == "drop":
        difficulty += 15
    elif source_type == "special":
        difficulty += 5
    return min(100.0, difficulty)


def build_monster_lookup(monsters_metadata):
    lookup = {}
    families = {}
    for entry in (monsters_metadata or {}).get("monsters", []):
        monster_id = entry.get("monster_id")
        if monster_id is None:
            continue
        lookup[monster_id] = entry
        family = entry.get("family") or {}
        family_id = family.get("id")
        if family_id is not None:
            fam = families.setdefault(family_id, {"id": family_id, "names": {}})
            for lang, value in (family.get("names") or {}).items():
                if value and not fam["names"].get(lang):
                    fam["names"][lang] = value
    return lookup, families


def build_drop_sources(monster_drops_data, monster_lookup, families):
    """item_id -> list of drop source dicts (mirrors API DropSourceResponse)."""
    by_item = {}
    for entry in monster_drops_data or []:
        monster_id = entry.get("id")
        drops = entry.get("drops", [])
        if not monster_id or not isinstance(drops, list):
            continue
        monster = monster_lookup.get(monster_id) or {}
        names = monster.get("name") or {}
        family_info = monster.get("family") or {}
        family_id = family_info.get("id")
        family = None
        if family_id is not None and family_id in families:
            family = {
                "id": family_id,
                "names": families[family_id]["names"] or None,
                "match": True,
            }
        gfx = monster.get("gfx_id") or monster_id
        monster_name = (
            names.get("en") or names.get("fr") or names.get("es") or names.get("pt")
            or f"Monster {monster_id}"
        )
        for drop in drops:
            item_id = drop.get("itemId")
            rate_value = drop.get("rate")
            if not item_id or rate_value is None:
                continue
            try:
                rate_percent = float(rate_value)
            except (TypeError, ValueError):
                continue
            by_item.setdefault(item_id, []).append({
                "monster_id": monster_id,
                "monster_name": monster_name,
                "monster_names": {k: v for k, v in names.items() if v} or None,
                "monster_type": monster.get("type"),
                "family": family,
                "level_min": monster.get("level_min"),
                "level_max": monster.get("level_max"),
                "drop_rate": rate_percent / 100.0,
                "drop_rate_percent": rate_percent,
                "image_url": f"https://vertylo.github.io/wakassets/monsters/{gfx}.png",
            })
    return by_item


def localized(title: dict, fallback: str = "") -> dict:
    """Normalize an Ankama title/description block to {en, es, fr}."""
    title = title or {}
    en = title.get("en") or title.get("fr") or fallback
    return {
        "en": en,
        "es": title.get("es") or en,
        "fr": title.get("fr") or en,
    }


def extract_state_effect(item_data: dict):
    """Return (state_id, state_level) from the first actionId-304 equip effect."""
    for effect in item_data.get("definition", {}).get("equipEffects", []):
        effect_def = effect.get("effect", {}).get("definition", {})
        if effect_def.get("actionId") == STATE_ACTION_ID and effect_def.get("params"):
            params = effect_def["params"]
            state_id = int(params[0])
            state_level = int(params[2]) if len(params) > 2 else 1
            return state_id, state_level
    return None, None


def build_wakforge_effects(wakforge_dir: Path):
    """state_id -> {name_key, lines: [{text: {en,es,fr}, indented, nums: {num_N: [per-level]}}]}."""
    state_data = load_json(wakforge_dir / "state_data.json")
    translations = {
        lang: load_json(wakforge_dir / f"{lang}_states.json")
        for lang in ("en", "es", "fr")
    }

    def translate(key):
        return {
            lang: translations[lang].get(key) or translations["en"].get(key) or ""
            for lang in ("en", "es", "fr")
        }

    effects = {}
    for state in state_data or []:
        try:
            state_id = int(state.get("id"))
        except (TypeError, ValueError):
            continue
        lines = []
        for part in state.get("descriptionData", []):
            nums = {}
            for key, per_level in part.items():
                if key.startswith("num_") and isinstance(per_level, dict):
                    ordered = sorted(
                        per_level.items(),
                        key=lambda kv: int(kv[0].rsplit("_", 1)[1]),
                    )
                    nums[key] = [v for _, v in ordered]
            lines.append({
                "text": translate(part.get("text", "")),
                "indented": bool(part.get("indented")),
                "nums": nums or None,
            })
        effects[state_id] = {"lines": lines}
    return effects


def parse_max_stack(description: dict):
    for lang in ("es", "en"):
        text = (description or {}).get(lang) or ""
        for pattern in MAX_STACK_PATTERNS:
            match = pattern.search(text)
            if match:
                return int(match.group(1))
    return None


def build_sublimations(items_data, wakforge_effects, states_by_id):
    subs = []
    missing_effects = 0
    for item_data in items_data:
        item_def = item_data.get("definition", {}).get("item", {})
        if item_def.get("baseParameters", {}).get("itemTypeId") != SUBLIMATION_TYPE_ID:
            continue
        sub_params = item_def.get("sublimationParameters", {}) or {}
        state_id, state_level = extract_state_effect(item_data)
        effect = wakforge_effects.get(state_id) if state_id is not None else None
        if effect is None:
            missing_effects += 1
        state_title = states_by_id.get(state_id)
        subs.append({
            "id": item_def.get("id"),
            "name": localized(item_data.get("title"), f"Sublimation {item_def.get('id')}"),
            "rarity": item_def.get("baseParameters", {}).get("rarity", 0),
            "gfx_id": item_def.get("graphicParameters", {}).get("gfxId"),
            "pattern": sub_params.get("slotColorPattern") or [],
            "is_epic": bool(sub_params.get("isEpic")),
            "is_relic": bool(sub_params.get("isRelic")),
            "state_id": state_id,
            "state_level": state_level,
            "max_stack": parse_max_stack(item_data.get("description")),
            "state_name": localized(state_title) if state_title else None,
            "effect": effect,
        })
    subs.sort(key=lambda s: (s["name"]["es"], s["id"]))
    return subs, missing_effects


def build_runes(items_data):
    runes = []
    for item_data in items_data:
        item_def = item_data.get("definition", {}).get("item", {})
        item_id = item_def.get("id")
        shards = item_def.get("shardsParameters")
        if not shards or item_id in DEPRECATED_RUNE_IDS:
            continue
        stat_def = RUNE_DEFS.get(item_id)
        if not stat_def:
            print(f"WARNING: rune {item_id} has no stat mapping, skipped")
            continue
        stat_key, values = stat_def
        runes.append({
            "id": item_id,
            "name": localized(item_data.get("title"), f"Rune {item_id}"),
            "color": shards.get("color"),  # 1=red, 2=green, 3=blue
            "gfx_id": item_def.get("graphicParameters", {}).get("gfxId"),
            "stat": stat_key,
            "values": values,  # index = rune level - 1
            "level_requirements": shards.get("shardLevelRequirement") or [],
            "double_bonus_slots": [
                RAW_SLOT_IDS[raw] for raw in (shards.get("doubleBonusPosition") or [])
                if raw in RAW_SLOT_IDS
            ],
        })
    runes.sort(key=lambda r: (r["color"], r["name"]["es"]))
    return runes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", default="1.92.1.59")
    parser.add_argument("--community-version", default="1.90.1.43",
                        help="gamedata dir whose community-data/ to use")
    parser.add_argument("--out", default=str(REPO_ROOT / "frontend" / "public" / "data"))
    args = parser.parse_args()

    gamedata = WAKFU_DATA / f"gamedata_{args.version}"
    community = WAKFU_DATA / f"gamedata_{args.community_version}" / "community-data"
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Gamedata:  {gamedata}")
    print(f"Community: {community}")

    items_data = load_json(gamedata / "items.json")
    equipment_types = load_json(gamedata / "equipmentItemTypes.json")
    recipe_results = load_json(gamedata / "recipeResults.json")
    harvest_loots = load_json(gamedata / "harvestLoots.json")
    states_data = load_json(gamedata / "states.json")
    wakforge_effects = build_wakforge_effects(WAKFU_DATA / "community-sourced" / "wakforge")
    states_by_id = {
        s.get("definition", {}).get("id"): s.get("title")
        for s in states_data or []
    }

    monster_drops_data = load_json(community / "monsterDrops.json")
    monsters_metadata = load_json(WAKFU_DATA / "processed" / "monsters_metadata.json")
    metadata_file = load_json(WAKFU_DATA / "item_metadata.json")
    item_metadata = metadata_file.get("items", {}) if isinstance(metadata_file, dict) else {}

    equipment_types_map = {et["definition"]["id"]: et for et in equipment_types}
    recipes_map = {}
    for result in recipe_results:
        rid = result.get("productedItemId")
        if rid and result.get("recipeId"):
            recipes_map[rid] = result["recipeId"]
    harvest_map = {loot["itemId"]: loot for loot in harvest_loots if loot.get("itemId")}

    monster_lookup, families = build_monster_lookup(monsters_metadata)
    drop_sources_by_item = build_drop_sources(monster_drops_data, monster_lookup, families)

    items_out = []
    # Distinct monsters per type (mirrors the old /gamedata/monster-types counts)
    monster_type_counts = Counter(
        m.get("type") for m in monster_lookup.values() if m.get("type")
    )

    for item_data in items_data:
        definition = item_data.get("definition", {})
        item_def = definition.get("item", {})
        item_id = item_def.get("id")
        if not item_id:
            continue

        item_type_id = item_def.get("baseParameters", {}).get("itemTypeId")
        if not item_type_id:
            continue
        equipment_def = equipment_types_map.get(item_type_id, {}).get("definition", {})
        positions = equipment_def.get("equipmentPositions", [])
        slot = positions[0] if positions else None
        if not slot:
            continue

        level = item_def.get("level", 0)
        rarity_raw = item_def.get("baseParameters", {}).get("rarity", 0)
        rarity = RARITY_MAP.get(rarity_raw, rarity_raw)
        is_epic = rarity == 7
        is_relic = rarity_raw == 5  # only true Relics, not "Recuerdo" (raw 6)

        shard_slots = item_def.get("baseParameters", {}).get("maximumShardSlotNumber", 0)
        properties = item_def.get("properties") or []
        epic_gem_slot = is_epic or EPIC_GEMMABLE_PROP in properties
        relic_gem_slot = is_relic or RELIC_GEMMABLE_PROP in properties

        blocks_second_weapon = (
            slot == "FIRST_WEAPON"
            and "SECOND_WEAPON" in equipment_def.get("equipmentDisabledPositions", [])
        )

        title = item_data.get("title", {})
        name_en = title.get("en", f"Item {item_id}")
        name_es = title.get("es", name_en)
        name_fr = title.get("fr", name_en)

        gfx_id = item_def.get("graphicParameters", {}).get("gfxId")
        stats = extract_equipment_stats(item_data, slot)

        if item_id in harvest_map:
            source_type = "harvest"
        elif item_id in recipes_map:
            source_type = "recipe"
        elif item_id < 10000:
            source_type = "special"
        else:
            source_type = "drop"

        metadata = item_metadata.get(str(item_id), {})
        if metadata:
            acq = metadata.get("acquisition_methods", {})
            if acq:
                if acq.get("recipe", {}).get("enabled"):
                    source_type = "recipe"
                elif acq.get("fragments", {}).get("enabled"):
                    source_type = "drop"
                elif acq.get("drop", {}).get("enabled"):
                    source_type = "drop"
                elif acq.get("crupier", {}).get("enabled"):
                    source_type = "special"
                elif acq.get("challenge_reward", {}).get("enabled"):
                    source_type = "special"
                elif acq.get("quest", {}).get("enabled"):
                    source_type = "special"

        difficulty = calculate_difficulty(level, rarity, is_epic, is_relic, source_type)
        if metadata.get("manual_difficulty_override") is not None:
            difficulty = metadata["manual_difficulty_override"]

        drop_sources = drop_sources_by_item.get(item_id, [])

        items_out.append({
            "item_id": item_id,
            "name": name_en,
            "name_en": name_en,
            "name_es": name_es,
            "name_fr": name_fr,
            "level": level,
            "rarity": rarity,
            "slot": slot,
            "is_epic": is_epic,
            "is_relic": is_relic,
            "has_gem_slot": epic_gem_slot or relic_gem_slot,
            "shard_slots": shard_slots,
            "epic_gem_slot": epic_gem_slot,
            "relic_gem_slot": relic_gem_slot,
            "blocks_second_weapon": blocks_second_weapon,
            "source_type": source_type,
            "difficulty": difficulty,
            "manual_drop_difficulty": None,
            "gfx_id": gfx_id,
            "stats": stats,
            "drop_sources": drop_sources,
            "metadata": metadata or None,
        })

    items_out.sort(key=lambda i: i["item_id"])

    items_path = out_dir / "items.json"
    with open(items_path, "w", encoding="utf-8") as f:
        json.dump(items_out, f, ensure_ascii=False, separators=(",", ":"))

    sublimations, missing_effects = build_sublimations(
        items_data, wakforge_effects, states_by_id
    )
    sublimations_path = out_dir / "sublimations.json"
    with open(sublimations_path, "w", encoding="utf-8") as f:
        json.dump({
            "attribution": "Effect templates from Tmktahu/wakforge (MIT)",
            "sublimations": sublimations,
        }, f, ensure_ascii=False, separators=(",", ":"))

    runes = build_runes(items_data)
    runes_path = out_dir / "runes.json"
    with open(runes_path, "w", encoding="utf-8") as f:
        json.dump({
            "attribution": "Per-level stat values from Tmktahu/wakforge (MIT)",
            "runes": runes,
        }, f, ensure_ascii=False, separators=(",", ":"))

    meta = {
        "gamedata_version": args.version,
        "community_data_version": args.community_version,
        "item_count": len(items_out),
        "sublimation_count": len(sublimations),
        "rune_count": len(runes),
        "monster_types": sorted(monster_type_counts.keys()),
        "monster_type_counts": dict(sorted(monster_type_counts.items())),
        "status": "completed",
    }
    with open(out_dir / "meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    size_mb = items_path.stat().st_size / 1024 / 1024
    print(f"Wrote {len(items_out)} items -> {items_path} ({size_mb:.1f} MB)")
    print(f"Wrote {len(sublimations)} sublimations -> {sublimations_path} "
          f"({missing_effects} without Wakforge effect template)")
    print(f"Wrote {len(runes)} runes -> {runes_path}")
    print(f"Monster types: {meta['monster_types']}")


if __name__ == "__main__":
    main()

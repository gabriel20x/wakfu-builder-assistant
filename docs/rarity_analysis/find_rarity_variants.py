"""
Find all rarity variants of items by analyzing item names and comparing stats
"""
import json
import re
from collections import defaultdict
from pathlib import Path

# Load items.json
items_path = Path("wakfu_data/gamedata_1.90.1.43/items.json")
print(f"Loading {items_path}...")

with open(items_path, 'r', encoding='utf-8') as f:
    items_data = json.load(f)

print(f"Total items loaded: {len(items_data)}\n")

# We need to extract item names - they're in title.en/es/fr
# Let's build a comprehensive map

items_info = []

for item in items_data:
    if 'definition' not in item or 'item' not in item['definition']:
        continue
    
    item_def = item['definition']['item']
    item_id = item_def.get('id')
    level = item_def.get('level', 0)
    rarity = item_def.get('baseParameters', {}).get('rarity', 0)
    item_type_id = item_def.get('baseParameters', {}).get('itemTypeId')
    
    # Get title (name)
    title = item.get('title', {})
    name_en = title.get('en', '')
    name_es = title.get('es', '')
    name_fr = title.get('fr', '')
    
    # Get equip effects for stat comparison
    equip_effects = item.get('definition', {}).get('equipEffects', [])
    
    items_info.append({
        'item_id': item_id,
        'level': level,
        'rarity': rarity,
        'item_type_id': item_type_id,
        'name_en': name_en,
        'name_es': name_es,
        'name_fr': name_fr,
        'equip_effects': equip_effects,
        'full_data': item
    })

# Group items by name (using Spanish for the examples from screenshot)
items_by_name = defaultdict(list)

for item in items_info:
    # Use Spanish name as key (lowercase, no accents for matching)
    name_key = item['name_es'].lower().strip()
    if name_key:
        items_by_name[name_key].append(item)

print("="*80)
print("SEARCHING FOR ITEMS FROM SCREENSHOTS")
print("="*80)

# Look for the specific items from the screenshots
target_names = ['la punzante', 'abrakapa', 'abrakasco']

rarity_names = {
    1: "Común (blanco)",
    2: "Común (verde claro)", 
    3: "Raro (verde)",
    4: "Mítico (naranja)",
    5: "Legendario (dorado)",
    6: "Reliquia (rosa)",
    7: "Épico (morado)"
}

detailed_findings = {}

for target_name in target_names:
    print(f"\n{'='*80}")
    print(f"ITEM: {target_name.upper()}")
    print(f"{'='*80}")
    
    if target_name not in items_by_name:
        print(f"  ❌ NOT FOUND in gamedata")
        continue
    
    variants = items_by_name[target_name]
    print(f"  ✅ Found {len(variants)} variant(s)\n")
    
    # Sort by rarity
    variants.sort(key=lambda x: x['rarity'])
    
    detailed_findings[target_name] = []
    
    for variant in variants:
        print(f"  📦 Item ID: {variant['item_id']}")
        print(f"     Rarity: {variant['rarity']} - {rarity_names.get(variant['rarity'], 'Unknown')}")
        print(f"     Level: {variant['level']}")
        print(f"     Type ID: {variant['item_type_id']}")
        print(f"     Name ES: {variant['name_es']}")
        print(f"     Name EN: {variant['name_en']}")
        
        # Extract stats from equipEffects
        print(f"     Stats:")
        for effect in variant['equip_effects']:
            effect_def = effect.get('effect', {}).get('definition', {})
            action_id = effect_def.get('actionId')
            params = effect_def.get('params', [])
            if params:
                print(f"       - ActionID {action_id}: params = {params}")
        
        print()
        
        detailed_findings[target_name].append({
            'item_id': variant['item_id'],
            'rarity': variant['rarity'],
            'level': variant['level'],
            'type_id': variant['item_type_id'],
            'equip_effects': variant['equip_effects']
        })

# Analyze stat scaling patterns
print("\n" + "="*80)
print("STAT SCALING ANALYSIS")
print("="*80)

for item_name, variants in detailed_findings.items():
    if len(variants) < 2:
        continue
    
    print(f"\n{item_name.upper()}:")
    print(f"  Found {len(variants)} rarity variants")
    
    # Compare stats across rarities
    stats_by_rarity = {}
    
    for variant in variants:
        rarity = variant['rarity']
        stats = {}
        
        for effect in variant['equip_effects']:
            effect_def = effect.get('effect', {}).get('definition', {})
            action_id = effect_def.get('actionId')
            params = effect_def.get('params', [])
            
            if params:
                # For simplicity, use first param as the stat value
                stats[action_id] = params[0] if len(params) > 0 else None
        
        stats_by_rarity[rarity] = stats
    
    # Find common action IDs across all rarities
    all_action_ids = set()
    for stats in stats_by_rarity.values():
        all_action_ids.update(stats.keys())
    
    if all_action_ids:
        print(f"\n  Stat comparison across rarities:")
        print(f"  {'ActionID':<12} {'Rarity 3':<12} {'Rarity 4':<12} {'Rarity 5':<12} {'Scaling Pattern'}")
        print(f"  {'-'*70}")
        
        for action_id in sorted(all_action_ids):
            values = []
            for rarity in [3, 4, 5]:
                if rarity in stats_by_rarity:
                    value = stats_by_rarity[rarity].get(action_id, '-')
                    values.append(value)
                else:
                    values.append('-')
            
            # Calculate scaling if we have numeric values
            scaling_pattern = "N/A"
            numeric_values = [v for v in values if isinstance(v, (int, float))]
            if len(numeric_values) >= 2:
                ratios = []
                for i in range(1, len(numeric_values)):
                    if numeric_values[i-1] != 0:
                        ratio = numeric_values[i] / numeric_values[i-1]
                        ratios.append(f"{ratio:.2f}x")
                scaling_pattern = " → ".join(ratios)
            
            val_str = [f"{v:>10}" if isinstance(v, (int, float)) else f"{str(v):>10}" for v in values]
            print(f"  {action_id:<12} {val_str[0]:<12} {val_str[1]:<12} {val_str[2]:<12} {scaling_pattern}")

# Save detailed findings
output_data = {}
for item_name, variants in detailed_findings.items():
    output_data[item_name] = []
    for variant in variants:
        # Extract clean stat data
        stats = {}
        for effect in variant['equip_effects']:
            effect_def = effect.get('effect', {}).get('definition', {})
            action_id = effect_def.get('actionId')
            params = effect_def.get('params', [])
            stats[f"action_{action_id}"] = params
        
        output_data[item_name].append({
            'item_id': variant['item_id'],
            'rarity': variant['rarity'],
            'level': variant['level'],
            'stats': stats
        })

with open('rarity_variants_detailed.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"\n\n✅ Detailed findings saved to: rarity_variants_detailed.json")


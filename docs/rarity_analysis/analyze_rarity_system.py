"""
Script to analyze the rarity system in Wakfu items
Investigates if items have multiple rarity versions and how stats scale
"""
import json
from collections import defaultdict
from pathlib import Path

# Load items.json with proper encoding
items_path = Path("wakfu_data/gamedata_1.90.1.43/items.json")
print(f"Loading {items_path}...")

with open(items_path, 'r', encoding='utf-8') as f:
    items_data = json.load(f)

print(f"Total items loaded: {len(items_data)}")

# Analyze item structure and rarity distribution
items_by_id = defaultdict(list)
rarity_distribution = defaultdict(int)
items_with_name = {}

for item in items_data:
    if 'definition' not in item or 'item' not in item['definition']:
        continue
    
    item_def = item['definition']['item']
    item_id = item_def.get('id')
    rarity = item_def.get('baseParameters', {}).get('rarity', 0)
    level = item_def.get('level', 0)
    
    # Track rarity distribution
    rarity_distribution[rarity] += 1
    
    # Track items by ID (to see if same ID appears multiple times)
    items_by_id[item_id].append({
        'rarity': rarity,
        'level': level,
        'item': item
    })
    
    # Try to extract name for reference
    if item_id not in items_with_name:
        items_with_name[item_id] = item

print("\n" + "="*80)
print("RARITY DISTRIBUTION")
print("="*80)
rarity_names = {
    0: "Sin rareza",
    1: "Común (blanco)",
    2: "Común (verde claro)", 
    3: "Raro (verde)",
    4: "Mítico (naranja)",
    5: "Legendario (dorado)",
    6: "Reliquia (rosa)",
    7: "Épico (morado)"
}

for rarity in sorted(rarity_distribution.keys()):
    name = rarity_names.get(rarity, f"Desconocido ({rarity})")
    count = rarity_distribution[rarity]
    print(f"  Rarity {rarity} ({name}): {count} items")

print("\n" + "="*80)
print("ITEMS WITH MULTIPLE RARITY VERSIONS (Same ID)")
print("="*80)

multi_rarity_items = {k: v for k, v in items_by_id.items() if len(v) > 1}

print(f"Found {len(multi_rarity_items)} items with multiple entries (same ID)")
if len(multi_rarity_items) > 0:
    print("\nFirst 10 examples:")
    for i, (item_id, versions) in enumerate(list(multi_rarity_items.items())[:10]):
        rarities = [v['rarity'] for v in versions]
        levels = [v['level'] for v in versions]
        print(f"  Item ID {item_id}: Rarities {rarities}, Levels {levels}")

# Now check: Are "Abrakapa", "Abrakasco", "La punzante" multiple items with different IDs?
print("\n" + "="*80)
print("SEARCHING FOR EXAMPLE ITEMS FROM IMAGES")
print("="*80)

# We need to search by level and see if there are items with similar stats
# Let's look for items around level 125-140 (from the images)
target_items = {
    23145: "La punzante (from screenshot)"
}

print("\nChecking specific items:")
for item_id, description in target_items.items():
    if item_id in items_by_id:
        versions = items_by_id[item_id]
        print(f"\n{description} (ID {item_id}):")
        for v in versions:
            print(f"  - Rarity {v['rarity']} ({rarity_names.get(v['rarity'])}), Level {v['level']}")
    else:
        print(f"\n{description} (ID {item_id}): NOT FOUND")

# Let's also search for items with the same level and itemTypeId
print("\n" + "="*80)
print("INVESTIGATING: Items with same level/type but different rarities")
print("="*80)

items_by_type_level = defaultdict(list)

for item_id, versions in items_by_id.items():
    for v in versions:
        item_def = v['item']['definition']['item']
        item_type_id = item_def.get('baseParameters', {}).get('itemTypeId')
        level = v['level']
        rarity = v['rarity']
        
        items_by_type_level[(item_type_id, level)].append({
            'item_id': item_id,
            'rarity': rarity,
            'full_data': v['item']
        })

# Find cases where same type+level has multiple rarities
print("\nLooking for (itemTypeId, level) combinations with multiple rarities...")
multi_rarity_combos = {}

for (item_type_id, level), items_list in items_by_type_level.items():
    rarities = set(item['rarity'] for item in items_list)
    if len(rarities) > 1:
        multi_rarity_combos[(item_type_id, level)] = items_list

print(f"\nFound {len(multi_rarity_combos)} (type, level) combinations with multiple rarities")

# Show examples for level 125 (La punzante level)
print("\nExamples at level 125:")
level_125_examples = [(k, v) for k, v in multi_rarity_combos.items() if k[1] == 125]

for (item_type_id, level), items_list in level_125_examples[:5]:
    print(f"\nType {item_type_id}, Level {level}:")
    for item in items_list[:5]:
        print(f"  - Item ID {item['item_id']}, Rarity {item['rarity']} ({rarity_names.get(item['rarity'])})")

print("\n" + "="*80)
print("CONCLUSION")
print("="*80)
print("""
Based on this analysis, we need to determine:
1. Are items with different rarities DIFFERENT item IDs?
2. Or is rarity stored as a property of the same item ID?
3. How do the stats scale with rarity?
""")

# Save results for further analysis
results = {
    'total_items': len(items_data),
    'rarity_distribution': dict(rarity_distribution),
    'multi_id_items': len(multi_rarity_items),
    'multi_type_level_combos': len(multi_rarity_combos),
    'examples': []
}

# Add some examples
for (item_type_id, level), items_list in list(multi_rarity_combos.items())[:20]:
    results['examples'].append({
        'type_id': item_type_id,
        'level': level,
        'items': [{
            'item_id': item['item_id'],
            'rarity': item['rarity']
        } for item in items_list[:5]]
    })

with open('rarity_analysis_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("\nResults saved to: rarity_analysis_results.json")


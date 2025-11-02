#!/usr/bin/env python3
"""
Script para analizar amuletos y comparar con la DB
"""
import json
import requests
from typing import Dict, List

# Items transcr desde las imágenes
AMULETS_FROM_IMAGES = {
    "Colgante de Imagori": {
        "level": 245,
        "slot": "NECK",
        "stats": {
            "AP": 1,
            "HP": 578,
            "Lock": 100,
            "Dodge": 100,
            "Multi_Element_Mastery_3": 490,
            "Armor_Given": 6,  # % de armadura dada
            "Elemental_Resistance": 40,
            "Fire_Resistance": 40,
            "Water_Resistance": 40,
            "Earth_Resistance": 40
        }
    },
    "Amuleto de un origen": {
        "level": 245,
        "slot": "NECK",
        "stats": {
            "AP": 1,
            "Range": 1,
            "HP": 659,
            "Block": 3,  # % de anticipación
            "Multi_Element_Mastery_3": 420,
            "Armor_Given": 10
        }
    },
    "Armonía ancestral": {
        "level": 245,
        "slot": "NECK",
        "stats": {
            "AP": 1,
            "Range": 1,
            "HP": 468,
            "Dodge": 80,
            "Multi_Element_Mastery_3": 120,
            "Critical_Mastery": 120,
            "Distance_Mastery": 382,
            "Critical_Hit": 6
        }
    },
    "El reloj de arena de Xelor ancestral": {
        "level": 245,
        "slot": "NECK",
        "stats": {
            "AP": 1,
            "Range": 1,
            "WP": 1,
            "HP": 350,
            "Multi_Element_Mastery_3": 390,
            "Elemental_Resistance": 25
        }
    },
    "Veluleto": {
        "level": 245,
        "slot": "NECK",
        "stats": {
            "AP": 1,
            "HP": 671,
            "Lock": 95,
            "Dodge": 95,
            "Multi_Element_Mastery_2": 244,
            "Critical_Mastery": 244,
            "Critical_Hit": 6,
            "Elemental_Resistance": 50,
            "Fire_Resistance": 50,
            "Earth_Resistance": 50
        }
    },
    "El Péndulo": {
        "level": 245,
        "slot": "NECK",
        "stats": {
            "AP": 1,
            "HP": 721,
            "Lock": 165,
            "Block": 4,
            "Multi_Element_Mastery_3": 440,
            "Elemental_Resistance": 60,
            "Fire_Resistance": 60,
            "Air_Resistance": 60
        }
    },
    "Talismán del clan de Bworkana": {
        "level": 245,
        "slot": "NECK",
        "stats": {
            "HP": 822,
            "Lock": 130,
            "Dodge": 130,
            "Block": 1,
            "Melee_Mastery": 770,
            "Critical_Hit": 6,
            "Elemental_Resistance": 65,
            "Water_Resistance": 65,
            "Earth_Resistance": 65,
            "Air_Resistance": 65
        }
    },
    "Amuleto de fénix": {
        "level": 245,
        "slot": "NECK",
        "stats": {
            "MP": 1,
            "Range": 1,
            "HP": 677,
            "Multi_Element_Mastery_2": 346,
            "Distance_Mastery": 346,
            "Elemental_Resistance": 35,
            "Earth_Resistance": 35,
            "Air_Resistance": 35
        }
    },
    "Amuleto de Nyom": {
        "level": 245,
        "slot": "NECK",
        "stats": {
            "AP": 1,
            "HP": 687,
            "Lock": 100,
            "Dodge": 100,
            "Multi_Element_Mastery_2": 200,
            "Rear_Mastery": 289,
            "Melee_Mastery": 289,
            "Elemental_Resistance": 30,
            "Fire_Resistance": 30,
            "Water_Resistance": 30,
            "Air_Resistance": 30
        }
    },
    "Amuleto cúbico": {
        "level": 245,
        "slot": "NECK",
        "stats": {
            "AP": 1,
            "HP": 616,
            "Lock": 100,
            "Dodge": 100,
            "Multi_Element_Mastery_2": 170,
            "Berserk_Mastery": 250,
            "Melee_Mastery": 370,
            "Elemental_Resistance": 35,
            "Water_Resistance": 35,
            "Earth_Resistance": 35,
            "Air_Resistance": 35
        }
    },
    "Amuleto petrificado": {
        "level": 245,
        "slot": "NECK",
        "stats": {
            "AP": 1,
            "Range": 2,
            "HP": 587,
            "Lock": 80,
            "Dodge": 80,
            "Multi_Element_Mastery_2": 400,
            "Elemental_Resistance": -15
        }
    },
    "Amuleto noctámbulo": {
        "level": 245,
        "slot": "NECK",
        "stats": {
            "AP": 1,
            "Range": 1,
            "HP": 493,
            "Multi_Element_Mastery_2": 253,
            "Healing_Mastery": 173,
            "Critical_Hit": 6,
            "Elemental_Resistance": 30,
            "Fire_Resistance": 30,
            "Earth_Resistance": 30,
            "Air_Resistance": 30
        }
    },
    "Collar con espíritu": {
        "level": 245,
        "slot": "NECK",
        "stats": {
            "AP": 1,
            "HP": 563,
            "Lock": 80,
            "Dodge": 80,
            "Multi_Element_Mastery_2": 268,
            "Rear_Mastery": 268,
            "Critical_Hit": 6,
            "Elemental_Resistance": 65,
            "Earth_Resistance": 65,
            "Air_Resistance": 65
        }
    },
    "El Vueltaminuto": {
        "level": 245,
        "slot": "NECK",
        "stats": {
            "AP": 1,
            "HP": 672,
            "Dodge": 120,
            "Multi_Element_Mastery_2": 270,
            "Distance_Mastery": 270,
            "Critical_Hit": 6,
            "Elemental_Resistance": 50,
            "Water_Resistance": 50,
            "Earth_Resistance": 50
        }
    },
    "Damdamuleto": {
        "level": 245,
        "slot": "NECK",
        "stats": {
            "AP": 1,
            "HP": 507,
            "Lock": 151,
            "Critical_Mastery": 292,
            "Melee_Mastery": 292,
            "Critical_Hit": 6,
            "Elemental_Resistance": 45,
            "Fire_Resistance": 45,
            "Water_Resistance": 45,
            "Earth_Resistance": 45
        }
    },
    "La Leidemallas": {
        "level": 245,
        "slot": "NECK",
        "stats": {
            "AP": 1,
            "HP": 539,
            "Lock": 100,
            "Dodge": 100,
            "Berserk_Mastery": 550,
            "Critical_Hit": 6,
            "Elemental_Resistance": 35,
            "Water_Resistance": 35,
            "Earth_Resistance": 35,
            "Air_Resistance": 35
        }
    },
    # Nivel 230 amuletos
    "La mibola": {
        "level": 230,
        "slot": "NECK",
        "stats": {
            "AP": 1,
            "Range": 2,
            "Dodge": 96,
            "Multi_Element_Mastery_2": 305,
            "Elemental_Resistance": 25
        }
    },
    "Amuleto de Rushu": {
        "level": 230,
        "slot": "NECK",
        "stats": {
            "AP": 1,
            "HP": 600,
            "Multi_Element_Mastery_2": 207,
            "Berserk_Mastery": 417,
            "Elemental_Resistance": 15
        }
    },
    "Grisgris sanguinario": {
        "level": 230,
        "slot": "NECK",
        "stats": {
            "MP": 1,
            "Range": 1,
            "HP": 497,
            "Multi_Element_Mastery_2": 244,
            "Berserk_Mastery": 252,
            "Elemental_Resistance": 33,
            "Fire_Resistance": 33,
            "Water_Resistance": 33,
            "Earth_Resistance": 33
        }
    },
    "Amuleto de Raeliss": {
        "level": 230,
        "slot": "NECK",
        "stats": {
            "AP": 1,
            "HP": 397,
            "Dodge": 110,
            "Multi_Element_Mastery_2": 219,
            "Rear_Mastery": 298,
            "Elemental_Resistance": 44,
            "Fire_Resistance": 44,
            "Water_Resistance": 44,
            "Air_Resistance": 44
        }
    },
    "Amuleto corrompido": {
        "level": 230,
        "slot": "NECK",
        "stats": {
            "AP": 1,
            "Range": 1,
            "HP": 736,
            "Lock": 160,
            "Multi_Element_Mastery_2": 299
        }
    }
}

API_BASE = "http://localhost:8000"

def get_item_from_api(name_es: str) -> Dict:
    """Get item from API by Spanish name"""
    try:
        # Search all NECK items at level 230-245
        response = requests.get(f"{API_BASE}/items", params={
            "slot": "NECK",
            "level_min": 230,
            "level_max": 245,
            "limit": 150
        }, timeout=10)
        
        if response.status_code != 200:
            return None
        
        items = response.json()
        
        # Find matching item by name
        for item in items:
            if item.get("name_es") and name_es.lower() in item["name_es"].lower():
                return {
                    "item_id": item["item_id"],
                    "name_es": item["name_es"],
                    "level": item["level"],
                    "slot": item["slot"],
                    "stats": item["stats"]
                }
        
        return None
    except Exception as e:
        print(f"   Error fetching from API: {e}")
        return None

def compare_stats(item_name: str, expected: Dict, actual: Dict) -> List[str]:
    """Compare expected vs actual stats"""
    discrepancies = []
    
    expected_stats = expected["stats"]
    actual_stats = actual.get("stats", {}) if actual else {}
    
    # Check each expected stat
    for stat, expected_value in expected_stats.items():
        actual_value = actual_stats.get(stat)
        
        if actual_value is None:
            discrepancies.append(f"❌ {stat}: Expected {expected_value}, but MISSING in DB")
        elif abs(float(actual_value) - float(expected_value)) > 0.1:
            discrepancies.append(f"⚠️ {stat}: Expected {expected_value}, got {actual_value}")
        # else: match
    
    # Check for extra stats in DB
    for stat, actual_value in actual_stats.items():
        if stat not in expected_stats:
            discrepancies.append(f"➕ {stat}: {actual_value} (extra in DB, not in image)")
    
    return discrepancies

def main():
    """Main analysis"""
    print("🔍 Analizando amuletos nivel 245...")
    print("=" * 80)
    
    total_items = len(AMULETS_FROM_IMAGES)
    items_with_discrepancies = 0
    all_discrepancies = []
    
    for item_name, expected_data in AMULETS_FROM_IMAGES.items():
        print(f"\n📦 {item_name}")
        print("-" * 80)
        
        # Get from API
        db_item = get_item_from_api(item_name)
        
        if not db_item:
            print(f"❌ NOT FOUND in DB!")
            items_with_discrepancies += 1
            continue
        
        print(f"✅ Found in DB (ID: {db_item['item_id']})")
        
        # Compare stats
        discrepancies = compare_stats(item_name, expected_data, db_item)
        
        if discrepancies:
            items_with_discrepancies += 1
            print(f"\n🚨 {len(discrepancies)} discrepancias detectadas:")
            for disc in discrepancies:
                print(f"   {disc}")
                all_discrepancies.append({
                    "item": item_name,
                    "item_id": db_item['item_id'],
                    "issue": disc
                })
        else:
            print("✅ All stats match!")
    
    # Summary
    print("\n" + "=" * 80)
    print(f"📊 RESUMEN")
    print("=" * 80)
    print(f"Total items analizados: {total_items}")
    print(f"Items con discrepancias: {items_with_discrepancies} ({items_with_discrepancies/total_items*100:.1f}%)")
    print(f"Total discrepancias: {len(all_discrepancies)}")
    
    # Group by type
    missing = [d for d in all_discrepancies if "MISSING" in d["issue"]]
    different = [d for d in all_discrepancies if "Expected" in d["issue"] and "MISSING" not in d["issue"]]
    extra = [d for d in all_discrepancies if "extra" in d["issue"]]
    
    print(f"\n  - Stats faltantes: {len(missing)}")
    print(f"  - Stats con valores diferentes: {len(different)}")
    print(f"  - Stats extra en DB: {len(extra)}")

if __name__ == "__main__":
    main()


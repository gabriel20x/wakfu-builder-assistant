#!/usr/bin/env python3
"""
Script para analizar hombreras y comparar con la DB
"""
import json
import requests
from typing import Dict, List

# Items transcritos desde las imágenes
SHOULDERS_FROM_IMAGES = {
    "Electrombreras": {
        "level": 245,
        "slot": "SHOULDERS",
        "stats": {
            "HP": 660,
            "Critical_Mastery": 830,
            "Critical_Hit": -10,  # % negativo
            "Elemental_Resistance": 45,
            "Fire_Resistance": 45,
            "Earth_Resistance": 45,
            "Air_Resistance": 45
        }
    },
    "Hombreras crepusculares": {
        "level": 245,
        "slot": "SHOULDERS",
        "stats": {
            "HP": 527,
            "Dodge": 100,
            "Rear_Mastery": 782,
            "Elemental_Resistance": 50,
            "Water_Resistance": 50,
            "Earth_Resistance": 50,
            "Air_Resistance": 50
        }
    },
    "Los engranajes del tiempo": {
        "level": 245,
        "slot": "SHOULDERS",
        "stats": {
            "Control": 1,
            "HP": 684,
            "Multi_Element_Mastery_2": 370,
            "Distance_Mastery": 300,
            "Critical_Hit": 6,
            "Elemental_Resistance": 43,
            "Fire_Resistance": 43,
            "Water_Resistance": 43,
            "Air_Resistance": 43
        }
    },
    "Las Cronógrafas": {
        "level": 245,
        "slot": "SHOULDERS",
        "stats": {
            "Range": 1,
            "HP": 654,
            "Multi_Element_Mastery_2": 615,
            "Elemental_Resistance": 40,
            "Fire_Resistance": 40,
            "Water_Resistance": 40,
            "Earth_Resistance": 40
        }
    },
    "Hombreras de la comandante": {
        "level": 245,
        "slot": "SHOULDERS",
        "stats": {
            "HP": 656,
            "Lock": 80,
            "Dodge": 80,
            "Berserk_Mastery": 730,
            "Elemental_Resistance": 45,
            "Fire_Resistance": 45,
            "Water_Resistance": 45,
            "Earth_Resistance": 45
        }
    },
    "Hombreras ajustables": {
        "level": 245,
        "slot": "SHOULDERS",
        "stats": {
            "HP": 631,
            "Lock": 95,
            "Dodge": 95,
            "Multi_Element_Mastery_2": 170,
            "Critical_Mastery": 265,
            "Melee_Mastery": 265,
            "Critical_Hit": 6,
            "Elemental_Resistance": 60,
            "Water_Resistance": 60,
            "Air_Resistance": 60
        }
    },
    "Hombreras pehese": {
        "level": 245,
        "slot": "SHOULDERS",
        "stats": {
            "HP": 629,
            "Dodge": 152,
            "Rear_Mastery": 380,
            "Distance_Mastery": 380,
            "Critical_Hit": 6,
            "Elemental_Resistance": 40,
            "Fire_Resistance": 40,
            "Water_Resistance": 40,
            "Air_Resistance": 40
        }
    },
    "Las Tokkimbreras": {
        "level": 245,
        "slot": "SHOULDERS",
        "stats": {
            "HP": 482,
            "Lock": 115,
            "Melee_Mastery": 641,
            "Critical_Hit": 6,
            "Elemental_Resistance": 39  # dice "Resistencia elemental"
        }
    },
    "Las Cegatas ancestrales": {
        "level": 245,
        "slot": "SHOULDERS",
        "stats": {
            "HP": 525,
            "Dodge": 115,
            "Rear_Mastery": 372,
            "Melee_Mastery": 372,
            "Critical_Hit": 6,
            "Elemental_Resistance": 56,
            "Fire_Resistance": 56,
            "Water_Resistance": 56,
            "Air_Resistance": 56
        }
    },
    "Hombreras de Imagori": {
        "level": 245,
        "slot": "SHOULDERS",
        "stats": {
            "Range": 1,
            "WP": -1,  # PW máx. negativo
            "HP": 673,
            "Multi_Element_Mastery_2": 570,
            "Critical_Hit": 6,
            "Elemental_Resistance": 55,
            "Water_Resistance": 55,
            "Air_Resistance": 55
        }
    },
    "Hombreras desperdiciadas": {
        "level": 245,
        "slot": "SHOULDERS",
        "stats": {
            "Control": 1,
            "HP": 502,
            "Lock": 115,
            "Dodge": 115,
            "Multi_Element_Mastery_2": 510,
            "Critical_Hit": 6,
            "Armor_Given": 6,  # % de armadura dada
            "Elemental_Resistance": 75,
            "Fire_Resistance": 75,
            "Earth_Resistance": 75
        }
    },
    "Las Peligadoras": {
        "level": 245,
        "slot": "SHOULDERS",
        "stats": {
            "HP": 602,
            "Multi_Element_Mastery_2": 400,
            "Melee_Mastery": 260,
            "Critical_Hit": 6,
            "Elemental_Resistance": 60,
            "Fire_Resistance": 60,
            "Water_Resistance": 60,
            "Earth_Resistance": 60
        }
    },
    "Hombreras del clan de Bworkana": {
        "level": 245,
        "slot": "SHOULDERS",
        "stats": {
            "HP": 583,
            "Lock": 80,
            "Dodge": 80,
            "Multi_Element_Mastery_3": 560,
            "Armor_Given": 10,  # % de armadura dada
            "Elemental_Resistance": 65,
            "Water_Resistance": 65,
            "Earth_Resistance": 65
        }
    },
    "Hombreras de Gabhortom": {
        "level": 245,
        "slot": "SHOULDERS",
        "stats": {
            "HP": 603,
            "Dodge": 115,
            "Berserk_Mastery": 372,
            "Distance_Mastery": 372,
            "Critical_Hit": 6,
            "Elemental_Resistance": 37  # dice "Resistencia elemental"
        }
    },
    "Hombreras de botones": {
        "level": 245,
        "slot": "SHOULDERS",
        "stats": {
            "HP": 581,
            "Dodge": 140,
            "Multi_Element_Mastery_2": 395,
            "Distance_Mastery": 280,
            "Armor_Given": 10,  # % de armadura dada
            "Elemental_Resistance": 40,
            "Fire_Resistance": 40,
            "Water_Resistance": 40,
            "Earth_Resistance": 40
        }
    },
    "Homblelas del Empeladol ancestrales": {
        "level": 245,
        "slot": "SHOULDERS",
        "stats": {
            "WP": 1,
            "HP": 464,
            "Lock": 103,
            "Dodge": 103,
            "Multi_Element_Mastery_3": 468,
            "Elemental_Resistance": 40,  # dice "Resistencia elemental"
            "Critical_Resistance": 10  # Resistencia crítica
        }
    },
    "Las Influenciables": {
        "level": 245,
        "slot": "SHOULDERS",
        "stats": {
            "HP": 563,
            "Lock": 90,
            "Dodge": 90,
            "Multi_Element_Mastery_2": 165,
            "Healing_Mastery": 274,
            "Distance_Mastery": 274,
            "Critical_Hit": 6,
            "Elemental_Resistance": 45,
            "Fire_Resistance": 45,
            "Water_Resistance": 45,
            "Earth_Resistance": 45
        }
    },
    "Hombreras de Lakha": {
        "level": 245,
        "slot": "SHOULDERS",
        "stats": {
            "HP": 639,
            "Berserk_Mastery": 665,
            "Critical_Hit": 6,
            "Elemental_Resistance": 75,
            "Water_Resistance": 75,
            "Air_Resistance": 75
        }
    },
    "Hombreras de Lacrimorsa": {
        "level": 215,
        "slot": "SHOULDERS",
        "stats": {
            "HP": 277,
            "Block": 1,  # % de anticipación
            "Armor_Given": 5,  # % de armadura dada
            "Distance_Mastery": 309,
            "Critical_Hit": 5,
            "Elemental_Resistance": 44,
            "Water_Resistance": 44,
            "Earth_Resistance": 44,
            "Air_Resistance": 44
        }
    }
}

API_BASE = "http://localhost:8000"

def get_item_from_api(name_es: str, level: int) -> Dict:
    """Get item from API by Spanish name"""
    try:
        # Search SHOULDERS items at specified level
        response = requests.get(f"{API_BASE}/items", params={
            "slot": "SHOULDERS",
            "level_min": level - 5,
            "level_max": level + 5,
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
    print("Analizando hombreras nivel 215-245...")
    print("=" * 80)
    
    total_items = len(SHOULDERS_FROM_IMAGES)
    items_with_discrepancies = 0
    all_discrepancies = []
    not_found = []
    
    for item_name, expected_data in SHOULDERS_FROM_IMAGES.items():
        print(f"\n{item_name}")
        print("-" * 80)
        
        # Get from API
        db_item = get_item_from_api(item_name, expected_data["level"])
        
        if not db_item:
            print(f"❌ NOT FOUND in DB!")
            items_with_discrepancies += 1
            not_found.append(item_name)
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
    print(f"RESUMEN")
    print("=" * 80)
    print(f"Total items analizados: {total_items}")
    print(f"Items con discrepancias: {items_with_discrepancies} ({items_with_discrepancies/total_items*100:.1f}%)")
    print(f"Items no encontrados: {len(not_found)}")
    print(f"Total discrepancias: {len(all_discrepancies)}")
    
    if not_found:
        print(f"\nItems NO ENCONTRADOS:")
        for item in not_found:
            print(f"  - {item}")
    
    # Group by type
    missing = [d for d in all_discrepancies if "MISSING" in d["issue"]]
    different = [d for d in all_discrepancies if "Expected" in d["issue"] and "MISSING" not in d["issue"]]
    extra = [d for d in all_discrepancies if "extra" in d["issue"]]
    
    print(f"\n  - Stats faltantes: {len(missing)}")
    print(f"  - Stats con valores diferentes: {len(different)}")
    print(f"  - Stats extra en DB: {len(extra)}")
    
    # Analyze patterns
    print(f"\n" + "=" * 80)
    print("PATRONES DETECTADOS")
    print("=" * 80)
    
    # Count specific patterns
    elemental_res_missing = len([d for d in missing if "Elemental_Resistance" in d["issue"]])
    range_missing = len([d for d in missing if "Range" in d["issue"]])
    rear_missing = len([d for d in missing if "Rear_Mastery" in d["issue"]])
    armor_given_missing = len([d for d in missing if "Armor_Given" in d["issue"]])
    healing_missing = len([d for d in missing if "Healing_Mastery" in d["issue"]])
    
    if elemental_res_missing:
        print(f"- Elemental_Resistance genérica faltante: {elemental_res_missing} items ({elemental_res_missing/total_items*100:.0f}%)")
    if range_missing:
        print(f"- Range faltante: {range_missing} items ({range_missing/total_items*100:.0f}%)")
    if rear_missing:
        print(f"- Rear_Mastery faltante: {rear_missing} items ({rear_missing/total_items*100:.0f}%)")
    if armor_given_missing:
        print(f"- Armor_Given faltante: {armor_given_missing} items ({armor_given_missing/total_items*100:.0f}%)")
    if healing_missing:
        print(f"- Healing_Mastery faltante: {healing_missing} items ({healing_missing/total_items*100:.0f}%)")

if __name__ == "__main__":
    main()


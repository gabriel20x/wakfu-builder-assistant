#!/usr/bin/env python3
"""
Script para analizar armas de segunda mano (daggas y escudos) y comparar con DB
"""
import json
import requests
from typing import Dict, List

# Items transcritos desde las imágenes
SECOND_WEAPON_FROM_IMAGES = {
    # Nivel 245
    "La escama Da de Kaido": {
        "level": 245,
        "slot": "SECOND_WEAPON",
        "stats": {
            "HP": 758,
            "Lock": 90,
            "Dodge": 90,
            "Block": 15,  # % de anticipación
            "Elemental_Resistance": 36,
            "Critical_Resistance": 10,
            "Rear_Resistance": 10
        }
    },
    "La Nuezdaga": {
        "level": 245,
        "slot": "SECOND_WEAPON",
        "stats": {
            "HP": 299,
            "Dodge": 145,
            "Multi_Element_Mastery_3": 180,
            "Critical_Mastery": 230,
            "Critical_Hit": 3
        }
    },
    # Nivel 230
    "Daga brujandera": {
        "level": 230,
        "slot": "SECOND_WEAPON",
        "stats": {
            "Damage": 63,  # Daños
            "HP": 252,
            "Dodge": 250,
            "Multi_Element_Mastery_2": 315
        }
    },
    "Daga secular": {
        "level": 230,
        "slot": "SECOND_WEAPON",
        "stats": {
            "Damage": 63,
            "HP": 172,
            "Dodge": 130,
            "Multi_Element_Mastery_3": 259,
            "Critical_Mastery": 113
        }
    },
    "Dagarafobia": {
        "level": 230,
        "slot": "SECOND_WEAPON",
        "stats": {
            "Damage": 63,
            "HP": 220,
            "Dodge": 120,
            "Multi_Element_Mastery_2": 122,
            "Healing_Mastery": 212,
            "Critical_Hit": 3
        }
    },
    "Dagario": {
        "level": 230,
        "slot": "SECOND_WEAPON",
        "stats": {
            "Damage": 63,
            "WP": 1,
            "HP": 220,
            "Multi_Element_Mastery_3": 318
        }
    },
    "Parada Dójica": {
        "level": 230,
        "slot": "SECOND_WEAPON",
        "stats": {
            "HP": 573,
            "Lock": 55,
            "Dodge": 55,
            "Block": 10,
            "Armor_Received": 10,  # % de armadura recibida
            "Elemental_Resistance": 40
        }
    },
    "Égida del fin de los tiempos": {
        "level": 230,
        "slot": "SECOND_WEAPON",
        "stats": {
            "WP": 1,
            "HP": 484,
            "Lock": 100,
            "Block": 10,
            "Elemental_Resistance": 40
        }
    },
    "El constante": {
        "level": 230,
        "slot": "SECOND_WEAPON",
        "stats": {
            "Range": -1,  # Negativo!
            "HP": 617,
            "Lock": 136,
            "Block": 20,
            "Multi_Element_Mastery_2": 97,
            "Armor_Received": 15
        }
    },
    "Daga Melón": {
        "level": 230,
        "slot": "SECOND_WEAPON",
        "stats": {
            "Damage": 63,
            "HP": 200,
            "Lock": 45,
            "Dodge": 45,
            "Rear_Mastery": 400,
            "Critical_Hit": 3
        }
    },
    # Nivel 215
    "Desértica": {
        "level": 215,
        "slot": "SECOND_WEAPON",
        "stats": {
            "Damage": 59,
            "HP": 175,
            "Dodge": 23,
            "Critical_Hit": 3,
            "Multi_Element_Mastery_2": 196,
            "Critical_Mastery": 147
        }
    },
    "Corazandía": {
        "level": 215,
        "slot": "SECOND_WEAPON",
        "stats": {
            "HP": 470,
            "Lock": 114,
            "Block": 15,
            "Elemental_Resistance": 52,
            "Fire_Resistance": 52,
            "Water_Resistance": 52,
            "Air_Resistance": 52
        }
    },
    "Daga cataral": {
        "level": 215,
        "slot": "SECOND_WEAPON",
        "stats": {
            "Damage": 59,
            "HP": 171,
            "Dodge": 28,
            "Critical_Hit": 3,
            "Rear_Mastery": 345
        }
    },
    "La égida 'belle époque'": {
        "level": 215,
        "slot": "SECOND_WEAPON",
        "stats": {
            "HP": 558,
            "Lock": 85,
            "Dodge": 85,
            "Armor_Received": 10,
            "Elemental_Resistance": 79,
            "Earth_Resistance": 79,
            "Air_Resistance": 79
        }
    },
    # Nivel 200
    "Daga de sutura": {
        "level": 200,
        "slot": "SECOND_WEAPON",
        "stats": {
            "Damage": 55,
            "HP": 134,
            "Dodge": 30,
            "Critical_Hit": 3,
            "Multi_Element_Mastery_3": 129,
            "Healing_Mastery": 106
        }
    },
    "Escumuleto": {
        "level": 200,
        "slot": "SECOND_WEAPON",
        "stats": {
            "HP": 541,
            "Lock": 60,
            "Block": 15,
            "Single_Element_Mastery": 125  # Resistencia en 1 elemento
        }
    },
    "Escudoponente": {
        "level": 200,
        "slot": "SECOND_WEAPON",
        "stats": {
            "HP": 743,
            "Lock": 70,
            "Dodge": 70,
            "Critical_Resistance": 35,
            "Rear_Resistance": 35
        }
    },
    "Daga de Sram": {
        "level": 200,
        "slot": "SECOND_WEAPON",
        "stats": {
            "Damage": 55,
            "HP": 144,
            "Lock": 30,
            "Dodge": 30,
            "Critical_Hit": 3,
            "Rear_Mastery": 148,
            "Melee_Mastery": 165
        }
    },
    "Escudo de Feca": {
        "level": 200,
        "slot": "SECOND_WEAPON",
        "stats": {
            "WP": -1,  # Negativo!
            "Control": 1,
            "HP": 540,
            "Lock": 50,
            "Block": 14,
            "Elemental_Resistance": 40
        }
    },
    "Dagarrotipa": {
        "level": 200,
        "slot": "SECOND_WEAPON",
        "stats": {
            "Damage": 55,
            "WP": 1,
            "HP": 145,
            "Critical_Hit": 3,
            "Multi_Element_Mastery_3": 159
        }
    },
    "Crox": {
        "level": 200,
        "slot": "SECOND_WEAPON",
        "stats": {
            "Damage": 55,
            "HP": 173,
            "Critical_Hit": 3,
            "Multi_Element_Mastery_3": 165,
            "Critical_Mastery": 78
        }
    },
    "Cascarilla": {
        "level": 200,
        "slot": "SECOND_WEAPON",
        "stats": {
            "WP": 1,
            "HP": 316,
            "Dodge": 40,
            "Block": 16,
            "Elemental_Resistance": 30
        }
    },
    "Daga Zapada": {
        "level": 200,
        "slot": "SECOND_WEAPON",
        "stats": {
            "Damage": 55,
            "HP": 147,
            "Lock": 25,
            "Dodge": 25,
            "Critical_Hit": 3,
            "Multi_Element_Mastery_2": 279
        }
    },
    "Escudo de fresno": {
        "level": 200,
        "slot": "SECOND_WEAPON",
        "stats": {
            "HP": 554,
            "Lock": 45,
            "Block": 10,
            "Multi_Element_Mastery_3": 56
        }
    }
}

API_BASE = "http://localhost:8000"

def get_item_from_api(name_es: str, level: int) -> Dict:
    """Get item from API by Spanish name"""
    try:
        response = requests.get(f"{API_BASE}/items", params={
            "slot": "SECOND_WEAPON",
            "level_min": level - 5,
            "level_max": level + 5,
            "limit": 200
        }, timeout=10)
        
        if response.status_code != 200:
            return None
        
        items = response.json()
        
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
    
    for stat, expected_value in expected_stats.items():
        actual_value = actual_stats.get(stat)
        
        if actual_value is None:
            discrepancies.append(f"❌ {stat}: Expected {expected_value}, but MISSING in DB")
        elif abs(float(actual_value) - float(expected_value)) > 0.1:
            discrepancies.append(f"⚠️ {stat}: Expected {expected_value}, got {actual_value}")
    
    for stat, actual_value in actual_stats.items():
        if stat not in expected_stats:
            discrepancies.append(f"➕ {stat}: {actual_value} (extra in DB, not in image)")
    
    return discrepancies

def main():
    """Main analysis"""
    print("Analizando armas de segunda mano (daggas y escudos) nivel 200-245...")
    print("=" * 80)
    
    total_items = len(SECOND_WEAPON_FROM_IMAGES)
    items_with_discrepancies = 0
    all_discrepancies = []
    not_found = []
    
    for item_name, expected_data in SECOND_WEAPON_FROM_IMAGES.items():
        print(f"\n{item_name}")
        print("-" * 80)
        
        db_item = get_item_from_api(item_name, expected_data["level"])
        
        if not db_item:
            print(f"❌ NOT FOUND in DB!")
            items_with_discrepancies += 1
            not_found.append(item_name)
            continue
        
        print(f"✅ Found in DB (ID: {db_item['item_id']})")
        
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
    damage_missing = len([d for d in missing if "Damage" in d["issue"]])
    healing_missing = len([d for d in missing if "Healing_Mastery" in d["issue"]])
    
    if damage_missing:
        print(f"- Damage faltante: {damage_missing} items ({damage_missing/total_items*100:.0f}%)")
    if elemental_res_missing:
        print(f"- Elemental_Resistance faltante: {elemental_res_missing} items ({elemental_res_missing/total_items*100:.0f}%)")
    if range_missing:
        print(f"- Range (negativo) faltante: {range_missing} items")
    if rear_missing:
        print(f"- Rear_Mastery faltante: {rear_missing} items")
    if healing_missing:
        print(f"- Healing_Mastery faltante: {healing_missing} items")

if __name__ == "__main__":
    main()


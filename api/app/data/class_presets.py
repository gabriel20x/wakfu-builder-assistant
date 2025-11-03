"""
Class and Role Presets for Wakfu Builder
Defines stat weights and priorities for each class and role combination
"""

# Role-based stat priorities (base templates)
ROLE_TEMPLATES = {
    "tank": {
        "description": "Maximiza supervivencia y control de zona",
        "primary_stats": ["HP", "Lock", "Block"],
        "secondary_stats": ["Dodge", "Force_Of_Will", "Initiative"],
        "resistances": ["Elemental_Resistance", "Critical_Resistance", "Rear_Resistance"],
        "weights": {
            "HP": 10.0,
            "Lock": 8.0,
            "Block": 8.0,
            "Dodge": 6.0,
            "Force_Of_Will": 6.0,
            "Elemental_Resistance": 7.0,
            "Critical_Resistance": 5.0,
            "Rear_Resistance": 5.0,
            "AP": 6.0,
            "MP": 5.0,
            "Initiative": 4.0,
        }
    },
    "dps_melee": {
        "description": "Daño cuerpo a cuerpo",
        "primary_stats": ["AP", "Melee_Mastery", "Critical_Hit", "Critical_Mastery"],
        "secondary_stats": ["Damage_Inflicted", "Rear_Mastery", "Berserk_Mastery"],
        "weights": {
            "AP": 10.0,
            "Melee_Mastery": 9.0,
            "Critical_Hit": 8.0,
            "Critical_Mastery": 8.0,
            "Damage_Inflicted": 7.0,
            "Rear_Mastery": 7.0,
            "MP": 6.0,
            "Berserk_Mastery": 6.0,
            "HP": 4.0,
            "Initiative": 3.0,
        }
    },
    "dps_distance": {
        "description": "Daño a distancia",
        "primary_stats": ["AP", "Distance_Mastery", "Critical_Hit", "Range"],
        "secondary_stats": ["Critical_Mastery", "Damage_Inflicted", "Rear_Mastery"],
        "weights": {
            "AP": 10.0,
            "Distance_Mastery": 9.0,
            "Critical_Hit": 8.0,
            "Critical_Mastery": 8.0,
            "Range": 7.0,
            "Damage_Inflicted": 7.0,
            "Rear_Mastery": 6.0,
            "MP": 5.0,
            "HP": 3.0,
            "Initiative": 3.0,
        }
    },
    "healer": {
        "description": "Soporte y curación",
        "primary_stats": ["AP", "WP", "Healing_Mastery", "Heals_Performed"],
        "secondary_stats": ["HP", "Critical_Hit", "Critical_Mastery", "Initiative"],
        "weights": {
            "AP": 10.0,
            "WP": 9.0,
            "Healing_Mastery": 9.0,
            "Heals_Performed": 8.0,
            "Critical_Hit": 6.0,
            "Critical_Mastery": 6.0,
            "HP": 5.0,
            "MP": 5.0,
            "Initiative": 4.0,
            "Wisdom": 3.0,
        }
    },
    "support": {
        "description": "Buffs, debuffs y control",
        "primary_stats": ["AP", "MP", "Control", "Initiative"],
        "secondary_stats": ["WP", "HP", "Critical_Hit"],
        "weights": {
            "AP": 10.0,
            "MP": 8.0,
            "Control": 7.0,
            "Initiative": 7.0,
            "WP": 6.0,
            "HP": 5.0,
            "Range": 5.0,
            "Critical_Hit": 4.0,
            "Wisdom": 3.0,
        }
    },
    "berserker": {
        "description": "DPS basado en Berserk",
        "primary_stats": ["AP", "Berserk_Mastery", "Melee_Mastery", "Critical_Hit"],
        "secondary_stats": ["Critical_Mastery", "Damage_Inflicted", "HP"],
        "weights": {
            "AP": 10.0,
            "Berserk_Mastery": 9.0,
            "Melee_Mastery": 8.0,
            "Critical_Hit": 7.0,
            "Critical_Mastery": 7.0,
            "Damage_Inflicted": 6.0,
            "HP": 5.0,
            "MP": 5.0,
            "Rear_Mastery": 4.0,
        }
    }
}

# Class-specific presets
CLASS_PRESETS = {
    "feca": {
        "name": "Feca",
        "icon": "feca",
        "primary_role": "tank",
        "roles": {
            "tank": {
                "name": "Tank Protector",
                "description": "Máxima supervivencia con glifos protectores",
                "elements": ["Water", "Earth"],
                "weights": {
                    "HP": 10.0,
                    "AP": 8.0,
                    "Water_Mastery": 7.0,
                    "Earth_Mastery": 7.0,
                    "Lock": 8.0,
                    "Block": 8.0,
                    "Elemental_Resistance": 7.0,
                    "Critical_Resistance": 6.0,
                    "MP": 5.0,
                    "Armor_Given": 5.0,
                    "Armor_Received": 5.0,
                }
            },
            "support": {
                "name": "Support Glifo",
                "description": "Buffs de equipo con glifos",
                "elements": ["Fire", "Air"],
                "weights": {
                    "AP": 10.0,
                    "Fire_Mastery": 7.0,
                    "Air_Mastery": 7.0,
                    "MP": 7.0,
                    "Control": 7.0,
                    "HP": 6.0,
                    "Initiative": 5.0,
                    "Range": 5.0,
                }
            }
        }
    },
    "osamodas": {
        "name": "Osamodas",
        "icon": "osamodas",
        "primary_role": "support",
        "roles": {
            "summoner": {
                "name": "Invocador",
                "description": "Control de invocaciones poderosas",
                "elements": ["Fire", "Earth", "Water"],
                "weights": {
                    "AP": 10.0,
                    "Fire_Mastery": 8.0,
                    "Earth_Mastery": 8.0,
                    "Water_Mastery": 8.0,
                    "MP": 7.0,
                    "Control": 9.0,
                    "HP": 5.0,
                    "Critical_Hit": 6.0,
                    "Damage_Inflicted": 6.0,
                }
            },
            "dps": {
                "name": "DPS Elemental",
                "description": "Daño directo multielemental",
                "elements": ["Fire", "Air"],
                "weights": {
                    "AP": 10.0,
                    "Fire_Mastery": 9.0,
                    "Air_Mastery": 8.0,
                    "Critical_Hit": 8.0,
                    "Critical_Mastery": 8.0,
                    "Damage_Inflicted": 7.0,
                    "MP": 6.0,
                    "Distance_Mastery": 6.0,
                }
            }
        }
    },
    "enutrof": {
        "name": "Enutrof",
        "icon": "enutrof",
        "primary_role": "support",
        "roles": {
            "support_mp": {
                "name": "Support MP Removal",
                "description": "Control con remoción de MP",
                "elements": ["Water", "Earth"],
                "weights": {
                    "AP": 10.0,
                    "Water_Mastery": 8.0,
                    "Earth_Mastery": 8.0,
                    "MP": 8.0,
                    "Lock": 7.0,
                    "Critical_Hit": 7.0,
                    "Range": 6.0,
                    "Prospecting": 5.0,
                    "Initiative": 5.0,
                }
            },
            "dps": {
                "name": "DPS Cac/Distance",
                "description": "Daño híbrido con movilidad",
                "elements": ["Fire", "Air"],
                "weights": {
                    "AP": 10.0,
                    "Fire_Mastery": 8.0,
                    "Air_Mastery": 8.0,
                    "Critical_Hit": 8.0,
                    "Critical_Mastery": 7.0,
                    "Melee_Mastery": 7.0,
                    "Distance_Mastery": 7.0,
                    "MP": 6.0,
                }
            }
        }
    },
    "sram": {
        "name": "Sram",
        "icon": "sram",
        "primary_role": "dps_melee",
        "roles": {
            "assassin": {
                "name": "Asesino Espalda",
                "description": "Máximo daño por la espalda",
                "elements": ["Fire", "Air"],
                "weights": {
                    "AP": 10.0,
                    "Fire_Mastery": 9.0,
                    "Air_Mastery": 8.0,
                    "Rear_Mastery": 10.0,
                    "Critical_Hit": 8.0,
                    "Critical_Mastery": 8.0,
                    "Melee_Mastery": 7.0,
                    "MP": 7.0,
                    "Damage_Inflicted": 7.0,
                }
            },
            "trap": {
                "name": "Especialista en Trampas",
                "description": "Control de zona con trampas",
                "elements": ["Earth", "Water"],
                "weights": {
                    "AP": 10.0,
                    "Earth_Mastery": 8.0,
                    "Water_Mastery": 8.0,
                    "MP": 8.0,
                    "Control": 7.0,
                    "Critical_Hit": 7.0,
                    "Rear_Mastery": 7.0,
                    "Range": 6.0,
                }
            }
        }
    },
    "xelor": {
        "name": "Xelor",
        "icon": "xelor",
        "primary_role": "dps_distance",
        "roles": {
            "dps_ap": {
                "name": "DPS Remoción AP",
                "description": "Control temporal con AP removal",
                "elements": ["Fire", "Air"],
                "weights": {
                    "AP": 10.0,
                    "Fire_Mastery": 9.0,
                    "Air_Mastery": 8.0,
                    "Critical_Hit": 8.0,
                    "Critical_Mastery": 8.0,
                    "Distance_Mastery": 7.0,
                    "MP": 7.0,
                    "Range": 6.0,
                    "Initiative": 6.0,
                }
            },
            "support": {
                "name": "Support Temporal",
                "description": "Control de tiempo y teleport",
                "elements": ["Water", "Earth"],
                "weights": {
                    "AP": 10.0,
                    "Water_Mastery": 7.0,
                    "Earth_Mastery": 7.0,
                    "MP": 8.0,
                    "Control": 7.0,
                    "Initiative": 7.0,
                    "Range": 6.0,
                    "HP": 5.0,
                }
            }
        }
    },
    "ecaflip": {
        "name": "Ecaflip",
        "icon": "ecaflip",
        "primary_role": "dps_melee",
        "roles": {
            "dps_crit": {
                "name": "DPS Crítico",
                "description": "Máximo daño con críticos",
                "elements": ["Fire", "Air"],
                "weights": {
                    "AP": 10.0,
                    "Fire_Mastery": 9.0,
                    "Air_Mastery": 8.0,
                    "Critical_Hit": 10.0,
                    "Critical_Mastery": 10.0,
                    "Melee_Mastery": 8.0,
                    "Damage_Inflicted": 7.0,
                    "MP": 6.0,
                }
            },
            "tank": {
                "name": "Tank Ágil",
                "description": "Tanque con esquiva",
                "elements": ["Water", "Earth"],
                "weights": {
                    "HP": 9.0,
                    "AP": 8.0,
                    "Water_Mastery": 7.0,
                    "Earth_Mastery": 7.0,
                    "Dodge": 8.0,
                    "Lock": 7.0,
                    "Critical_Hit": 7.0,
                    "MP": 6.0,
                }
            }
        }
    },
    "eniripsa": {
        "name": "Eniripsa",
        "icon": "eniripsa",
        "primary_role": "healer",
        "roles": {
            "healer": {
                "name": "Curandero",
                "description": "Máxima curación",
                "elements": ["Water"],
                "weights": {
                    "AP": 10.0,
                    "WP": 9.0,
                    "Water_Mastery": 8.0,
                    "Healing_Mastery": 10.0,
                    "Heals_Performed": 9.0,
                    "Critical_Hit": 7.0,
                    "Critical_Mastery": 7.0,
                    "MP": 6.0,
                    "HP": 5.0,
                }
            },
            "dps_fire": {
                "name": "DPS Fuego",
                "description": "Daño con marca",
                "elements": ["Fire"],
                "weights": {
                    "AP": 10.0,
                    "Fire_Mastery": 9.0,
                    "Critical_Hit": 8.0,
                    "Critical_Mastery": 8.0,
                    "Distance_Mastery": 7.0,
                    "Damage_Inflicted": 7.0,
                    "MP": 6.0,
                    "WP": 5.0,
                }
            }
        }
    },
    "iop": {
        "name": "Iop",
        "icon": "iop",
        "primary_role": "dps_melee",
        "roles": {
            "dps_melee": {
                "name": "DPS Melé",
                "description": "Máximo daño cuerpo a cuerpo",
                "elements": ["Fire", "Air"],
                "weights": {
                    "AP": 10.0,
                    "Fire_Mastery": 9.0,
                    "Air_Mastery": 8.0,
                    "Melee_Mastery": 9.0,
                    "Critical_Hit": 8.0,
                    "Critical_Mastery": 8.0,
                    "Damage_Inflicted": 8.0,
                    "MP": 6.0,
                    "Rear_Mastery": 7.0,
                }
            },
            "berserker": {
                "name": "Berserker",
                "description": "DPS con Berserk",
                "elements": ["Fire"],
                "weights": {
                    "AP": 10.0,
                    "Fire_Mastery": 9.0,
                    "Berserk_Mastery": 10.0,
                    "Melee_Mastery": 8.0,
                    "Critical_Hit": 7.0,
                    "Critical_Mastery": 7.0,
                    "Damage_Inflicted": 7.0,
                    "HP": 6.0,
                }
            }
        }
    },
    "cra": {
        "name": "Cra",
        "icon": "cra",
        "primary_role": "dps_distance",
        "roles": {
            "sniper": {
                "name": "Francotirador",
                "description": "Máximo daño a distancia",
                "elements": ["Fire", "Air"],
                "weights": {
                    "AP": 10.0,
                    "Fire_Mastery": 9.0,
                    "Air_Mastery": 8.0,
                    "Distance_Mastery": 10.0,
                    "Critical_Hit": 8.0,
                    "Critical_Mastery": 8.0,
                    "Range": 8.0,
                    "Damage_Inflicted": 7.0,
                    "MP": 5.0,
                }
            },
            "support": {
                "name": "Support Beacon",
                "description": "Buffs con beacons",
                "elements": ["Water", "Earth"],
                "weights": {
                    "AP": 10.0,
                    "Water_Mastery": 7.0,
                    "Earth_Mastery": 7.0,
                    "Distance_Mastery": 7.0,
                    "MP": 7.0,
                    "Range": 7.0,
                    "Critical_Hit": 6.0,
                    "Control": 6.0,
                }
            }
        }
    },
    "sadida": {
        "name": "Sadida",
        "icon": "sadida",
        "primary_role": "support",
        "roles": {
            "summoner_heal": {
                "name": "Invocador Curandero",
                "description": "Soporte con muñecos y curas",
                "elements": ["Water"],
                "weights": {
                    "AP": 10.0,
                    "Water_Mastery": 8.0,
                    "Healing_Mastery": 8.0,
                    "Control": 8.0,
                    "MP": 7.0,
                    "HP": 6.0,
                    "Critical_Hit": 6.0,
                    "Heals_Performed": 6.0,
                }
            },
            "dps_poison": {
                "name": "DPS Veneno",
                "description": "Daño con envenenamientos",
                "elements": ["Earth", "Air"],
                "weights": {
                    "AP": 10.0,
                    "Earth_Mastery": 9.0,
                    "Air_Mastery": 8.0,
                    "Critical_Hit": 8.0,
                    "Critical_Mastery": 7.0,
                    "Control": 7.0,
                    "Distance_Mastery": 6.0,
                    "MP": 6.0,
                }
            }
        }
    },
    "sacrier": {
        "name": "Sacrier",
        "icon": "sacrier",
        "primary_role": "berserker",
        "roles": {
            "tank_aggro": {
                "name": "Tank Agresivo",
                "description": "Tanque con daño",
                "elements": ["Fire", "Earth"],
                "weights": {
                    "HP": 10.0,
                    "AP": 9.0,
                    "Fire_Mastery": 8.0,
                    "Earth_Mastery": 7.0,
                    "Melee_Mastery": 7.0,
                    "Lock": 7.0,
                    "Berserk_Mastery": 7.0,
                    "Elemental_Resistance": 6.0,
                    "MP": 5.0,
                }
            },
            "berserker": {
                "name": "Berserker Puro",
                "description": "Máximo Berserk",
                "elements": ["Fire"],
                "weights": {
                    "AP": 10.0,
                    "Fire_Mastery": 9.0,
                    "Berserk_Mastery": 10.0,
                    "Melee_Mastery": 8.0,
                    "HP": 8.0,
                    "Critical_Hit": 7.0,
                    "Damage_Inflicted": 7.0,
                    "MP": 5.0,
                }
            }
        }
    },
    "pandawa": {
        "name": "Pandawa",
        "icon": "pandawa",
        "primary_role": "tank",
        "roles": {
            "tank_support": {
                "name": "Tank Soporte",
                "description": "Tanque con control de posición",
                "elements": ["Water", "Earth"],
                "weights": {
                    "HP": 10.0,
                    "AP": 8.0,
                    "Water_Mastery": 7.0,
                    "Earth_Mastery": 7.0,
                    "Lock": 8.0,
                    "MP": 7.0,
                    "Elemental_Resistance": 7.0,
                    "Initiative": 6.0,
                    "Control": 5.0,
                }
            },
            "dps_melee": {
                "name": "DPS Melé",
                "description": "Daño cuerpo a cuerpo",
                "elements": ["Fire", "Air"],
                "weights": {
                    "AP": 10.0,
                    "Fire_Mastery": 9.0,
                    "Air_Mastery": 8.0,
                    "Melee_Mastery": 8.0,
                    "Critical_Hit": 8.0,
                    "Critical_Mastery": 7.0,
                    "HP": 6.0,
                    "MP": 6.0,
                }
            }
        }
    },
    "rogue": {
        "name": "Rogue",
        "icon": "rogue",
        "primary_role": "dps_distance",
        "roles": {
            "bomber": {
                "name": "Bombardero",
                "description": "Máximo daño con bombas",
                "elements": ["Fire", "Air"],
                "weights": {
                    "AP": 10.0,
                    "Fire_Mastery": 9.0,
                    "Air_Mastery": 8.0,
                    "Critical_Hit": 9.0,
                    "Critical_Mastery": 9.0,
                    "Distance_Mastery": 8.0,
                    "Damage_Inflicted": 8.0,
                    "MP": 7.0,
                    "Control": 6.0,
                }
            },
            "support_wall": {
                "name": "Support Muros",
                "description": "Control con muros",
                "elements": ["Earth", "Water"],
                "weights": {
                    "AP": 10.0,
                    "Earth_Mastery": 7.0,
                    "Water_Mastery": 7.0,
                    "MP": 8.0,
                    "Control": 8.0,
                    "Critical_Hit": 6.0,
                    "Range": 6.0,
                    "HP": 5.0,
                }
            }
        }
    },
    "masqueraider": {
        "name": "Masqueraider",
        "icon": "masqueraider",
        "primary_role": "dps_melee",
        "roles": {
            "dps_versatile": {
                "name": "DPS Versátil",
                "description": "Daño adaptable con máscaras",
                "elements": ["Fire", "Air", "Water"],
                "weights": {
                    "AP": 10.0,
                    "Fire_Mastery": 8.0,
                    "Air_Mastery": 8.0,
                    "Water_Mastery": 7.0,
                    "Melee_Mastery": 8.0,
                    "Critical_Hit": 8.0,
                    "Critical_Mastery": 7.0,
                    "MP": 7.0,
                    "Damage_Inflicted": 6.0,
                }
            },
            "tank": {
                "name": "Tank Máscara",
                "description": "Tanque con evasión",
                "elements": ["Earth"],
                "weights": {
                    "HP": 9.0,
                    "AP": 8.0,
                    "Earth_Mastery": 7.0,
                    "Dodge": 8.0,
                    "Lock": 7.0,
                    "Melee_Mastery": 6.0,
                    "MP": 6.0,
                    "Initiative": 6.0,
                }
            }
        }
    },
    "foggernaut": {
        "name": "Foggernaut",
        "icon": "foggernaut",
        "primary_role": "dps_distance",
        "roles": {
            "dps_railgun": {
                "name": "DPS Railgun",
                "description": "Daño a distancia con stasis",
                "elements": ["Fire", "Water"],
                "weights": {
                    "AP": 10.0,
                    "Fire_Mastery": 9.0,
                    "Water_Mastery": 8.0,
                    "Distance_Mastery": 8.0,
                    "Critical_Hit": 8.0,
                    "Critical_Mastery": 8.0,
                    "Range": 7.0,
                    "MP": 6.0,
                }
            },
            "tank_fire": {
                "name": "Tank Fuego",
                "description": "Tanque con daño de fuego",
                "elements": ["Fire", "Earth"],
                "weights": {
                    "HP": 9.0,
                    "AP": 8.0,
                    "Fire_Mastery": 8.0,
                    "Earth_Mastery": 7.0,
                    "Melee_Mastery": 6.0,
                    "Lock": 7.0,
                    "Elemental_Resistance": 6.0,
                    "MP": 5.0,
                }
            }
        }
    },
    "eliotrope": {
        "name": "Eliotrope",
        "icon": "eliotrope",
        "primary_role": "dps_distance",
        "roles": {
            "dps_portal": {
                "name": "DPS Portales",
                "description": "Daño con portales",
                "elements": ["Fire", "Air"],
                "weights": {
                    "AP": 10.0,
                    "Fire_Mastery": 9.0,
                    "Air_Mastery": 8.0,
                    "Distance_Mastery": 8.0,
                    "Critical_Hit": 8.0,
                    "Critical_Mastery": 7.0,
                    "MP": 7.0,
                    "Control": 7.0,
                }
            },
            "support": {
                "name": "Support Movilidad",
                "description": "Soporte con portales",
                "elements": ["Water", "Earth"],
                "weights": {
                    "AP": 10.0,
                    "Water_Mastery": 7.0,
                    "Earth_Mastery": 7.0,
                    "MP": 8.0,
                    "Control": 8.0,
                    "Initiative": 7.0,
                    "Range": 6.0,
                    "HP": 5.0,
                }
            }
        }
    },
    "huppermage": {
        "name": "Huppermage",
        "icon": "huppermage",
        "primary_role": "dps_distance",
        "roles": {
            "dps_quad": {
                "name": "DPS Cuadrielemental",
                "description": "Los 4 elementos",
                "elements": ["Fire", "Water", "Earth", "Air"],
                "weights": {
                    "AP": 10.0,
                    "Fire_Mastery": 9.0,
                    "Water_Mastery": 9.0,
                    "Earth_Mastery": 9.0,
                    "Air_Mastery": 9.0,
                    "Elemental_Mastery": 8.0,
                    "Critical_Hit": 7.0,
                    "Distance_Mastery": 7.0,
                    "MP": 6.0,
                }
            },
            "dps_tri": {
                "name": "DPS Trielemental",
                "description": "3 elementos optimizado",
                "elements": ["Fire", "Water", "Air"],
                "weights": {
                    "AP": 10.0,
                    "Fire_Mastery": 9.0,
                    "Water_Mastery": 9.0,
                    "Air_Mastery": 9.0,
                    "Critical_Hit": 8.0,
                    "Critical_Mastery": 7.0,
                    "Distance_Mastery": 7.0,
                    "MP": 6.0,
                }
            }
        }
    },
    "ouginak": {
        "name": "Ouginak",
        "icon": "ouginak",
        "primary_role": "dps_melee",
        "roles": {
            "dps_fury": {
                "name": "DPS Furia",
                "description": "Daño con furia canina",
                "elements": ["Fire", "Air"],
                "weights": {
                    "AP": 10.0,
                    "Fire_Mastery": 9.0,
                    "Air_Mastery": 8.0,
                    "Melee_Mastery": 9.0,
                    "Critical_Hit": 8.0,
                    "Critical_Mastery": 8.0,
                    "Rear_Mastery": 7.0,
                    "MP": 6.0,
                }
            },
            "tank_prey": {
                "name": "Tank Presa",
                "description": "Tanque con marcas de presa",
                "elements": ["Earth", "Water"],
                "weights": {
                    "HP": 9.0,
                    "AP": 8.0,
                    "Earth_Mastery": 7.0,
                    "Water_Mastery": 7.0,
                    "Melee_Mastery": 7.0,
                    "Lock": 8.0,
                    "MP": 6.0,
                    "Elemental_Resistance": 6.0,
                }
            }
        }
    }
}


def get_class_preset(class_name: str, role: str = None):
    """
    Get preset weights for a specific class and role
    
    Args:
        class_name: Class identifier (e.g. 'iop', 'cra')
        role: Optional role identifier (e.g. 'dps_melee', 'tank')
        
    Returns:
        Dict with stat weights, or None if not found
    """
    class_name = class_name.lower()
    
    if class_name not in CLASS_PRESETS:
        return None
    
    class_data = CLASS_PRESETS[class_name]
    
    # If no role specified, use primary role
    if role is None:
        role = class_data["primary_role"]
        
    # If role not in class roles, try to find it in role templates
    if role not in class_data.get("roles", {}):
        if role in ROLE_TEMPLATES:
            return ROLE_TEMPLATES[role]["weights"]
        return None
    
    return class_data["roles"][role]["weights"]


def get_element_preferences_from_preset(class_name: str, role: str = None):
    """
    Get recommended element order for a class/role
    
    Returns:
        tuple: (damage_preferences, resistance_preferences)
    """
    class_name = class_name.lower()
    
    if class_name not in CLASS_PRESETS:
        return (['Fire', 'Water', 'Earth', 'Air'], ['Fire', 'Water', 'Earth', 'Air'])
    
    class_data = CLASS_PRESETS[class_name]
    
    if role is None:
        role = class_data["primary_role"]
    
    if role in class_data.get("roles", {}):
        elements = class_data["roles"][role].get("elements", ['Fire', 'Water', 'Earth', 'Air'])
        # Complete with remaining elements
        all_elements = ['Fire', 'Water', 'Earth', 'Air']
        damage_prefs = elements + [e for e in all_elements if e not in elements]
        return (damage_prefs, damage_prefs)
    
    return (['Fire', 'Water', 'Earth', 'Air'], ['Fire', 'Water', 'Earth', 'Air'])


def list_all_classes():
    """Return list of all available classes"""
    return [
        {
            "id": class_id,
            "name": data["name"],
            "icon": data["icon"],
            "primary_role": data["primary_role"],
            "roles": list(data["roles"].keys())
        }
        for class_id, data in CLASS_PRESETS.items()
    ]


def list_roles_for_class(class_name: str):
    """Return available roles for a specific class"""
    class_name = class_name.lower()
    
    if class_name not in CLASS_PRESETS:
        return []
    
    class_data = CLASS_PRESETS[class_name]
    
    return [
        {
            "id": role_id,
            "name": role_data["name"],
            "description": role_data["description"],
            "elements": role_data.get("elements", []),
            "is_primary": role_id == class_data["primary_role"]
        }
        for role_id, role_data in class_data["roles"].items()
    ]


from csv import reader
import os


def read_csv(path):
    lay_map = []
    with open(path, newline='') as file:
        lay = reader(file, delimiter=',')
        lay_map = [list(row) for row in lay]
    return lay_map


def shorten_column_name(name):
    abbreviations = {
        "max_general_level": "Lvl",
        "max_countEnemies": "Enemies",
        "max_level_health": "HP",
        "max_level_stamina": "Stam",
        "max_level_cooldown": "CD",
        "max_level_melee_attack": "Atk",
        "max_damage_done": "DMG"
    }
    return abbreviations.get(name, name)

import yaml
import random

_current_combat_state = {}


def load_player_combat_data(path):
    with open(path, 'r') as f:
        data = yaml.safe_load(f)

    return [
        {
            "name": pc["name"],
            "type": "player",
            "ac": pc["derived"]["ac"],
            "hp": pc["derived"]["health"],
            "brawn": pc["stats"]["brawn"],
            "agility": pc["stats"]["agility"],
            "conditions": pc.get("conditions", []),
        }
        for pc in data
    ]


def load_monster_data(monster_names):
    with open("vault/lookup/monsters/monsters.yaml", 'r') as f:
        monsters = yaml.safe_load(f)["entries"]

    enemies = []
    for name in monster_names:
        m = next((m for m in monsters if m["name"] == name), None)
        if m:
            hp = int(m["hit_dice"].split('(')[1].split('hp')[0])  # crude hp extract
            enemies.append({
                "name": m["name"],
                "type": "monster",
                "ac": m["armor_class"],
                "hp": hp,
                "to_hit": m.get("to_hit", 0),
                "damage": m["attacks"],
                "morale": m.get("morale", 7),
            })
    return enemies


def roll_initiative(entities):
    for entity in entities:
        entity["initiative"] = random.randint(1, 20) + entity.get("agility", 0)
    return sorted(entities, key=lambda e: e["initiative"], reverse=True)


def init_combat_state(entities):
    global _current_combat_state
    _current_combat_state = {e["name"]: e for e in entities}
    return _current_combat_state


def get_current_combat_state():
    return _current_combat_state


def resolve_attack(attacker, defender):
    roll = random.randint(1, 20)
    to_hit_bonus = attacker.get("brawn", attacker.get("to_hit", 0))
    hit = roll + to_hit_bonus >= defender["ac"]
    result = {
        "attacker": attacker["name"],
        "defender": defender["name"],
        "roll": roll,
        "to_hit": to_hit_bonus,
        "hit": hit,
    }

    if hit:
        damage = random.randint(1, 6)  # temp default
        defender["hp"] -= damage
        result["damage"] = damage
        result["defender_hp"] = defender["hp"]
    return result

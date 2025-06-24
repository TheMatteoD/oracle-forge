import yaml
import json
import argparse
import random

def load_monsters(path="vault/tables/monsters.yaml"):
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    return data["entries"]

def find_monster(name_query, monsters):
    name_query = name_query.strip().lower()
    return [
        m for m in monsters
        if name_query in m.get("name", "").lower()
    ]


def roll_number_appearing(monster):
    import re
    match = re.search(r"(\d+)d(\d+)(?:\s*\((\d+)d(\d+)\))?", monster["number_appearing"])
    if match:
        d1, d2 = int(match.group(1)), int(match.group(2))
        return sum(random.randint(1, d2) for _ in range(d1))
    return 1

def display_monster(monster, as_json=False):
    def trait_to_str(trait):
        if isinstance(trait, dict):
            key, val = next(iter(trait.items()))
            return f"{key}: {val}"
        return str(trait)

    traits = [trait_to_str(t) for t in monster.get('traits', [])]
    saves = monster.get('saving_throws', [{}])[0]
    saving_str = f"Brawn {saves.get('brawn', '-')}, Agility {saves.get('agility', '-')}, Mind {saves.get('mind', '-')}"

    if as_json:
        return {
            "name": monster["name"],
            "description": monster.get("description", ""),
            "hit_dice": monster.get("hit_dice"),
            "armor_class": monster.get("armor_class"),
            "movement": monster.get("movement"),
            "morale": monster.get("morale"),
            "to_hit": monster.get("to_hit"),
            "attacks": monster.get("attacks"),
            "saving_throws": saves,
            "traits": traits,
            "xp": monster.get("experience"),
            "number_appearing": monster.get("number_appearing"),
            "alignment": monster.get("alignment"),
            "tags": monster.get("tags", []),
            "system": monster.get("system", ""),
            "source": monster.get("source", "")
        }
    else:
        return f"""{monster['name']} ({monster['hit_dice']} HD)
{monster.get('description', '')}
AC {monster['armor_class']}, MV {monster['movement']}, Morale {monster['morale']}, To-Hit Bonus: +{monster['to_hit']}
Attacks: {monster['attacks']}
Saving Throws: {saving_str}
Traits: {', '.join(traits)}
XP: {monster['experience']}, Appearing: {monster['number_appearing']}
System: {monster.get('system', 'Unknown')}
Source: {monster.get('source', 'Unknown')}
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monster Lookup Utility")
    parser.add_argument("query", type=str, nargs="?", help="Partial monster name")
    parser.add_argument("--json", action="store_true", help="Return results in JSON")
    parser.add_argument("--system", type=str, help="Filter by system (e.g., OSE:AF)")
    parser.add_argument("--tag", type=str, help="Filter by tag (e.g., undead, humanoid)")

    args = parser.parse_args()

    monsters = load_monsters()
    matches = monsters

    if args.query:
        matches = find_monster(args.query, matches)

    if args.system:
        matches = [
            m for m in matches
            if args.system.lower() in m.get("system", "").lower()
        ]
    
    if args.tag:
        tag_query = args.tag.lower()
        matches = [
            m for m in matches
            if any(tag_query in t.lower() for t in m.get("tags", []))
        ]



    if not matches:
        print("No match found.")
    else:
        if args.json:
            print(json.dumps([display_monster(m, as_json=True) for m in matches], indent=2))
        else:
            for m in matches:
                print(display_monster(m))


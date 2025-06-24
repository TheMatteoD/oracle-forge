import yaml
import json
import argparse

def load_spells(path="vault/tables/spells.yaml"):
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    return data["entries"]

def find_spells(query, spells):
    query = query.lower()
    return [s for s in spells if query in s["name"].lower()]

def display_spell(spell, as_json=False):
    if as_json:
        return {
            "name": spell["name"],
            "description": spell.get("description", ""),
            "class": spell.get("class", ""),
            "level": spell.get("level", ""),
            "duration": spell.get("duration", ""),
            "range": spell.get("range", ""),
            "tags": spell.get("tags", []),
            "system": spell.get("system", ""),
            "source": spell.get("source", "")
        }
    else:
        return f"""{spell['name']} (Level {spell['level']} {spell['class']})
{spell.get('description', '')}
Duration: {spell.get('duration', '-')}, Range: {spell.get('range', '-')}
Tags: {', '.join(spell.get('tags', []))}
System: {spell.get('system', 'Unknown')}
Source: {spell.get('source', 'Unknown')}
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spell Lookup Utility")
    parser.add_argument("query", type=str, nargs="?", help="Partial spell name")
    parser.add_argument("--json", action="store_true", help="Return results in JSON")
    parser.add_argument("--class", dest="spell_class", type=str, help="Filter by class (e.g., Cleric)")
    parser.add_argument("--level", type=int, help="Filter by spell level")
    parser.add_argument("--tag", type=str, help="Filter by tag (e.g., utility, healing)")
    parser.add_argument("--system", type=str, help="Filter by system (e.g., OSE:AF)")

    args = parser.parse_args()

    spells = load_spells()
    matches = spells

    if args.query:
        matches = find_spells(args.query, matches)

    if args.spell_class:
        matches = [s for s in matches if s.get("class", "").lower() == args.spell_class.lower()]

    if args.level is not None:
        matches = [s for s in matches if s.get("level") == args.level]
    
    if args.tag:
        tag_query = args.tag.lower()
        matches = [
            s for s in matches
            if any(tag_query in t.lower() for t in s.get("tags", []))
        ]

    if args.system:
        matches = [s for s in matches if args.system.lower() in s.get("system", "").lower()]

    if not matches:
        print("No match found.")
    else:
        if args.json:
            print(json.dumps([display_spell(s, as_json=True) for s in matches], indent=2))
        else:
            for s in matches:
                print(display_spell(s))


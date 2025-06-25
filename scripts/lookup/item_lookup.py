import yaml
import json
import argparse
import os
import glob
import random
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from llm.flavoring import narrate_items

def load_items_from_directory(directory="vault/lookup/items/"):
    """Load all items from all YAML files in the items directory."""
    all_items = []
    
    if not os.path.exists(directory):
        return all_items
    
    # Find all YAML files in the items directory
    yaml_files = glob.glob(os.path.join(directory, "*.yaml"))
    
    for file_path in yaml_files:
        try:
            with open(file_path, "r") as f:
                data = yaml.safe_load(f)
                if data and "entries" in data:
                    all_items.extend(data["entries"])
        except Exception as e:
            print(f"Warning: Could not load {file_path}: {e}")
    
    return all_items

def find_items(query, items):
    """Find items matching the query in name or description."""
    query = query.lower()
    return [
        item for item in items
        if query in item.get("name", "").lower() or 
           query in item.get("description", "").lower()
    ]

def get_random_items(items, count=1):
    """Get a random selection of items from the provided list."""
    if not items:
        return []
    
    count = min(count, len(items))
    return random.sample(items, count)

def display_item(item, as_json=False):
    """Format an item for display."""
    if as_json:
        return {
            "name": item["name"],
            "description": item.get("description", ""),
            "category": item.get("category", ""),
            "subcategory": item.get("subcategory", ""),
            "tags": item.get("tags", []),
            "damage": item.get("damage", ""),
            "damage_type": item.get("damage_type", ""),
            "armor_class": item.get("armor_class", ""),
            "weight": item.get("weight", ""),
            "cost": item.get("cost", ""),
            "properties": item.get("properties", []),
            "traits": item.get("traits", []),
            "system": item.get("system", ""),
            "source": item.get("source", "")
        }
    else:
        # Format for console display
        output = f"{item['name']}"
        
        if item.get("category"):
            output += f" ({item['category']}"
            if item.get("subcategory"):
                output += f"/{item['subcategory']}"
            output += ")"
        
        output += f"\n{item.get('description', '')}"
        
        if item.get("damage"):
            output += f"\nDamage: {item['damage']}"
            if item.get("damage_type"):
                output += f" ({item['damage_type']})"
        
        if item.get("armor_class"):
            output += f"\nArmor Class: {item['armor_class']}"
        
        if item.get("weight"):
            output += f"\nWeight: {item['weight']}"
        
        if item.get("cost"):
            output += f"\nCost: {item['cost']}"
        
        if item.get("properties"):
            output += f"\nProperties: {', '.join(item['properties'])}"
        
        if item.get("traits"):
            traits_str = []
            for trait in item["traits"]:
                if isinstance(trait, dict):
                    key, val = next(iter(trait.items()))
                    traits_str.append(f"{key}: {val}")
                else:
                    traits_str.append(str(trait))
            output += f"\nTraits: {', '.join(traits_str)}"
        
        if item.get("tags"):
            output += f"\nTags: {', '.join(item['tags'])}"
        
        output += f"\nSystem: {item.get('system', 'Unknown')}"
        output += f"\nSource: {item.get('source', 'Unknown')}"
        
        return output

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Item Lookup Utility")
    parser.add_argument("query", type=str, nargs="?", help="Partial item name or description")
    parser.add_argument("--json", action="store_true", help="Return results in JSON")
    parser.add_argument("--category", type=str, help="Filter by category (e.g., weapon, armor)")
    parser.add_argument("--subcategory", type=str, help="Filter by subcategory (e.g., melee, light)")
    parser.add_argument("--tag", type=str, help="Filter by tag (e.g., light, magical)")
    parser.add_argument("--system", type=str, help="Filter by system (e.g., OSE:AF)")
    parser.add_argument("--random", type=int, help="Get N random items from filtered results")
    parser.add_argument("--environment", type=str, help="Apply environmental flavoring (e.g., forest, desert, mountain)")
    parser.add_argument("--quality", type=str, help="Apply quality flavoring (e.g., poor, average, superior, masterwork)")
    parser.add_argument("--theme", type=str, help="Apply thematic flavoring (e.g., elven, dwarven, orcish)")
    parser.add_argument("--context", type=str, help="Player context for flavoring")
    parser.add_argument("--narrate", action="store_true", help="Generate LLM narration for results")

    args = parser.parse_args()

    items = load_items_from_directory()
    matches = items

    if args.query:
        matches = find_items(args.query, matches)

    if args.category:
        matches = [i for i in matches if i.get("category", "").lower() == args.category.lower()]

    if args.subcategory:
        matches = [i for i in matches if i.get("subcategory", "").lower() == args.subcategory.lower()]

    if args.system:
        matches = [i for i in matches if args.system.lower() in i.get("system", "").lower()]

    if args.tag:
        tag_query = args.tag.lower()
        matches = [
            i for i in matches
            if any(tag_query in t.lower() for t in i.get("tags", []))
        ]

    # Apply random selection if requested
    if args.random and args.random > 0:
        matches = get_random_items(matches, args.random)

    if not matches:
        print("No match found.")
    else:
        if args.narrate:
            # Generate LLM narration
            narration = narrate_items(
                matches, 
                context=args.context,
                environment=args.environment, 
                quality=args.quality, 
                theme=args.theme
            )
            print("=== LLM Narration ===")
            print(narration)
            print("\n=== Raw Data ===")
        
        if args.json:
            print(json.dumps([display_item(i, as_json=True) for i in matches], indent=2))
        else:
            for item in matches:
                print(display_item(item))
                print("-" * 50) 
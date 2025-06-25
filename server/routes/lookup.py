# server/routes/lookup.py
from flask import Blueprint, request, jsonify
from scripts.lookup.monster_lookup import load_monsters, find_monster, display_monster, get_random_monsters
from scripts.lookup.spell_lookup import load_spells, find_spells, display_spell, get_random_spells
from scripts.lookup.item_lookup import load_items_from_directory, find_items, display_item, get_random_items
from scripts.lookup.rule_search import search_rules
from scripts.llm.flavoring import narrate_items, narrate_monsters, narrate_spells, rewrite_narration

lookup = Blueprint('lookup', __name__)

@lookup.route("/lookup/monster", methods=["POST"])
def lookup_monster():
    data = request.get_json()
    monsters = load_monsters()
    query = data.get("query", "").strip()
    system = data.get("system", "").strip().lower()
    tag = data.get("tag", "").strip().lower()
    random_count = data.get("random", 0)
    environment = data.get("environment", "").strip()
    theme = data.get("theme", "").strip()
    context = data.get("context", "").strip()
    narrate = data.get("narrate", False)
    log_session = data.get("log_session", True)

    if query:
        monsters = find_monster(query, monsters)
    if system:
        monsters = [m for m in monsters if system in m.get("system", "").lower()]
    if tag:
        monsters = [m for m in monsters if any(tag in t.lower() for t in m.get("tags", []))]

    # Apply random selection if requested
    if random_count and random_count > 0:
        monsters = get_random_monsters(monsters, random_count)

    # Generate narration if requested
    narration = None
    if narrate and monsters:
        narration = narrate_monsters(monsters, context, environment, theme, log_session)

    result = {
        "items": [display_monster(m, as_json=True) for m in monsters],
        "count": len(monsters)
    }
    
    if narration:
        result["narration"] = narration

    return jsonify(result)

@lookup.route("/lookup/spell", methods=["POST"])
def lookup_spell():
    data = request.get_json()
    spells = load_spells()
    query = data.get("query", "").strip().lower()
    system = data.get("system", "").strip().lower()
    spell_class = data.get("class", "").strip().lower()
    tag = data.get("tag", "").strip().lower()
    level = data.get("level")
    random_count = data.get("random", 0)
    theme = data.get("theme", "").strip()
    context = data.get("context", "").strip()
    narrate = data.get("narrate", False)
    log_session = data.get("log_session", True)

    if query:
        spells = [s for s in spells if query in s.get("name", "").lower()]
    if system:
        spells = [s for s in spells if system in s.get("system", "").lower()]
    if spell_class:
        spells = [s for s in spells if spell_class in s.get("class", "").lower()]
    if isinstance(level, int):
        spells = [s for s in spells if s.get("level") == level]
    if tag:
        spells = [s for s in spells if any(tag in t.lower() for t in s.get("tags", []))]

    # Apply random selection if requested
    if random_count and random_count > 0:
        spells = get_random_spells(spells, random_count)

    # Generate narration if requested
    narration = None
    if narrate and spells:
        narration = narrate_spells(spells, context, theme, log_session)

    result = {
        "items": [display_spell(s, as_json=True) for s in spells],
        "count": len(spells)
    }
    
    if narration:
        result["narration"] = narration

    return jsonify(result)

@lookup.route("/lookup/item", methods=["POST"])
def lookup_item():
    data = request.get_json()
    items = load_items_from_directory()
    query = data.get("query", "").strip()
    system = data.get("system", "").strip().lower()
    category = data.get("category", "").strip().lower()
    subcategory = data.get("subcategory", "").strip().lower()
    tag = data.get("tag", "").strip().lower()
    random_count = data.get("random", 0)
    environment = data.get("environment", "").strip()
    quality = data.get("quality", "").strip()
    theme = data.get("theme", "").strip()
    context = data.get("context", "").strip()
    narrate = data.get("narrate", False)
    log_session = data.get("log_session", True)

    if query:
        items = find_items(query, items)
    if system:
        items = [i for i in items if system in i.get("system", "").lower()]
    if category:
        items = [i for i in items if category in i.get("category", "").lower()]
    if subcategory:
        items = [i for i in items if subcategory in i.get("subcategory", "").lower()]
    if tag:
        items = [i for i in items if any(tag in t.lower() for t in i.get("tags", []))]

    # Apply random selection if requested
    if random_count and random_count > 0:
        items = get_random_items(items, random_count)

    # Generate narration if requested
    narration = None
    if narrate and items:
        narration = narrate_items(items, context, environment, quality, theme, log_session)

    result = {
        "items": [display_item(i, as_json=True) for i in items],
        "count": len(items)
    }
    
    if narration:
        result["narration"] = narration

    return jsonify(result)

@lookup.route("/lookup/rewrite", methods=["POST"])
def rewrite_lookup_narration():
    """Rewrite an existing narration based on user instructions."""
    data = request.get_json()
    original_narration = data.get("narration", "").strip()
    rewrite_instruction = data.get("instruction", "").strip()
    log_session = data.get("log_session", True)
    
    if not original_narration or not rewrite_instruction:
        return jsonify({"error": "Both narration and instruction are required"}), 400
    
    rewritten_narration = rewrite_narration(original_narration, rewrite_instruction, log_session)
    
    return jsonify({
        "original_narration": original_narration,
        "rewrite_instruction": rewrite_instruction,
        "rewritten_narration": rewritten_narration
    })

@lookup.route("/lookup/rule", methods=["POST"])
def lookup_rule():
    data = request.get_json()
    query = data.get("query", "").strip()
    system = data.get("system", "").strip()
    tag = data.get("tag", "").strip()
    
    results = search_rules(query, system, tag)
    return jsonify(results)

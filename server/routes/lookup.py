# server/routes/lookup.py
from flask import Blueprint, request, jsonify
from scripts.lookup.monster_lookup import load_monsters, find_monster, display_monster
from scripts.lookup.spell_lookup import load_spells, find_spells, display_spell
from scripts.lookup.rule_search import search_rules

lookup = Blueprint('lookup', __name__)

@lookup.route("/lookup/monster", methods=["POST"])
def lookup_monster():
    data = request.get_json()
    monsters = load_monsters()
    query = data.get("query", "").strip()
    system = data.get("system", "").strip().lower()
    tag = data.get("tag", "").strip().lower()

    if query:
        monsters = find_monster(query, monsters)
    if system:
        monsters = [m for m in monsters if system in m.get("system", "").lower()]
    if tag:
        monsters = [m for m in monsters if any(tag in t.lower() for t in m.get("tags", []))]

    return jsonify([display_monster(m, as_json=True) for m in monsters])

@lookup.route("/lookup/spell", methods=["POST"])
def lookup_spell():
    data = request.get_json()
    spells = load_spells()
    query = data.get("query", "").strip().lower()
    system = data.get("system", "").strip().lower()
    spell_class = data.get("class", "").strip().lower()
    tag = data.get("tag", "").strip().lower()
    level = data.get("level")

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

    return jsonify([display_spell(s, as_json=True) for s in spells])

@lookup.route("/lookup/rule", methods=["POST"])
def lookup_rule():
    data = request.get_json()
    return jsonify(search_rules(
        data.get("query"), data.get("system"), data.get("tag")
    ))

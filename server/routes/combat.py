from flask import Blueprint, request, jsonify
from scripts.combat import combat_driver as combat

combat_bp = Blueprint("combat", __name__)

@combat_bp.route("/combat/start", methods=["POST"])
def start_combat():
    data = request.get_json()
    players = combat.load_player_combat_data("vault/logs/adventure01/player_states.yaml")
    enemies = combat.load_monster_data(data.get("monsters", []))

    initiative_order = combat.roll_initiative(players + enemies)
    state = combat.init_combat_state(initiative_order)

    return jsonify({
        "initiative_order": [entity["name"] for entity in initiative_order],
        "combat_state": state
    })

@combat_bp.route("/combat/attack", methods=["POST"])
def attack():
    data = request.get_json()
    result = combat.resolve_attack(data["attacker"], data["defender"])
    return jsonify(result)

@combat_bp.route("/combat/status", methods=["GET"])
def status():
    return jsonify(combat.get_current_combat_state())
from flask import Blueprint, request, g
from scripts.combat import combat_driver as combat
from ..utils.responses import APIResponse, handle_service_response
from ..utils.validation import validate_json_body, validate_field

combat_bp = Blueprint("combat", __name__)

@combat_bp.route("/combat/start", methods=["POST"])
@validate_json_body(required_fields=["monsters"])
@validate_field("monsters", field_type=list, allow_none=False)
def start_combat():
    """Start a new combat encounter"""
    data = g.request_data
    
    players = combat.load_player_combat_data("vault/adventures/adventure01/player_states.yaml")
    enemies = combat.load_monster_data(data.get("monsters", []))

    initiative_order = combat.roll_initiative(players + enemies)
    state = combat.init_combat_state(initiative_order)

    return APIResponse.success({
        "initiative_order": [entity["name"] for entity in initiative_order],
        "combat_state": state
    })

@combat_bp.route("/combat/attack", methods=["POST"])
@validate_json_body(required_fields=["attacker", "defender"])
def attack():
    """Resolve an attack in combat"""
    data = g.request_data
    
    result = combat.resolve_attack(data["attacker"], data["defender"])
    return APIResponse.success(result)

@combat_bp.route("/combat/status", methods=["GET"])
def status():
    """Get current combat status"""
    state = combat.get_current_combat_state()
    return APIResponse.success(state)
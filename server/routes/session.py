from flask import Blueprint, jsonify, request
import os
import yaml
from datetime import datetime
import re

session = Blueprint("session", __name__)

BASE_DIR = os.path.join("vault", "logs")
STATE_DIR = "server/state"
ACTIVE_FILE = os.path.join(STATE_DIR, "active_adventure.txt")

def get_active_adventure():
    if not os.path.exists(ACTIVE_FILE):
        return None
    with open(ACTIVE_FILE, 'r') as f:
        return f.read().strip()

def load_yaml(path):
    if not os.path.exists(path):
        return {}
    with open(path, 'r') as f:
        return yaml.safe_load(f) or {}

def write_yaml(path, data):
    with open(path, 'w') as f:
        yaml.dump(data, f)

def sanitize_filename(name):
    """Convert character name to a safe filename"""
    # Remove special characters and replace spaces with underscores
    safe_name = re.sub(r'[^a-zA-Z0-9\s]', '', name)
    safe_name = re.sub(r'\s+', '_', safe_name).lower()
    return safe_name

@session.route("/session/character", methods=["POST"])
def create_character():
    adv = get_active_adventure()
    if not adv:
        return jsonify({"error": "No active adventure"}), 400

    name = request.json.get("name", "").strip()
    if not name:
        return jsonify({"error": "Character name is required"}), 400

    # Load character template
    template_path = os.path.join("vault", "templates", "character_template.yaml")
    if not os.path.exists(template_path):
        return jsonify({"error": "Character template not found"}), 500

    character_data = load_yaml(template_path)
    character_data["name"] = name

    # Create safe filename
    safe_filename = sanitize_filename(name) + ".yaml"
    
    # Ensure players directory exists
    players_dir = os.path.join(BASE_DIR, adv, "players")
    os.makedirs(players_dir, exist_ok=True)
    
    # Save character file
    character_path = os.path.join(players_dir, safe_filename)
    write_yaml(character_path, character_data)

    # Update player_states.yaml to include new character
    player_states_path = os.path.join(BASE_DIR, adv, "player_states.yaml")
    player_states = load_yaml(player_states_path)
    players = player_states.get("players", [])
    
    if safe_filename not in players:
        players.append(safe_filename)
        player_states["players"] = players
        write_yaml(player_states_path, player_states)

    return jsonify({
        "success": True,
        "character": character_data,
        "filename": safe_filename
    })

@session.route("/session/state", methods=["GET"])
def session_state():
    adv = get_active_adventure()
    if not adv:
        return jsonify({"error": "No active adventure"}), 400

    base_path = os.path.join(BASE_DIR, adv)

    world = load_yaml(os.path.join(base_path, "world_state.yaml"))
    
    players_index = load_yaml(os.path.join(base_path, "player_states.yaml"))
    player_refs = players_index.get("players", [])
    players = []
    for filename in player_refs:
        full_path = os.path.join(base_path, "players", filename)
        data = load_yaml(full_path)
        players.append(data)

    session_data = load_yaml(os.path.join(base_path, "active_session.yaml"))

    return jsonify({
        "world": world,
        "players": players,
        "session": session_data,
        "combat_log": session_data.get("combat_log", [])
    })

@session.route("/session/log", methods=["POST"])
def add_log_entry():
    adv = get_active_adventure()
    if not adv:
        return jsonify({"error": "No active adventure"}), 400

    entry = request.json.get("entry", "").strip()
    entry_type = request.json.get("type", "combat")  # default type

    if not entry:
        return jsonify({"error": "Empty log entry"}), 400

    path = os.path.join(BASE_DIR, adv, "active_session.yaml")
    session_data = load_yaml(path)
    log = session_data.get("combat_log", [])

    timestamp = datetime.now().strftime("[%H:%M] ")
    log.append(timestamp + entry)

    session_data["combat_log"] = log
    write_yaml(path, session_data)

    return jsonify({"success": True, "entry": entry})

@session.route("/session/character/<character_name>", methods=["GET"])
def get_character(character_name):
    adv = get_active_adventure()
    if not adv:
        return jsonify({"error": "No active adventure"}), 400

    # Load player states to find the character file
    player_states_path = os.path.join(BASE_DIR, adv, "player_states.yaml")
    player_states = load_yaml(player_states_path)
    players = player_states.get("players", [])
    
    # Find the character file that matches the name
    character_file = None
    for filename in players:
        if filename.endswith('.yaml'):
            char_path = os.path.join(BASE_DIR, adv, "players", filename)
            char_data = load_yaml(char_path)
            if char_data.get("name") == character_name:
                character_file = filename
                break
    
    if not character_file:
        return jsonify({"error": "Character not found"}), 404
    
    # Load and return the character data
    character_path = os.path.join(BASE_DIR, adv, "players", character_file)
    character_data = load_yaml(character_path)
    
    return jsonify({
        "success": True,
        "character": character_data
    })

@session.route("/session/character/<character_name>", methods=["PUT"])
def update_character(character_name):
    adv = get_active_adventure()
    if not adv:
        return jsonify({"error": "No active adventure"}), 400

    # Load player states to find the character file
    player_states_path = os.path.join(BASE_DIR, adv, "player_states.yaml")
    player_states = load_yaml(player_states_path)
    players = player_states.get("players", [])
    
    # Find the character file that matches the name
    character_file = None
    for filename in players:
        if filename.endswith('.yaml'):
            char_path = os.path.join(BASE_DIR, adv, "players", filename)
            char_data = load_yaml(char_path)
            if char_data.get("name") == character_name:
                character_file = filename
                break
    
    if not character_file:
        return jsonify({"error": "Character not found"}), 404
    
    # Load current character data
    character_path = os.path.join(BASE_DIR, adv, "players", character_file)
    character_data = load_yaml(character_path)
    
    # Update with new data from request
    update_data = request.json.get("character", {})
    character_data.update(update_data)
    
    # Save updated character
    write_yaml(character_path, character_data)
    
    return jsonify({
        "success": True,
        "character": character_data
    })

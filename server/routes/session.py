from flask import Blueprint, jsonify, request
import os
import yaml
from datetime import datetime
import re
import glob
from scripts.llm.flavoring import summarize_session_log_llm

session = Blueprint("session", __name__)

BASE_DIR = os.path.join("vault", "adventures")
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

def get_session_file(adv, session_id=None):
    sessions_dir = os.path.join(BASE_DIR, adv, "sessions")
    if not os.path.exists(sessions_dir):
        return None
    if session_id:
        file = os.path.join(sessions_dir, f"{session_id}.yaml")
        if os.path.exists(file):
            return file
        return None
    # If no session_id, return the latest session file (by name)
    files = sorted(glob.glob(os.path.join(sessions_dir, "session_*.yaml")))
    return files[-1] if files else None

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

@session.route("/session/log", methods=["GET"])
def get_session_log():
    adv = get_active_adventure()
    if not adv:
        return jsonify({"error": "No active adventure"}), 400
    file = get_session_file(adv)
    if not file:
        return jsonify({"error": "No session log found"}), 404
    data = load_yaml(file)
    log = data.get("log", [])
    return jsonify(log)

@session.route("/session/log", methods=["POST"])
def append_session_log():
    adv = get_active_adventure()
    if not adv:
        return jsonify({"error": "No active adventure"}), 400
    entry = request.json
    if not entry or not entry.get("content"):
        return jsonify({"error": "Empty log entry"}), 400
    file = get_session_file(adv)
    if not file:
        return jsonify({"error": "No session log found"}), 404
    data = load_yaml(file)
    log = data.get("log", [])
    from datetime import datetime
    entry_obj = {
        "timestamp": entry.get("timestamp") or datetime.now().isoformat(),
        "type": entry.get("type", "custom"),
        "content": entry["content"]
    }
    log.append(entry_obj)
    data["log"] = log
    write_yaml(file, data)
    return jsonify({"success": True, "entry": entry_obj})

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

def summarize_session_log(log):
    prompt = (
        "Summarize the following RPG session log concisely as a narrative, with no additions or embellishments. " +
        "Your response should be as retelling the counts or telling it as a story, meaning use full sentences, no lists, and explain what happened. " +
        "Use only the information provided.\n\nSession Log:\n" +
        "\n".join(f"[{entry.get('timestamp', '')}] [{entry.get('type', '')}] {entry.get('content', '')}" for entry in log)
    )
    return summarize_session_log_llm(prompt)

@session.route("/session/end", methods=["POST"])
def end_session():
    adv = get_active_adventure()
    if not adv:
        return jsonify({"error": "No active adventure"}), 400
    file = get_session_file(adv)
    if not file:
        return jsonify({"error": "No session log found"}), 404

    data = load_yaml(file)
    log = data.get("log", [])

    try:
        summary = summarize_session_log(log)
    except Exception as e:
        return jsonify({"error": f"LLM summarization failed: {e}"}), 500

    md_path = file.replace('.yaml', '.md')
    with open(md_path, 'w') as f:
        f.write(f"# Session Summary\n\n{summary}\n\n---\n\n## Full Log\n\n")
        for entry in log:
            f.write(f"- [{entry.get('timestamp', '')}] [{entry.get('type', '')}] {entry.get('content', '')}\n")

    sessions_dir = os.path.join(BASE_DIR, adv, "sessions")
    os.makedirs(sessions_dir, exist_ok=True)
    existing = glob.glob(os.path.join(sessions_dir, "session_*.yaml"))
    next_id = len(existing) + 1
    next_filename = f"session_{next_id:02d}.yaml"
    next_path = os.path.join(sessions_dir, next_filename)
    with open(next_path, "w") as f:
        yaml.dump({
            "session_id": next_filename.replace(".yaml", ""),
            "adventure": adv,
            "log": [],
            "phase": "start"
        }, f)

    active_path = os.path.join(BASE_DIR, adv, "active_session.yaml")
    write_yaml(active_path, {
        "session_id": next_filename.replace(".yaml", ""),
        "adventure": adv,
        "log": [],
        "phase": "start"
    })

    return jsonify({"success": True, "summary": summary, "next_session": next_filename})


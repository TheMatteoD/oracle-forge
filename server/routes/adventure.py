from flask import Blueprint, send_from_directory, jsonify, request, send_file
import os
import yaml

adventure = Blueprint('adventure', __name__)

ADVENTURE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "vault", "logs"))
ACTIVE_PATH = os.path.join("server", "state", "active_adventure.txt")

@adventure.route("/adventures/list", methods=["GET"])
def list_adventures():
    folders = [f for f in os.listdir(ADVENTURE_ROOT) if os.path.isdir(os.path.join(ADVENTURE_ROOT, f))]
    return jsonify(folders)

def init_adventure_structure(adventure_name):
    base_path = os.path.join(ADVENTURE_ROOT, adventure_name)

    # Ensure base folders
    os.makedirs(base_path, exist_ok=True)
    os.makedirs(os.path.join(base_path, "players"), exist_ok=True)  # ⬅️ Add this line
    os.makedirs(os.path.join(base_path, "world", "locations"), exist_ok=True)
    os.makedirs(os.path.join(base_path, "world", "factions"), exist_ok=True)
    os.makedirs(os.path.join(base_path, "world", "npcs"), exist_ok=True)
    os.makedirs(os.path.join(base_path, "sessions"), exist_ok=True)

    # Init files
    files_to_create = {
        "world_state.yaml": {
            "chaos_factor": 5,
            "current_scene": 1,
            "days_passed": 0,
            "preferred_rule_system": "Oracle Forge",
            "locations": [],
            "factions": [],
            "threads": []
        },
        "player_states.yaml": { "players": [] },
        "active_session.yaml": {
            "session_id": "session_01",
            "adventure": adventure_name,
            "log": [],
            "phase": "start"
        }
    }

    for filename, content in files_to_create.items():
        full_path = os.path.join(base_path, filename)
        if not os.path.exists(full_path):
            with open(full_path, "w") as f:
                yaml.dump(content, f)


@adventure.route("/adventures/select/<adventure>", methods=["POST"])
def select_adventure(adventure):
    full_path = os.path.join(ADVENTURE_ROOT, adventure)
    os.makedirs(full_path, exist_ok=True)
    os.makedirs(os.path.dirname(ACTIVE_PATH), exist_ok=True)
    with open(ACTIVE_PATH, 'w') as f:
        f.write(adventure)

    # 🆕 Initialize folder and YAML structure
    init_adventure_structure(adventure)

    return jsonify({"selected": adventure})

@adventure.route("/adventures/active", methods=["GET"])
def get_active_adventure():
    if not os.path.exists(ACTIVE_PATH):
        return jsonify({"active": None})
    with open(ACTIVE_PATH, 'r') as f:
        adventure = f.read().strip()
    return jsonify({"active": adventure})

def reset_active_adventure():
    if os.path.exists(ACTIVE_PATH):
        os.remove(ACTIVE_PATH)

@adventure.route("/adventures/clear", methods=["POST"])
def clear_active_adventure_route():
    reset_active_adventure()
    return jsonify({"cleared": True})


# Serve Azgaar map files from /server/azgaar/
@adventure.route('/azgaar/<path:filename>')
def serve_azgaar(filename):
    azgaar_dir = os.path.join(os.path.dirname(__file__), '../azgaar')
    return send_from_directory(azgaar_dir, filename)


@adventure.route("/adventures/<adv>/upload_map", methods=["POST"])
def upload_map(adv):
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if not file.filename.endswith(".map"):
        return jsonify({"error": "Invalid file type"}), 400

    map_dir = os.path.join(ADVENTURE_ROOT, adv, "world")
    os.makedirs(map_dir, exist_ok=True)

    file.save(os.path.join(map_dir, "map.map"))
    return jsonify({"success": True})

@adventure.route("/adventures/<adv>/map_file", methods=["GET"])
def get_map_file(adv):
    print("Looking for that map file")
    map_path = os.path.join(ADVENTURE_ROOT, adv, "world", "map.map")
    if not os.path.exists(map_path):
        print("No map file")
        return jsonify({"error": "Map file not found"}), 404
    print("Map found at ", map_path)
    return send_file(map_path, as_attachment=True)
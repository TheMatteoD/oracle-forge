from flask import Blueprint, send_from_directory, jsonify, request, send_file
import os
import yaml
from werkzeug.utils import secure_filename
import glob

adventure = Blueprint('adventure', __name__)

ADVENTURE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "vault", "adventures"))
ACTIVE_PATH = os.path.join("server", "state", "active_adventure.txt")

ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_image(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

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

# --- Custom Map Image Endpoints ---

@adventure.route("/adventures/<adv>/upload_custom_map", methods=["POST"])
def upload_custom_map(adv):
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['file']
    if not allowed_image(file.filename):
        return jsonify({"error": "Invalid file type"}), 400
    map_dir = os.path.join(ADVENTURE_ROOT, adv, "world", "custom_maps")
    os.makedirs(map_dir, exist_ok=True)
    filename = secure_filename(file.filename)
    save_path = os.path.join(map_dir, filename)
    file.save(save_path)
    return jsonify({"success": True, "filename": filename})

@adventure.route("/adventures/<adv>/custom_maps", methods=["GET"])
def list_custom_maps(adv):
    map_dir = os.path.join(ADVENTURE_ROOT, adv, "world", "custom_maps")
    if not os.path.exists(map_dir):
        return jsonify([])
    files = [f for f in os.listdir(map_dir) if allowed_image(f)]
    return jsonify(files)

@adventure.route("/adventures/<adv>/custom_maps/<filename>", methods=["GET"])
def serve_custom_map(adv, filename):
    map_dir = os.path.join(ADVENTURE_ROOT, adv, "world", "custom_maps")
    if not allowed_image(filename):
        return jsonify({"error": "Invalid file type"}), 400
    return send_from_directory(map_dir, filename)

# --- World State Endpoints ---

@adventure.route("/adventures/<adv>/world_state", methods=["GET"])
def get_world_state(adv):
    path = os.path.join(ADVENTURE_ROOT, adv, "world_state.yaml")
    if not os.path.exists(path):
        return jsonify({"error": "World state not found"}), 404
    with open(path, "r") as f:
        data = yaml.safe_load(f) or {}
    return jsonify(data)

@adventure.route("/adventures/<adv>/world_state", methods=["POST"])
def update_world_state(adv):
    path = os.path.join(ADVENTURE_ROOT, adv, "world_state.yaml")
    data = request.json
    with open(path, "w") as f:
        yaml.dump(data, f)
    return jsonify({"success": True})

# --- World Entity CRUD Endpoints ---

ENTITY_TYPES = ["npcs", "factions", "locations", "story_lines"]

@adventure.route("/adventures/<adv>/world/<entity_type>", methods=["GET"])
def list_entities(adv, entity_type):
    if entity_type not in ENTITY_TYPES:
        return jsonify({"error": "Invalid entity type"}), 400
    folder = os.path.join(ADVENTURE_ROOT, adv, "world", entity_type)
    if not os.path.exists(folder):
        return jsonify([])
    files = glob.glob(os.path.join(folder, "*.yaml"))
    entities = []
    for file in files:
        with open(file, "r") as f:
            entities.append(yaml.safe_load(f))
    return jsonify(entities)

@adventure.route("/adventures/<adv>/world/<entity_type>/<entity_name>", methods=["GET"])
def get_entity(adv, entity_type, entity_name):
    if entity_type not in ENTITY_TYPES:
        return jsonify({"error": "Invalid entity type"}), 400
    file = os.path.join(ADVENTURE_ROOT, adv, "world", entity_type, f"{entity_name}.yaml")
    if not os.path.exists(file):
        return jsonify({"error": "Entity not found"}), 404
    with open(file, "r") as f:
        data = yaml.safe_load(f)
    return jsonify(data)

@adventure.route("/adventures/<adv>/world/<entity_type>/<entity_name>", methods=["POST"])
def create_or_update_entity(adv, entity_type, entity_name):
    if entity_type not in ENTITY_TYPES:
        return jsonify({"error": "Invalid entity type"}), 400
    file = os.path.join(ADVENTURE_ROOT, adv, "world", entity_type, f"{entity_name}.yaml")
    data = request.json
    with open(file, "w") as f:
        yaml.dump(data, f)
    return jsonify({"success": True})

@adventure.route("/adventures/<adv>/world/<entity_type>/<entity_name>", methods=["DELETE"])
def delete_entity(adv, entity_type, entity_name):
    if entity_type not in ENTITY_TYPES:
        return jsonify({"error": "Invalid entity type"}), 400
    file = os.path.join(ADVENTURE_ROOT, adv, "world", entity_type, f"{entity_name}.yaml")
    if not os.path.exists(file):
        return jsonify({"error": "Entity not found"}), 404
    os.remove(file)
    return jsonify({"success": True})
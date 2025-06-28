from flask import Blueprint, send_from_directory, jsonify, request, send_file
import os
from werkzeug.utils import secure_filename
from ..services.adventure import AdventureService
from ..config import get_config
import logging

adventure = Blueprint('adventure', __name__)

config = get_config()
ADVENTURE_ROOT = config.database.adventures_path
ACTIVE_PATH = os.path.join("server", "state", "active_adventure.txt")

ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg"}

# Initialize service
adventure_service = AdventureService()

logger = logging.getLogger(__name__)

def allowed_image(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

@adventure.route("/adventures/list", methods=["GET"])
def list_adventures():
    try:
        adventures = adventure_service.list_adventures()
        return jsonify(adventures)
    except Exception as e:
        # Only catch unexpected system errors
        logger.error(f"Unexpected error in list_adventures: {e}")
        return jsonify({"error": "Internal server error"}), 500

@adventure.route("/adventures/select/<adventure>", methods=["POST"])
def select_adventure(adventure):
    try:
        result = adventure_service.select_adventure(adventure)
        if result["success"]:
            return jsonify({"selected": adventure})
        else:
            return jsonify({"error": result["error"]}), 400
    except Exception as e:
        # Only catch unexpected system errors
        logger.error(f"Unexpected error in select_adventure: {e}")
        return jsonify({"error": "Internal server error"}), 500

@adventure.route("/adventures/active", methods=["GET"])
def get_active_adventure():
    try:
        active_adventure = adventure_service.get_active_adventure()
        return jsonify({"active": active_adventure})
    except Exception as e:
        # Only catch unexpected system errors
        logger.error(f"Unexpected error in get_active_adventure: {e}")
        return jsonify({"error": "Internal server error"}), 500

@adventure.route("/adventures/clear", methods=["POST"])
def clear_active_adventure_route():
    try:
        result = adventure_service.clear_active_adventure()
        if result["success"]:
            return jsonify({"cleared": True})
        else:
            return jsonify({"error": result["error"]}), 500
    except Exception as e:
        # Only catch unexpected system errors
        logger.error(f"Unexpected error in clear_active_adventure: {e}")
        return jsonify({"error": "Internal server error"}), 500


# Serve Azgaar map files from /server/azgaar/
@adventure.route('/azgaar/<path:filename>')
def serve_azgaar(filename):
    azgaar_dir = os.path.join(os.path.dirname(__file__), '../azgaar')
    return send_from_directory(azgaar_dir, filename)


@adventure.route("/adventures/<adv>/upload_map", methods=["POST"])
def upload_map(adv):
    # HTTP-specific validation
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if not file.filename.endswith(".map"):
        return jsonify({"error": "Invalid file type"}), 400

    try:
        # Read file data
        file_data = file.read()
        result = adventure_service.upload_map_file(adv, file_data, file.filename)
        
        if result["success"]:
            return jsonify({"success": True})
        else:
            return jsonify({"error": result["error"]}), 400
    except Exception as e:
        logger.error(f"Unexpected error in upload_map: {e}")
        return jsonify({"error": "Internal server error"}), 500

@adventure.route("/adventures/<adv>/map_file", methods=["GET"])
def get_map_file(adv):
    try:
        map_path = adventure_service.get_map_file_path(adv)
        if map_path and os.path.exists(map_path):
            return send_file(map_path, as_attachment=True)
        else:
            return jsonify({"error": "Map file not found"}), 404
    except Exception as e:
        logger.error(f"Unexpected error in get_map_file: {e}")
        return jsonify({"error": "Internal server error"}), 500

# --- Custom Map Image Endpoints ---

@adventure.route("/adventures/<adv>/upload_custom_map", methods=["POST"])
def upload_custom_map(adv):
    # HTTP-specific validation
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['file']
    if not allowed_image(file.filename):
        return jsonify({"error": "Invalid file type"}), 400
    
    try:
        # Read file data
        file_data = file.read()
        result = adventure_service.upload_custom_map_image(adv, file_data, file.filename)
        
        if result["success"]:
            return jsonify({"success": True, "filename": result["filename"]})
        else:
            return jsonify({"error": result["error"]}), 400
    except Exception as e:
        logger.error(f"Unexpected error in upload_custom_map: {e}")
        return jsonify({"error": "Internal server error"}), 500

@adventure.route("/adventures/<adv>/custom_maps", methods=["GET"])
def list_custom_maps(adv):
    try:
        files = adventure_service.list_custom_map_images(adv)
        return jsonify(files)
    except Exception as e:
        logger.error(f"Unexpected error in list_custom_maps: {e}")
        return jsonify({"error": "Internal server error"}), 500

@adventure.route("/adventures/<adv>/custom_maps/<filename>", methods=["GET"])
def serve_custom_map(adv, filename):
    # HTTP-specific validation
    if not allowed_image(filename):
        return jsonify({"error": "Invalid file type"}), 400
    
    try:
        map_path = adventure_service.get_custom_map_image_path(adv, filename)
        if map_path and os.path.exists(map_path):
            return send_from_directory(os.path.dirname(map_path), filename)
        else:
            return jsonify({"error": "Custom map not found"}), 404
    except Exception as e:
        logger.error(f"Unexpected error in serve_custom_map: {e}")
        return jsonify({"error": "Internal server error"}), 500

# --- World State Endpoints ---

@adventure.route("/adventures/<adv>/world_state", methods=["GET"])
def get_world_state(adv):
    try:
        world_state = adventure_service.get_world_state(adv)
        if world_state:
            return jsonify(world_state)
        else:
            return jsonify({"error": "World state not found"}), 404
    except Exception as e:
        logger.error(f"Unexpected error in get_world_state: {e}")
        return jsonify({"error": "Internal server error"}), 500

@adventure.route("/adventures/<adv>/world_state", methods=["POST"])
def update_world_state(adv):
    # HTTP-specific validation
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    try:
        result = adventure_service.update_world_state(adv, data)
        if result["success"]:
            return jsonify({"success": True})
        else:
            return jsonify({"error": result["error"]}), 400
    except Exception as e:
        logger.error(f"Unexpected error in update_world_state: {e}")
        return jsonify({"error": "Internal server error"}), 500

# --- World Entity CRUD Endpoints ---

ENTITY_TYPES = ["npcs", "factions", "locations", "story_lines"]

@adventure.route("/adventures/<adv>/world/<entity_type>", methods=["GET"])
def list_entities(adv, entity_type):
    # HTTP-specific validation
    if entity_type not in ENTITY_TYPES:
        return jsonify({"error": "Invalid entity type"}), 400
    
    try:
        result = adventure_service.list_world_entities(adv, entity_type)
        if result["success"]:
            return jsonify(result["entities"])
        else:
            return jsonify({"error": result["error"]}), 400
    except Exception as e:
        logger.error(f"Unexpected error in list_entities: {e}")
        return jsonify({"error": "Internal server error"}), 500

@adventure.route("/adventures/<adv>/world/<entity_type>/<entity_name>", methods=["GET"])
def get_entity(adv, entity_type, entity_name):
    # HTTP-specific validation
    if entity_type not in ENTITY_TYPES:
        return jsonify({"error": "Invalid entity type"}), 400
    
    try:
        result = adventure_service.get_world_entity(adv, entity_type, entity_name)
        if result["success"]:
            return jsonify(result["entity"])
        else:
            return jsonify({"error": result["error"]}), 404
    except Exception as e:
        logger.error(f"Unexpected error in get_entity: {e}")
        return jsonify({"error": "Internal server error"}), 500

@adventure.route("/adventures/<adv>/world/<entity_type>/<entity_name>", methods=["POST"])
def create_or_update_entity(adv, entity_type, entity_name):
    # HTTP-specific validation
    if entity_type not in ENTITY_TYPES:
        return jsonify({"error": "Invalid entity type"}), 400
    
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Add entity name to data if not present
    if "name" not in data:
        data["name"] = entity_name
    
    try:
        result = adventure_service.create_world_entity(adv, entity_type, data)
        if result["success"]:
            return jsonify({"success": True})
        else:
            return jsonify({"error": result["error"]}), 400
    except Exception as e:
        logger.error(f"Unexpected error in create_or_update_entity: {e}")
        return jsonify({"error": "Internal server error"}), 500

@adventure.route("/adventures/<adv>/world/<entity_type>/<entity_name>", methods=["DELETE"])
def delete_entity(adv, entity_type, entity_name):
    # HTTP-specific validation
    if entity_type not in ENTITY_TYPES:
        return jsonify({"error": "Invalid entity type"}), 400
    
    try:
        result = adventure_service.delete_world_entity(adv, entity_type, entity_name)
        if result["success"]:
            return jsonify({"success": True})
        else:
            return jsonify({"error": result["error"]}), 404
    except Exception as e:
        logger.error(f"Unexpected error in delete_entity: {e}")
        return jsonify({"error": "Internal server error"}), 500
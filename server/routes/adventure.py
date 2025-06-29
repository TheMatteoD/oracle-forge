from flask import Blueprint, send_from_directory, request, send_file, g
import os
from werkzeug.utils import secure_filename
from ..services.adventure import AdventureService
from ..config import get_config
from ..utils.responses import APIResponse, handle_service_response
from ..utils.validation import validate_json_body, validate_enum_field
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
    """List all available adventures"""
    adventures = adventure_service.list_adventures()
    return APIResponse.success(adventures)

@adventure.route("/adventures/select/<adventure>", methods=["POST"])
def select_adventure(adventure):
    """Select an adventure as active"""
    result = adventure_service.select_adventure(adventure)
    return handle_service_response(result)

@adventure.route("/adventures/active", methods=["GET"])
def get_active_adventure():
    """Get the currently active adventure"""
    active_adventure = adventure_service.get_active_adventure()
    return APIResponse.success({"active": active_adventure})

@adventure.route("/adventures/clear", methods=["POST"])
def clear_active_adventure_route():
    """Clear the active adventure"""
    result = adventure_service.clear_active_adventure()
    return handle_service_response(result)

# Serve Azgaar map files from /server/azgaar/
@adventure.route('/azgaar/<path:filename>')
def serve_azgaar(filename):
    azgaar_dir = os.path.join(os.path.dirname(__file__), '../azgaar')
    return send_from_directory(azgaar_dir, filename)

@adventure.route("/adventures/<adv>/upload_map", methods=["POST"])
def upload_map(adv):
    """Upload a map file for an adventure"""
    # HTTP-specific validation
    if 'file' not in request.files:
        return APIResponse.bad_request("No file uploaded")
    
    file = request.files['file']
    if not file.filename.endswith(".map"):
        return APIResponse.bad_request("Invalid file type")
    
    # Read file data
    file_data = file.read()
    result = adventure_service.upload_map_file(adv, file_data, file.filename)
    return handle_service_response(result)

@adventure.route("/adventures/<adv>/map_file", methods=["GET"])
def get_map_file(adv):
    """Get map file for an adventure"""
    map_path = adventure_service.get_map_file_path(adv)
    if map_path and os.path.exists(map_path):
        return send_file(map_path, as_attachment=True)
    else:
        return APIResponse.not_found("Map file not found")

# --- Custom Map Image Endpoints ---

@adventure.route("/adventures/<adv>/upload_custom_map", methods=["POST"])
def upload_custom_map(adv):
    """Upload a custom map image for an adventure"""
    # HTTP-specific validation
    if 'file' not in request.files:
        return APIResponse.bad_request("No file uploaded")
    
    file = request.files['file']
    if not allowed_image(file.filename):
        return APIResponse.bad_request("Invalid file type")
    
    # Read file data
    file_data = file.read()
    result = adventure_service.upload_custom_map_image(adv, file_data, file.filename)
    return handle_service_response(result)

@adventure.route("/adventures/<adv>/custom_maps", methods=["GET"])
def list_custom_maps(adv):
    """List custom map images for an adventure"""
    files = adventure_service.list_custom_map_images(adv)
    return APIResponse.success(files)

@adventure.route("/adventures/<adv>/custom_maps/<filename>", methods=["GET"])
def serve_custom_map(adv, filename):
    """Serve a custom map image"""
    # HTTP-specific validation
    if not allowed_image(filename):
        return APIResponse.bad_request("Invalid file type")
    
    map_path = adventure_service.get_custom_map_image_path(adv, filename)
    if map_path and os.path.exists(map_path):
        return send_from_directory(os.path.dirname(map_path), filename)
    else:
        return APIResponse.not_found("Custom map not found")

# --- World State Endpoints ---

@adventure.route("/adventures/<adv>/world_state", methods=["GET"])
def get_world_state(adv):
    """Get world state for an adventure"""
    world_state = adventure_service.get_world_state(adv)
    if world_state:
        return APIResponse.success(world_state)
    else:
        return APIResponse.not_found("World state not found")

@adventure.route("/adventures/<adv>/world_state", methods=["POST"])
@validate_json_body(required_fields=[])
def update_world_state(adv):
    """Update world state for an adventure"""
    data = g.request_data
    
    result = adventure_service.update_world_state(adv, data)
    return handle_service_response(result)

# --- World Entity CRUD Endpoints ---

ENTITY_TYPES = ["npcs", "factions", "locations", "story_lines"]

@adventure.route("/adventures/<adv>/world/<entity_type>", methods=["GET"])
@validate_enum_field("entity_type", ENTITY_TYPES, allow_none=False)
def list_entities(adv, entity_type):
    """List entities of a specific type"""
    result = adventure_service.list_world_entities(adv, entity_type)
    return handle_service_response(result, "entities")

@adventure.route("/adventures/<adv>/world/<entity_type>/<entity_name>", methods=["GET"])
@validate_enum_field("entity_type", ENTITY_TYPES, allow_none=False)
def get_entity(adv, entity_type, entity_name):
    """Get a specific entity"""
    result = adventure_service.get_world_entity(adv, entity_type, entity_name)
    return handle_service_response(result)

@adventure.route("/adventures/<adv>/world/<entity_type>/<entity_name>", methods=["POST"])
@validate_enum_field("entity_type", ENTITY_TYPES, allow_none=False)
@validate_json_body(required_fields=["entity_data"])
def create_or_update_entity(adv, entity_type, entity_name):
    """Create or update an entity"""
    data = g.request_data
    
    result = adventure_service.create_or_update_world_entity(adv, entity_type, entity_name, data)
    return handle_service_response(result)

@adventure.route("/adventures/<adv>/world/<entity_type>/<entity_name>", methods=["DELETE"])
@validate_enum_field("entity_type", ENTITY_TYPES, allow_none=False)
def delete_entity(adv, entity_type, entity_name):
    """Delete an entity"""
    result = adventure_service.delete_world_entity(adv, entity_type, entity_name)
    return handle_service_response(result)
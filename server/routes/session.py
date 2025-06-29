from flask import Blueprint, request, g
import logging
from ..services.session import SessionService
from ..utils.responses import APIResponse, handle_service_response
from ..utils.validation import validate_json_body, validate_field

session = Blueprint('session', __name__)
session_service = SessionService()
logger = logging.getLogger(__name__)

@session.route("/session/state", methods=["GET"])
def session_state():
    """Get current session state"""
    # Call service
    result = session_service.get_session_state()
    return handle_service_response(result, "state")

@session.route("/session/log", methods=["GET"])
def get_session_log():
    """Get session log entries"""
    # Call service
    result = session_service.get_session_log()
    return handle_service_response(result, "log")

@session.route("/session/log", methods=["POST"])
@validate_json_body(required_fields=["content"])
@validate_field("content", field_type=str, min_length=1, allow_empty=False)
def append_session_log():
    """Append entry to session log"""
    data = g.request_data
    # Call service
    result = session_service.append_session_log(data)
    return handle_service_response(result)

@session.route("/session/character/<character_name>", methods=["GET"])
def get_character(character_name):
    """Get character by name"""
    if not character_name:
        return APIResponse.bad_request("Character name is required")
    # Call service
    result = session_service.get_character(character_name)
    return handle_service_response(result)

@session.route("/session/character/<character_name>", methods=["POST"])
@validate_json_body(required_fields=["character_data"])
def create_or_update_character(character_name):
    """Create or update character"""
    data = g.request_data
    # Call service
    result = session_service.create_or_update_character(character_name, data)
    return handle_service_response(result)

@session.route("/session/character/<character_name>", methods=["DELETE"])
def delete_character(character_name):
    """Delete character by name"""
    if not character_name:
        return APIResponse.bad_request("Character name is required")
    # Call service
    result = session_service.delete_character(character_name)
    return handle_service_response(result)

@session.route("/session/characters", methods=["GET"])
def list_characters():
    """List all characters in session"""
    # Call service
    result = session_service.list_characters()
    return handle_service_response(result, "characters")

@session.route("/session/characters", methods=["POST"])
@validate_json_body(required_fields=["characters"])
@validate_field("characters", field_type=list, allow_none=False)
def bulk_update_characters():
    """Bulk update characters"""
    data = g.request_data
    # Call service
    result = session_service.bulk_update_characters(data.get("characters", []))
    return handle_service_response(result)

@session.route("/session/clear", methods=["POST"])
def clear_session():
    """Clear all session data"""
    # Call service
    result = session_service.clear_session()
    return handle_service_response(result)

@session.route("/session/end", methods=["POST"])
def end_session():
    """End the current session"""
    # Call service
    result = session_service.end_session()
    return handle_service_response(result)

@session.route("/session/export", methods=["GET"])
def export_session():
    """Export session data"""
    # Call service
    result = session_service.export_session()
    return handle_service_response(result, "session_data")

@session.route("/session/import", methods=["POST"])
@validate_json_body(required_fields=["session_data"])
def import_session():
    """Import session data"""
    data = g.request_data
    # Call service
    result = session_service.import_session(data.get("session_data"))
    return handle_service_response(result)


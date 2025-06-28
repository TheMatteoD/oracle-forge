from flask import Blueprint, jsonify, request
import logging
from ..services.session import SessionService

session = Blueprint("session", __name__)
session_service = SessionService()
logger = logging.getLogger(__name__)

@session.route("/session/character", methods=["POST"])
def create_character():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        name = data.get("name", "").strip()
        if not name:
            return jsonify({"error": "Character name is required"}), 400
        
        # Call service
        result = session_service.create_character(name)
        
        if result["success"]:
            return jsonify(result)
        else:
            return jsonify({"error": result["error"]}), 400
            
    except Exception as e:
        logger.error(f"Unexpected error in create_character: {e}")
        return jsonify({"error": "Internal server error"}), 500

@session.route("/session/state", methods=["GET"])
def session_state():
    try:
        # Call service
        result = session_service.get_session_state()
        
        if result["success"]:
            return jsonify(result["state"])
        else:
            return jsonify({"error": result["error"]}), 400
            
    except Exception as e:
        logger.error(f"Unexpected error in session_state: {e}")
        return jsonify({"error": "Internal server error"}), 500

@session.route("/session/log", methods=["GET"])
def get_session_log():
    try:
        # Call service
        result = session_service.get_session_log()
        
        if result["success"]:
            return jsonify(result["log"])
        else:
            return jsonify({"error": result["error"]}), 400
            
    except Exception as e:
        logger.error(f"Unexpected error in get_session_log: {e}")
        return jsonify({"error": "Internal server error"}), 500

@session.route("/session/log", methods=["POST"])
def append_session_log():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        if not data.get("content"):
            return jsonify({"error": "Empty log entry"}), 400
        
        # Call service
        result = session_service.append_session_log(data)
        
        if result["success"]:
            return jsonify(result)
        else:
            return jsonify({"error": result["error"]}), 400
            
    except Exception as e:
        logger.error(f"Unexpected error in append_session_log: {e}")
        return jsonify({"error": "Internal server error"}), 500

@session.route("/session/character/<character_name>", methods=["GET"])
def get_character(character_name):
    try:
        if not character_name:
            return jsonify({"error": "Character name is required"}), 400
        
        # Call service
        result = session_service.get_character(character_name)
        
        if result["success"]:
            return jsonify(result)
        else:
            return jsonify({"error": result["error"]}), 404
            
    except Exception as e:
        logger.error(f"Unexpected error in get_character: {e}")
        return jsonify({"error": "Internal server error"}), 500

@session.route("/session/character/<character_name>", methods=["PUT"])
def update_character(character_name):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        if not character_name:
            return jsonify({"error": "Character name is required"}), 400
        
        character_data = data.get("character", {})
        if not character_data:
            return jsonify({"error": "Character data is required"}), 400
        
        # Call service
        result = session_service.update_character(character_name, character_data)
        
        if result["success"]:
            return jsonify(result)
        else:
            return jsonify({"error": result["error"]}), 400
            
    except Exception as e:
        logger.error(f"Unexpected error in update_character: {e}")
        return jsonify({"error": "Internal server error"}), 500

@session.route("/session/end", methods=["POST"])
def end_session():
    try:
        # Call service
        result = session_service.end_session()
        
        if result["success"]:
            return jsonify(result)
        else:
            return jsonify({"error": result["error"]}), 400
            
    except Exception as e:
        logger.error(f"Unexpected error in end_session: {e}")
        return jsonify({"error": "Internal server error"}), 500


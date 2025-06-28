from flask import Blueprint, request, jsonify
import logging
from ..services.oracle import OracleService

oracle = Blueprint('oracle', __name__)
oracle_service = OracleService()
logger = logging.getLogger(__name__)

@oracle.route("/oracle/yesno", methods=["POST"])
def oracle_yesno():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        question = data.get("question", "").strip()
        odds = data.get("odds", "50/50")
        chaos = int(data.get("chaos", 5))
        
        if not question:
            return jsonify({"error": "Question is required"}), 400
        
        # Call service
        result = oracle_service.yes_no_query(question=question, odds=odds, chaos=chaos)
        
        if result["success"]:
            return jsonify(result["result"])
        else:
            return jsonify({"error": result["error"]}), 400
            
    except Exception as e:
        logger.error(f"Unexpected error in oracle_yesno: {e}")
        return jsonify({"error": "Internal server error"}), 500

@oracle.route("/oracle/yesno/flavor", methods=["POST"])
def oracle_yesno_flavor():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        question = data.get("question", "").strip()
        outcome = data.get("result", "").strip()
        event_trigger = data.get("event_trigger", "").strip()
        
        if not question or not outcome:
            return jsonify({"error": "Question and result are required"}), 400
        
        # Call service
        result = oracle_service.yes_no_narration(
            question=question, 
            outcome=outcome, 
            event_trigger=event_trigger
        )
        
        if result["success"]:
            return jsonify({"narration": result["narration"]})
        else:
            return jsonify({"error": result["error"]}), 400
            
    except Exception as e:
        logger.error(f"Unexpected error in oracle_yesno_flavor: {e}")
        return jsonify({"error": "Internal server error"}), 500

@oracle.route("/oracle/scene", methods=["POST"])
def oracle_scene():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        chaos = int(data.get("chaos", 5))
        flavor = bool(data.get("flavor", False))
        
        # Call service
        result = oracle_service.scene_test(chaos=chaos, flavor=flavor)
        
        if result["success"]:
            return jsonify(result["result"])
        else:
            return jsonify({"error": result["error"]}), 400
            
    except Exception as e:
        logger.error(f"Unexpected error in oracle_scene: {e}")
        return jsonify({"error": "Internal server error"}), 500

@oracle.route("/oracle/scene/flavor", methods=["POST"])
def oracle_scene_flavor():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        focus = data.get("focus", "").strip()
        expectation = data.get("expectation", "").strip()
        
        if not focus:
            return jsonify({"error": "Focus is required"}), 400
        
        # Call service
        result = oracle_service.scene_narration(focus=focus, expectation=expectation)
        
        if result["success"]:
            return jsonify({"narration": result["narration"]})
        else:
            return jsonify({"error": result["error"]}), 400
            
    except Exception as e:
        logger.error(f"Unexpected error in oracle_scene_flavor: {e}")
        return jsonify({"error": "Internal server error"}), 500

@oracle.route("/oracle/meaning", methods=["POST"])
def oracle_meaning():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        question = data.get("question", "").strip()
        table = data.get("table", "").strip()
        
        if not question:
            return jsonify({"error": "Question is required"}), 400
        if not table:
            return jsonify({"error": "Table is required"}), 400
        
        # Call service
        result = oracle_service.meaning_query(question=question, table=table)
        
        if result["success"]:
            return jsonify(result["result"])
        else:
            return jsonify({"error": result["error"]}), 400
            
    except Exception as e:
        logger.error(f"Unexpected error in oracle_meaning: {e}")
        return jsonify({"error": "Internal server error"}), 500

@oracle.route("/oracle/meaning/flavor", methods=["POST"])
def oracle_meaning_flavor():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        question = data.get("question", "").strip()
        keywords = data.get("keywords", [])
        
        if not question:
            return jsonify({"error": "Question is required"}), 400
        if not keywords:
            return jsonify({"error": "Keywords are required"}), 400
        
        # Call service
        result = oracle_service.meaning_narration(question=question, keywords=keywords)
        
        if result["success"]:
            return jsonify({"narration": result["narration"]})
        else:
            return jsonify({"error": result["error"]}), 400
            
    except Exception as e:
        logger.error(f"Unexpected error in oracle_meaning_flavor: {e}")
        return jsonify({"error": "Internal server error"}), 500

@oracle.route("/oracle/meaning/tables", methods=["GET"])
def oracle_meaning_tables():
    try:
        # Call service
        result = oracle_service.list_oracle_tables()
        
        if result["success"]:
            return jsonify(result["tables"])
        else:
            return jsonify({"error": result["error"]}), 400
            
    except Exception as e:
        logger.error(f"Unexpected error in oracle_meaning_tables: {e}")
        return jsonify({"error": "Internal server error"}), 500

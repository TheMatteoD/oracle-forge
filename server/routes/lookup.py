# server/routes/lookup.py
from flask import Blueprint, request, jsonify
import logging
from ..services.lookup import LookupService

lookup = Blueprint('lookup', __name__)
lookup_service = LookupService()
logger = logging.getLogger(__name__)

@lookup.route("/lookup/monster", methods=["POST"])
def lookup_monster():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Extract parameters
        query = data.get("query", "").strip()
        system = data.get("system", "").strip()
        tag = data.get("tag", "").strip()
        random_count = data.get("random", 0)
        environment = data.get("environment", "").strip()
        theme = data.get("theme", "").strip()
        context = data.get("context", "").strip()
        narrate = data.get("narrate", False)
        
        # Call service
        result = lookup_service.lookup_monsters(
            query=query,
            system=system,
            tag=tag,
            environment=environment,
            random_count=random_count,
            narrate=narrate,
            context=context,
            theme=theme
        )
        
        if result["success"]:
            return jsonify(result)
        else:
            return jsonify({"error": result["error"]}), 400
            
    except Exception as e:
        logger.error(f"Unexpected error in lookup_monster: {e}")
        return jsonify({"error": "Internal server error"}), 500

@lookup.route("/lookup/spell", methods=["POST"])
def lookup_spell():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Extract parameters
        query = data.get("query", "").strip()
        system = data.get("system", "").strip()
        spell_class = data.get("class", "").strip()
        tag = data.get("tag", "").strip()
        level = data.get("level")
        random_count = data.get("random", 0)
        theme = data.get("theme", "").strip()
        context = data.get("context", "").strip()
        narrate = data.get("narrate", False)
        
        # Call service
        result = lookup_service.lookup_spells(
            query=query,
            system=system,
            spell_class=spell_class,
            level=level,
            tag=tag,
            random_count=random_count,
            narrate=narrate,
            context=context,
            theme=theme
        )
        
        if result["success"]:
            return jsonify(result)
        else:
            return jsonify({"error": result["error"]}), 400
            
    except Exception as e:
        logger.error(f"Unexpected error in lookup_spell: {e}")
        return jsonify({"error": "Internal server error"}), 500

@lookup.route("/lookup/item", methods=["POST"])
def lookup_item():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Extract parameters
        query = data.get("query", "").strip()
        system = data.get("system", "").strip()
        category = data.get("category", "").strip()
        subcategory = data.get("subcategory", "").strip()
        tag = data.get("tag", "").strip()
        random_count = data.get("random", 0)
        environment = data.get("environment", "").strip()
        quality = data.get("quality", "").strip()
        theme = data.get("theme", "").strip()
        context = data.get("context", "").strip()
        narrate = data.get("narrate", False)
        
        # Call service
        result = lookup_service.lookup_items(
            query=query,
            system=system,
            category=category,
            subcategory=subcategory,
            tag=tag,
            random_count=random_count,
            narrate=narrate,
            context=context,
            environment=environment,
            quality=quality,
            theme=theme
        )
        
        if result["success"]:
            return jsonify(result)
        else:
            return jsonify({"error": result["error"]}), 400
            
    except Exception as e:
        logger.error(f"Unexpected error in lookup_item: {e}")
        return jsonify({"error": "Internal server error"}), 500

@lookup.route("/lookup/rewrite", methods=["POST"])
def rewrite_lookup_narration():
    """Rewrite an existing narration based on user instructions."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        original_narration = data.get("narration", "").strip()
        rewrite_instruction = data.get("instruction", "").strip()
        
        if not original_narration or not rewrite_instruction:
            return jsonify({"error": "Both narration and instruction are required"}), 400
        
        # Call service
        result = lookup_service.rewrite_narration(original_narration, rewrite_instruction)
        
        if result["success"]:
            return jsonify(result)
        else:
            return jsonify({"error": result["error"]}), 400
            
    except Exception as e:
        logger.error(f"Unexpected error in rewrite_lookup_narration: {e}")
        return jsonify({"error": "Internal server error"}), 500

@lookup.route("/lookup/rule", methods=["POST"])
def lookup_rule():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        query = data.get("query", "").strip()
        system = data.get("system", "").strip()
        tag = data.get("tag", "").strip()
        
        # Call service
        result = lookup_service.lookup_rules(query=query, system=system, tag=tag)
        
        if result["success"]:
            return jsonify(result)
        else:
            return jsonify({"error": result["error"]}), 400
            
    except Exception as e:
        logger.error(f"Unexpected error in lookup_rule: {e}")
        return jsonify({"error": "Internal server error"}), 500

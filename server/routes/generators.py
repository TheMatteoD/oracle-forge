"""
Generator routes for Oracle Forge

This module provides API endpoints for generator operations including:
- Table-based generators (dungeons, etc.)
- Custom generators (programmatic generators)
- Generator flavoring and narration
"""

from flask import Blueprint, request, jsonify
import logging
from ..services.generator import GeneratorService

generators = Blueprint("generators", __name__)
generator_service = GeneratorService()

logger = logging.getLogger(__name__)


@generators.route("/generators/categories", methods=["GET"])
def list_categories():
    """List all available generator categories"""
    try:
        categories = generator_service.list_generator_types()
        return jsonify(categories)
    except Exception as e:
        # Only catch unexpected system errors
        logger.error(f"Unexpected error in list_categories: {e}")
        return jsonify({"error": "Internal server error"}), 500


@generators.route("/generators/<category>/files", methods=["GET"])
def list_files(category):
    """List all generator files in a category"""
    try:
        files = generator_service.list_generators(category)
        return jsonify(files)
    except Exception as e:
        # Only catch unexpected system errors
        logger.error(f"Unexpected error in list_files: {e}")
        return jsonify({"error": "Internal server error"}), 500


@generators.route("/generators/<category>/<filename>/tables", methods=["GET"])
def list_tables(category, filename):
    """List all tables in a generator file"""
    try:
        generator_data = generator_service.get_generator(category, filename)
        table_ids = [table.get('id') for table in generator_data.get('tables', []) if table.get('id')]
        return jsonify(table_ids)
    except Exception as e:
        # Only catch unexpected system errors
        logger.error(f"Unexpected error in list_tables: {e}")
        return jsonify({"error": "Internal server error"}), 500


@generators.route("/generators/custom", methods=["GET"])
def list_custom_generators():
    """List all available custom generators"""
    try:
        custom_generators = generator_service.list_custom_generators()
        return jsonify(custom_generators)
    except Exception as e:
        # Only catch unexpected system errors
        logger.error(f"Unexpected error in list_custom_generators: {e}")
        return jsonify({"error": "Internal server error"}), 500


@generators.route("/generators/custom/<category>/<system>/<generator_id>", methods=["POST"])
def run_custom_generator(category, system, generator_id):
    """Execute a custom generator"""
    try:
        data = request.get_json() or {}
        parameters = data.get('parameters', {})
        
        result = generator_service.execute_custom_generator(category, system, generator_id, parameters)
        if result.get("success"):
            return jsonify(result)
        else:
            return jsonify({"error": result.get("error", "Unknown error")}), 400
    except Exception as e:
        # Only catch unexpected system errors
        logger.error(f"Unexpected error in run_custom_generator: {e}")
        return jsonify({"error": "Internal server error"}), 500


@generators.route("/generators/roll", methods=["POST"])
def roll_table():
    """Roll on a specific table within a generator"""
    # HTTP-specific validation
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400
    
    category = data.get("category")
    filename = data.get("file")
    table_id = data.get("table_id")
    
    if not all([category, filename, table_id]):
        return jsonify({"error": "category, file, and table_id are required"}), 400
    
    try:
        result = generator_service.roll_table(category, filename, table_id)
        if result.get("success"):
            return jsonify(result)
        else:
            return jsonify({"error": result.get("error", "Unknown error")}), 400
    except Exception as e:
        # Only catch unexpected system errors
        logger.error(f"Unexpected error in roll_table: {e}")
        return jsonify({"error": "Internal server error"}), 500


@generators.route("/generators/flavor", methods=["POST"])
def generate_flavor():
    """Generate flavored narration for generator results"""
    try:
        data = request.get_json() or {}
        
        context = data.get("context", "")
        result_data = data.get("data", {})
        category = data.get("category", "")
        source = data.get("source", "")
        
        result = generator_service.generate_flavor(context, result_data, category, source)
        if result.get("success"):
            return jsonify({"narration": result.get("narration")})
        else:
            return jsonify({"error": result.get("error", "Unknown error")}), 400
    except Exception as e:
        # Only catch unexpected system errors
        logger.error(f"Unexpected error in generate_flavor: {e}")
        return jsonify({"error": "Internal server error"}), 500


# Additional CRUD endpoints for generators
@generators.route("/generators/<category>/<filename>", methods=["GET"])
def get_generator(category, filename):
    """Get a specific generator"""
    try:
        generator_data = generator_service.get_generator(category, filename)
        if generator_data:
            return jsonify(generator_data)
        else:
            return jsonify({"error": f"Generator '{filename}' not found"}), 404
    except Exception as e:
        # Only catch unexpected system errors
        logger.error(f"Unexpected error in get_generator: {e}")
        return jsonify({"error": "Internal server error"}), 500


@generators.route("/generators/<category>", methods=["POST"])
def create_generator(category):
    """Create a new generator in a category"""
    # HTTP-specific validation
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400
    
    try:
        result = generator_service.create_generator(category, data)
        if result.get("success"):
            return jsonify(result.get("generator")), 201
        else:
            return jsonify({"error": result.get("error", "Unknown error")}), 400
    except Exception as e:
        # Only catch unexpected system errors
        logger.error(f"Unexpected error in create_generator: {e}")
        return jsonify({"error": "Internal server error"}), 500


@generators.route("/generators/<category>/<filename>", methods=["PUT"])
def update_generator(category, filename):
    """Update a specific generator"""
    # HTTP-specific validation
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400
    
    try:
        result = generator_service.update_generator(category, filename, data)
        if result.get("success"):
            return jsonify(result.get("generator"))
        else:
            return jsonify({"error": result.get("error", "Unknown error")}), 400
    except Exception as e:
        # Only catch unexpected system errors
        logger.error(f"Unexpected error in update_generator: {e}")
        return jsonify({"error": "Internal server error"}), 500


@generators.route("/generators/<category>/<filename>", methods=["DELETE"])
def delete_generator(category, filename):
    """Delete a specific generator"""
    try:
        result = generator_service.delete_generator(category, filename)
        if result.get("success"):
            return jsonify({"message": result.get("message")}), 200
        else:
            return jsonify({"error": result.get("error", "Unknown error")}), 400
    except Exception as e:
        # Only catch unexpected system errors
        logger.error(f"Unexpected error in delete_generator: {e}")
        return jsonify({"error": "Internal server error"}), 500


@generators.route("/generators/search", methods=["GET"])
def search_generators():
    """Search for generators"""
    # HTTP-specific validation
    query = request.args.get("q", "")
    generator_type = request.args.get("type")
    
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400
    
    try:
        results = generator_service.search_generators(query, generator_type)
        return jsonify(results)
    except Exception as e:
        # Only catch unexpected system errors
        logger.error(f"Unexpected error in search_generators: {e}")
        return jsonify({"error": "Internal server error"}), 500


@generators.route("/generators/<category>/<filename>/statistics", methods=["GET"])
def get_generator_statistics(category, filename):
    """Get statistics about a generator"""
    try:
        result = generator_service.get_generator_statistics(category, filename)
        if result.get("success"):
            return jsonify(result.get("statistics"))
        else:
            return jsonify({"error": result.get("error", "Unknown error")}), 400
    except Exception as e:
        # Only catch unexpected system errors
        logger.error(f"Unexpected error in get_generator_statistics: {e}")
        return jsonify({"error": "Internal server error"}), 500


@generators.route("/generators/<category>/<filename>/validate", methods=["GET"])
def validate_generator(category, filename):
    """Validate a generator's structure"""
    try:
        result = generator_service.validate_generator(category, filename)
        if result.get("success"):
            return jsonify(result.get("validation"))
        else:
            return jsonify({"error": result.get("error", "Unknown error")}), 400
    except Exception as e:
        # Only catch unexpected system errors
        logger.error(f"Unexpected error in validate_generator: {e}")
        return jsonify({"error": "Internal server error"}), 500
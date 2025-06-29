"""
Generator routes for Oracle Forge

This module provides API endpoints for generator operations including:
- Table-based generators (dungeons, etc.)
- Custom generators (programmatic generators)
- Generator flavoring and narration
"""

from flask import Blueprint, request, jsonify, g
import logging
from ..services.generator import GeneratorService
from ..utils.responses import APIResponse, handle_service_response
from ..utils.validation import validate_field, validate_json_body, validate_query_params

generators = Blueprint("generators", __name__)
generator_service = GeneratorService()
logger = logging.getLogger(__name__)


@generators.route("/generators/categories", methods=["GET"])
def list_categories():
    """List all available generator categories"""
    categories = generator_service.list_generator_types()
    return APIResponse.success(categories)


@generators.route("/generators/<category>/files", methods=["GET"])
def list_files(category):
    """List all generator files in a category"""
    files = generator_service.list_generators(category)
    return APIResponse.success(files)


@generators.route("/generators/<category>/<filename>/tables", methods=["GET"])
def list_tables(category, filename):
    """List all tables in a generator file"""
    generator_data = generator_service.get_generator(category, filename)
    table_ids = [table.get('id') for table in generator_data.get('tables', []) if table.get('id')]
    return APIResponse.success(table_ids)


@generators.route("/generators/custom", methods=["GET"])
def list_custom_generators():
    """List all available custom generators"""
    custom_generators = generator_service.list_custom_generators()
    return APIResponse.success(custom_generators)


@generators.route("/generators/custom/<category>/<system>/<generator_id>", methods=["POST"])
@validate_field("parameters", field_type=dict, allow_none=True)
def run_custom_generator(category, system, generator_id):
    """Execute a custom generator"""
    data = g.request_data or {}
    parameters = data.get('parameters', {})
    
    result = generator_service.execute_custom_generator(category, system, generator_id, parameters)
    return handle_service_response(result)


@generators.route("/generators/roll", methods=["POST"])
@validate_json_body(required_fields=["category", "file", "table_id"])
def roll_table():
    """Roll on a specific table within a generator"""
    data = g.request_data
    
    category = data.get("category")
    filename = data.get("file")
    table_id = data.get("table_id")
    
    result = generator_service.roll_table(category, filename, table_id)
    return handle_service_response(result)


@generators.route("/generators/flavor", methods=["POST"])
@validate_field("context", field_type=str, allow_none=True)
@validate_field("data", field_type=dict, allow_none=True)
@validate_field("category", field_type=str, allow_none=True)
@validate_field("source", field_type=str, allow_none=True)
def generate_flavor():
    """Generate flavored narration for generator results"""
    data = g.request_data or {}
    
    context = data.get("context", "")
    result_data = data.get("data", {})
    category = data.get("category", "")
    source = data.get("source", "")
    
    result = generator_service.generate_flavor(context, result_data, category, source)
    return handle_service_response(result, "narration")


# Additional CRUD endpoints for generators
@generators.route("/generators/<category>/<filename>", methods=["GET"])
def get_generator(category, filename):
    """Get a specific generator"""
    generator_data = generator_service.get_generator(category, filename)
    if generator_data:
        return APIResponse.success(generator_data)
    else:
        return APIResponse.not_found(f"Generator '{filename}' not found")


@generators.route("/generators/<category>", methods=["POST"])
@validate_json_body(required_fields=["name"])
def create_generator(category):
    """Create a new generator in a category"""
    data = g.request_data
    
    result = generator_service.create_generator(category, data)
    return handle_service_response(result, "generator")


@generators.route("/generators/<category>/<filename>", methods=["PUT"])
@validate_json_body(required_fields=["name"])
def update_generator(category, filename):
    """Update a specific generator"""
    data = g.request_data
    
    result = generator_service.update_generator(category, filename, data)
    return handle_service_response(result, "generator")


@generators.route("/generators/<category>/<filename>", methods=["DELETE"])
def delete_generator(category, filename):
    """Delete a specific generator"""
    result = generator_service.delete_generator(category, filename)
    return handle_service_response(result)


@generators.route("/generators/search", methods=["GET"])
@validate_query_params(required_params=["q"])
def search_generators():
    """Search for generators"""
    params = g.query_params
    
    query = params.get("q", "")
    generator_type = params.get("type")
    
    results = generator_service.search_generators(query, generator_type)
    return APIResponse.success(results)


@generators.route("/generators/<category>/<filename>/statistics", methods=["GET"])
def get_generator_statistics(category, filename):
    """Get statistics about a generator"""
    result = generator_service.get_generator_statistics(category, filename)
    return handle_service_response(result, "statistics")


@generators.route("/generators/<category>/<filename>/validate", methods=["GET"])
def validate_generator(category, filename):
    """Validate a generator's structure"""
    result = generator_service.validate_generator(category, filename)
    return handle_service_response(result, "validation")
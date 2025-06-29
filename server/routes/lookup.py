# server/routes/lookup.py
from flask import Blueprint, request, g
import logging
from ..services.lookup import LookupService
from ..utils.responses import APIResponse, handle_service_response
from ..utils.validation import validate_json_body, validate_field, validate_enum_field

lookup = Blueprint('lookup', __name__)
lookup_service = LookupService()
logger = logging.getLogger(__name__)

@lookup.route("/lookup/monster", methods=["POST"])
@validate_json_body(required_fields=["query"])
@validate_field("random", field_type=int, min_value=0, max_value=50, allow_none=True)
@validate_field("narrate", field_type=bool, allow_none=True)
def lookup_monster():
    """Lookup monsters endpoint"""
    data = g.request_data
    
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
    return handle_service_response(result)

@lookup.route("/lookup/monster/random", methods=["POST"])
@validate_field("count", field_type=int, min_value=1, max_value=20, allow_none=True)
@validate_field("narrate", field_type=bool, allow_none=True)
def lookup_random_monster():
    """Lookup random monsters endpoint"""
    data = g.request_data or {}
    
    count = data.get("count", 1)
    system = data.get("system", "").strip()
    environment = data.get("environment", "").strip()
    theme = data.get("theme", "").strip()
    context = data.get("context", "").strip()
    narrate = data.get("narrate", False)
    
    # Call service
    result = lookup_service.lookup_monsters(
        query="",
        system=system,
        environment=environment,
        random_count=count,
        narrate=narrate,
        context=context,
        theme=theme
    )
    return handle_service_response(result)

@lookup.route("/lookup/item", methods=["POST"])
@validate_json_body(required_fields=["query"])
@validate_field("random", field_type=int, min_value=0, max_value=50, allow_none=True)
@validate_field("narrate", field_type=bool, allow_none=True)
def lookup_item():
    """Lookup items endpoint"""
    data = g.request_data
    
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
    return handle_service_response(result)

@lookup.route("/lookup/item/random", methods=["POST"])
@validate_field("count", field_type=int, min_value=1, max_value=20, allow_none=True)
@validate_field("narrate", field_type=bool, allow_none=True)
def lookup_random_item():
    """Lookup random items endpoint"""
    data = g.request_data or {}
    
    count = data.get("count", 1)
    system = data.get("system", "").strip()
    category = data.get("category", "").strip()
    environment = data.get("environment", "").strip()
    quality = data.get("quality", "").strip()
    theme = data.get("theme", "").strip()
    context = data.get("context", "").strip()
    narrate = data.get("narrate", False)
    
    # Call service
    result = lookup_service.lookup_items(
        query="",
        system=system,
        category=category,
        random_count=count,
        narrate=narrate,
        context=context,
        environment=environment,
        quality=quality,
        theme=theme
    )
    return handle_service_response(result)

@lookup.route("/lookup/spell", methods=["POST"])
@validate_json_body(required_fields=["query"])
@validate_field("random", field_type=int, min_value=0, max_value=50, allow_none=True)
@validate_field("narrate", field_type=bool, allow_none=True)
def lookup_spell():
    """Lookup spells endpoint"""
    data = g.request_data
    
    query = data.get("query", "").strip()
    system = data.get("system", "").strip()
    tag = data.get("tag", "").strip()
    random_count = data.get("random", 0)
    context = data.get("context", "").strip()
    narrate = data.get("narrate", False)
    
    # Call service
    result = lookup_service.lookup_spells(
        query=query,
        system=system,
        tag=tag,
        random_count=random_count,
        narrate=narrate,
        context=context
    )
    return handle_service_response(result)

@lookup.route("/lookup/spell/random", methods=["POST"])
@validate_field("count", field_type=int, min_value=1, max_value=20, allow_none=True)
@validate_field("narrate", field_type=bool, allow_none=True)
def lookup_random_spell():
    """Lookup random spells endpoint"""
    data = g.request_data or {}
    
    count = data.get("count", 1)
    system = data.get("system", "").strip()
    context = data.get("context", "").strip()
    narrate = data.get("narrate", False)
    
    # Call service
    result = lookup_service.lookup_spells(
        query="",
        system=system,
        random_count=count,
        narrate=narrate,
        context=context
    )
    return handle_service_response(result)

@lookup.route("/lookup/rule", methods=["POST"])
@validate_json_body(required_fields=["query"])
def lookup_rule():
    """Lookup rules endpoint"""
    data = g.request_data
    
    query = data.get("query", "").strip()
    system = data.get("system", "").strip()
    tag = data.get("tag", "").strip()
    
    # Call service
    result = lookup_service.lookup_rules(query=query, system=system, tag=tag)
    return handle_service_response(result)

@lookup.route("/lookup/categories", methods=["GET"])
def list_lookup_categories():
    """List available lookup categories"""
    # Call service
    result = lookup_service.list_lookup_categories()
    return handle_service_response(result, "categories")

@lookup.route("/lookup/systems", methods=["GET"])
def list_lookup_systems():
    """List available lookup systems"""
    # Call service
    result = lookup_service.list_lookup_systems()
    return handle_service_response(result, "systems")

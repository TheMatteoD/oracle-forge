"""
Route Utilities for Oracle Forge

This module provides common utilities and patterns for route handlers
to eliminate duplicate code and ensure consistency.
"""

import logging
from typing import Dict, Any, Optional, List
from flask import g, request
from .responses import APIResponse, handle_service_response

logger = logging.getLogger(__name__)


def extract_common_lookup_params(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract common parameters used across lookup endpoints
    
    Args:
        data: Request data dictionary
        
    Returns:
        Dictionary of extracted parameters
    """
    return {
        "query": data.get("query", "").strip(),
        "system": data.get("system", "").strip(),
        "tag": data.get("tag", "").strip(),
        "random_count": data.get("random", 0),
        "environment": data.get("environment", "").strip(),
        "theme": data.get("theme", "").strip(),
        "context": data.get("context", "").strip(),
        "narrate": data.get("narrate", False)
    }


def extract_item_lookup_params(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract parameters specific to item lookup endpoints
    
    Args:
        data: Request data dictionary
        
    Returns:
        Dictionary of extracted parameters
    """
    base_params = extract_common_lookup_params(data)
    base_params.update({
        "category": data.get("category", "").strip(),
        "subcategory": data.get("subcategory", "").strip(),
        "quality": data.get("quality", "").strip()
    })
    return base_params


def extract_oracle_params(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract parameters specific to oracle endpoints
    
    Args:
        data: Request data dictionary
        
    Returns:
        Dictionary of extracted parameters
    """
    return {
        "question": data.get("question", "").strip(),
        "odds": data.get("odds", "50/50"),
        "chaos": data.get("chaos", 5),
        "flavor": data.get("flavor", False)
    }


def extract_generator_params(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract parameters specific to generator endpoints
    
    Args:
        data: Request data dictionary
        
    Returns:
        Dictionary of extracted parameters
    """
    return {
        "category": data.get("category", "").strip(),
        "filename": data.get("file", "").strip(),
        "table_id": data.get("table_id", "").strip(),
        "parameters": data.get("parameters", {})
    }


def extract_flavor_params(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract parameters specific to flavor generation endpoints
    
    Args:
        data: Request data dictionary
        
    Returns:
        Dictionary of extracted parameters
    """
    return {
        "context": data.get("context", "").strip(),
        "data": data.get("data", {}),
        "category": data.get("category", "").strip(),
        "source": data.get("source", "").strip()
    }


def validate_entity_type(entity_type: str, allowed_types: List[str]) -> bool:
    """
    Validate entity type against allowed types
    
    Args:
        entity_type: Entity type to validate
        allowed_types: List of allowed entity types
        
    Returns:
        True if valid, False otherwise
    """
    return entity_type in allowed_types


def get_pagination_params() -> Dict[str, int]:
    """
    Extract pagination parameters from request
    
    Returns:
        Dictionary with page and page_size
    """
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("page_size", 10, type=int)
    
    # Ensure reasonable limits
    page = max(1, page)
    page_size = max(1, min(100, page_size))
    
    return {"page": page, "page_size": page_size}


def create_list_response(items: List[Any], total: Optional[int] = None, 
                        page: Optional[int] = None, page_size: Optional[int] = None) -> APIResponse:
    """
    Create a standardized list response with pagination
    
    Args:
        items: List of items
        total: Total number of items
        page: Current page number
        page_size: Items per page
        
    Returns:
        APIResponse with list data
    """
    response_data = {
        "items": items,
        "count": len(items)
    }
    
    if total is not None:
        response_data["total"] = total
        
    if page is not None and page_size is not None:
        response_data["pagination"] = {
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size if total else 0
        }
    
    return APIResponse.success(response_data)


def log_request_info(endpoint: str, data: Optional[Dict[str, Any]] = None) -> None:
    """
    Log request information for debugging
    
    Args:
        endpoint: Endpoint name
        data: Request data (optional)
    """
    logger.debug(f"Request: {request.method} {request.url} -> {endpoint}")
    if data:
        logger.debug(f"Request data: {data}")


def log_response_info(endpoint: str, status_code: int) -> None:
    """
    Log response information for debugging
    
    Args:
        endpoint: Endpoint name
        status_code: HTTP status code
    """
    logger.debug(f"Response: {endpoint} -> {status_code}")


# Common validation patterns
def validate_adventure_name(adventure_name: str) -> bool:
    """Validate adventure name format"""
    return bool(adventure_name and adventure_name.strip())


def validate_character_name(character_name: str) -> bool:
    """Validate character name format"""
    return bool(character_name and character_name.strip())


def validate_file_upload(file, allowed_extensions: List[str]) -> bool:
    """Validate file upload"""
    if not file or not file.filename:
        return False
    
    extension = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
    return extension in allowed_extensions


# Common error responses
def not_found_response(resource_type: str, resource_name: str) -> APIResponse:
    """Create a standardized not found response"""
    return APIResponse.not_found(f"{resource_type} '{resource_name}' not found")


def validation_error_response(field: str, message: str) -> APIResponse:
    """Create a standardized validation error response"""
    return APIResponse.bad_request(message, details={"field": field})


def unauthorized_response(message: str = "Unauthorized") -> APIResponse:
    """Create a standardized unauthorized response"""
    return APIResponse.unauthorized(message)


def forbidden_response(message: str = "Forbidden") -> APIResponse:
    """Create a standardized forbidden response"""
    return APIResponse.forbidden(message) 
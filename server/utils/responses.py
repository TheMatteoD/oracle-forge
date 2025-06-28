"""
API Response Utilities for Oracle Forge

This module provides standardized response formats, error handling,
and validation helpers for consistent API responses across all endpoints.
"""

from typing import Dict, Any, Optional, Union, List
from flask import jsonify, Response
import logging

logger = logging.getLogger(__name__)


class APIResponse:
    """Standardized API response class"""
    
    @staticmethod
    def success(data: Any = None, message: str = "Success", status_code: int = 200) -> Response:
        """
        Create a standardized success response
        
        Args:
            data: The response data
            message: Success message
            status_code: HTTP status code
            
        Returns:
            Flask Response object
        """
        response = {
            "success": True,
            "message": message,
            "data": data
        }
        return jsonify(response), status_code
    
    @staticmethod
    def error(message: str, status_code: int = 400, error_code: Optional[str] = None, 
              details: Optional[Dict[str, Any]] = None) -> Response:
        """
        Create a standardized error response
        
        Args:
            message: Error message
            status_code: HTTP status code
            error_code: Optional error code for client handling
            details: Optional additional error details
            
        Returns:
            Flask Response object
        """
        response = {
            "success": False,
            "error": {
                "message": message,
                "code": error_code,
                "status_code": status_code
            }
        }
        
        if details:
            response["error"]["details"] = details
            
        return jsonify(response), status_code
    
    @staticmethod
    def list_response(items: List[Any], total: Optional[int] = None, 
                     page: Optional[int] = None, page_size: Optional[int] = None) -> Response:
        """
        Create a standardized list response with pagination support
        
        Args:
            items: List of items
            total: Total number of items (for pagination)
            page: Current page number
            page_size: Items per page
            
        Returns:
            Flask Response object
        """
        response = {
            "success": True,
            "data": {
                "items": items,
                "count": len(items)
            }
        }
        
        if total is not None:
            response["data"]["total"] = total
            
        if page is not None and page_size is not None:
            response["data"]["pagination"] = {
                "page": page,
                "page_size": page_size,
                "total_pages": (total + page_size - 1) // page_size if total else 0
            }
            
        return jsonify(response), 200
    
    @staticmethod
    def created(data: Any = None, message: str = "Resource created successfully") -> Response:
        """Create a 201 Created response"""
        return APIResponse.success(data, message, 201)
    
    @staticmethod
    def no_content(message: str = "Resource deleted successfully") -> Response:
        """Create a 204 No Content response"""
        return APIResponse.success(None, message, 204)
    
    @staticmethod
    def not_found(message: str = "Resource not found", error_code: str = "NOT_FOUND") -> Response:
        """Create a 404 Not Found response"""
        return APIResponse.error(message, 404, error_code)
    
    @staticmethod
    def bad_request(message: str = "Bad request", error_code: str = "BAD_REQUEST", 
                   details: Optional[Dict[str, Any]] = None) -> Response:
        """Create a 400 Bad Request response"""
        return APIResponse.error(message, 400, error_code, details)
    
    @staticmethod
    def unauthorized(message: str = "Unauthorized", error_code: str = "UNAUTHORIZED") -> Response:
        """Create a 401 Unauthorized response"""
        return APIResponse.error(message, 401, error_code)
    
    @staticmethod
    def forbidden(message: str = "Forbidden", error_code: str = "FORBIDDEN") -> Response:
        """Create a 403 Forbidden response"""
        return APIResponse.error(message, 403, error_code)
    
    @staticmethod
    def internal_error(message: str = "Internal server error", error_code: str = "INTERNAL_ERROR") -> Response:
        """Create a 500 Internal Server Error response"""
        return APIResponse.error(message, 500, error_code)


class ValidationError(Exception):
    """Custom exception for validation errors"""
    
    def __init__(self, message: str, field: Optional[str] = None, error_code: str = "VALIDATION_ERROR"):
        self.message = message
        self.field = field
        self.error_code = error_code
        super().__init__(message)


def validate_required_fields(data: Dict[str, Any], required_fields: List[str], 
                           field_names: Optional[Dict[str, str]] = None) -> None:
    """
    Validate that required fields are present in request data
    
    Args:
        data: Request data dictionary
        required_fields: List of required field names
        field_names: Optional mapping of field names to display names
        
    Raises:
        ValidationError: If required fields are missing
    """
    if not data:
        raise ValidationError("Request body is required")
    
    missing_fields = []
    for field in required_fields:
        if field not in data or data[field] is None or (isinstance(data[field], str) and not data[field].strip()):
            display_name = field_names.get(field, field) if field_names else field
            missing_fields.append(display_name)
    
    if missing_fields:
        raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")


def validate_field_type(data: Dict[str, Any], field: str, expected_type: type, 
                       allow_none: bool = False) -> None:
    """
    Validate that a field has the expected type
    
    Args:
        data: Request data dictionary
        field: Field name to validate
        expected_type: Expected type
        allow_none: Whether None values are allowed
        
    Raises:
        ValidationError: If field has wrong type
    """
    if field not in data:
        return  # Field is optional
    
    value = data[field]
    
    if value is None and allow_none:
        return
    
    if not isinstance(value, expected_type):
        raise ValidationError(
            f"Field '{field}' must be of type {expected_type.__name__}",
            field=field
        )


def validate_enum_field(data: Dict[str, Any], field: str, allowed_values: List[Any], 
                       allow_none: bool = False) -> None:
    """
    Validate that a field has one of the allowed values
    
    Args:
        data: Request data dictionary
        field: Field name to validate
        allowed_values: List of allowed values
        allow_none: Whether None values are allowed
        
    Raises:
        ValidationError: If field has invalid value
    """
    if field not in data:
        return  # Field is optional
    
    value = data[field]
    
    if value is None and allow_none:
        return
    
    if value not in allowed_values:
        raise ValidationError(
            f"Field '{field}' must be one of: {', '.join(map(str, allowed_values))}",
            field=field
        )


def validate_range_field(data: Dict[str, Any], field: str, min_value: Optional[Union[int, float]] = None,
                        max_value: Optional[Union[int, float]] = None, allow_none: bool = False) -> None:
    """
    Validate that a numeric field is within the specified range
    
    Args:
        data: Request data dictionary
        field: Field name to validate
        min_value: Minimum allowed value
        max_value: Maximum allowed value
        allow_none: Whether None values are allowed
        
    Raises:
        ValidationError: If field is outside allowed range
    """
    if field not in data:
        return  # Field is optional
    
    value = data[field]
    
    if value is None and allow_none:
        return
    
    if not isinstance(value, (int, float)):
        raise ValidationError(f"Field '{field}' must be a number", field=field)
    
    if min_value is not None and value < min_value:
        raise ValidationError(f"Field '{field}' must be at least {min_value}", field=field)
    
    if max_value is not None and value > max_value:
        raise ValidationError(f"Field '{field}' must be at most {max_value}", field=field)


def validate_string_length(data: Dict[str, Any], field: str, min_length: Optional[int] = None,
                          max_length: Optional[int] = None, allow_empty: bool = True) -> None:
    """
    Validate string field length
    
    Args:
        data: Request data dictionary
        field: Field name to validate
        min_length: Minimum string length
        max_length: Maximum string length
        allow_empty: Whether empty strings are allowed
        
    Raises:
        ValidationError: If string length is invalid
    """
    if field not in data:
        return  # Field is optional
    
    value = data[field]
    
    if value is None:
        return
    
    if not isinstance(value, str):
        raise ValidationError(f"Field '{field}' must be a string", field=field)
    
    if not allow_empty and not value.strip():
        raise ValidationError(f"Field '{field}' cannot be empty", field=field)
    
    if min_length is not None and len(value) < min_length:
        raise ValidationError(f"Field '{field}' must be at least {min_length} characters", field=field)
    
    if max_length is not None and len(value) > max_length:
        raise ValidationError(f"Field '{field}' must be at most {max_length} characters", field=field)


def handle_validation_error(error: ValidationError) -> Response:
    """
    Handle validation errors and return appropriate response
    
    Args:
        error: ValidationError instance
        
    Returns:
        Flask Response object
    """
    details = None
    if error.field:
        details = {"field": error.field}
    
    return APIResponse.bad_request(error.message, error.error_code, details)


def handle_service_response(service_result: Dict[str, Any], 
                          success_data_key: Optional[str] = None) -> Response:
    """
    Handle service layer responses and convert to standardized API response
    
    Args:
        service_result: Result from service layer
        success_data_key: Key to extract data from success response
        
    Returns:
        Flask Response object
    """
    if service_result.get("success"):
        data = service_result.get(success_data_key) if success_data_key else service_result
        return APIResponse.success(data)
    else:
        error_message = service_result.get("error", "Unknown error")
        return APIResponse.bad_request(error_message) 
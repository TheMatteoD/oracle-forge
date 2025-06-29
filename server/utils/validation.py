"""
Request Validation Utilities for Oracle Forge

This module provides decorators and utilities for standardizing request validation
across all API endpoints.
"""

import functools
import logging
from typing import Dict, Any, List, Optional, Union, Callable
from flask import request, g
from .responses import ValidationError, validate_required_fields, validate_field_type, \
                      validate_enum_field, validate_range_field, validate_string_length

logger = logging.getLogger(__name__)


def validate_json_body(required_fields: Optional[List[str]] = None,
                      field_names: Optional[Dict[str, str]] = None):
    """
    Decorator to validate JSON request body
    
    Args:
        required_fields: List of required field names
        field_names: Optional mapping of field names to display names
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                data = request.get_json()
                if required_fields:
                    validate_required_fields(data, required_fields, field_names)
                g.request_data = data
                return func(*args, **kwargs)
            except ValidationError as e:
                raise e
            except Exception as e:
                raise ValidationError(f"Invalid JSON format: {str(e)}")
        return wrapper
    return decorator


def validate_query_params(required_params: Optional[List[str]] = None,
                         param_names: Optional[Dict[str, str]] = None):
    """
    Decorator to validate query parameters
    
    Args:
        required_params: List of required parameter names
        param_names: Optional mapping of parameter names to display names
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                params = dict(request.args)
                if required_params:
                    validate_required_fields(params, required_params, param_names)
                g.query_params = params
                return func(*args, **kwargs)
            except ValidationError as e:
                raise e
        return wrapper
    return decorator


def validate_path_params(required_params: Optional[List[str]] = None,
                        param_names: Optional[Dict[str, str]] = None):
    """
    Decorator to validate path parameters
    
    Args:
        required_params: List of required parameter names
        param_names: Optional mapping of parameter names to display names
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                params = kwargs
                if required_params:
                    validate_required_fields(params, required_params, param_names)
                g.path_params = params
                return func(*args, **kwargs)
            except ValidationError as e:
                raise e
        return wrapper
    return decorator


def validate_field(field_name: str, field_type: Optional[type] = None,
                  required: bool = False, allow_none: bool = False,
                  allowed_values: Optional[List[Any]] = None,
                  min_value: Optional[Union[int, float]] = None,
                  max_value: Optional[Union[int, float]] = None,
                  min_length: Optional[int] = None,
                  max_length: Optional[int] = None,
                  allow_empty: bool = True):
    """
    Decorator to validate a specific field in the request
    
    Args:
        field_name: Name of the field to validate
        field_type: Expected type of the field
        required: Whether the field is required
        allow_none: Whether None values are allowed
        allowed_values: List of allowed values (for enum validation)
        min_value: Minimum value (for numeric fields)
        max_value: Maximum value (for numeric fields)
        min_length: Minimum length (for string fields)
        max_length: Maximum length (for string fields)
        allow_empty: Whether empty strings are allowed
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            
            if field_name in kwargs:
                value = kwargs[field_name]
                if allowed_values:
                    if not (allow_none and value is None) and value not in allowed_values:
                        raise ValidationError(
                            f"Invalid {field_name!r}: must be one of {list(allowed_values)}",
                            field=field_name
                        )

                return func(*args, **kwargs)


            try:
                data = getattr(g, 'request_data', request.get_json() or {})
                
                if required and field_name not in data:
                    raise ValidationError(f"Field '{field_name}' is required", field=field_name)
                
                if field_name in data:
                    value = data[field_name]
                    
                    # Type validation
                    if field_type and value is not None:
                        validate_field_type(data, field_name, field_type, allow_none)
                    
                    # Enum validation
                    if allowed_values and value is not None:
                        validate_enum_field(data, field_name, allowed_values, allow_none)
                    
                    # Range validation
                    if (min_value is not None or max_value is not None) and value is not None:
                        validate_range_field(data, field_name, min_value, max_value, allow_none)
                    
                    # String length validation
                    if (min_length is not None or max_length is not None) and value is not None:
                        validate_string_length(data, field_name, min_length, max_length, allow_empty)
                
                return func(*args, **kwargs)
            except ValidationError as e:
                raise e
        return wrapper
    return decorator


def validate_pagination(page_param: str = "page", page_size_param: str = "page_size",
                       max_page_size: int = 100):
    """
    Decorator to validate pagination parameters
    
    Args:
        page_param: Name of the page parameter
        page_size_param: Name of the page size parameter
        max_page_size: Maximum allowed page size
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                params = dict(request.args)
                
                # Validate page parameter
                if page_param in params:
                    try:
                        page = int(params[page_param])
                        if page < 1:
                            raise ValidationError(f"Page must be at least 1", field=page_param)
                    except ValueError:
                        raise ValidationError(f"Page must be a number", field=page_param)
                
                # Validate page size parameter
                if page_size_param in params:
                    try:
                        page_size = int(params[page_size_param])
                        if page_size < 1:
                            raise ValidationError(f"Page size must be at least 1", field=page_size_param)
                        if page_size > max_page_size:
                            raise ValidationError(f"Page size cannot exceed {max_page_size}", field=page_size_param)
                    except ValueError:
                        raise ValidationError(f"Page size must be a number", field=page_size_param)
                
                return func(*args, **kwargs)
            except ValidationError as e:
                raise e
        return wrapper
    return decorator


def validate_file_upload(allowed_extensions: Optional[List[str]] = None,
                        max_size: Optional[int] = None,
                        required: bool = False):
    """
    Decorator to validate file uploads
    
    Args:
        allowed_extensions: List of allowed file extensions
        max_size: Maximum file size in bytes
        required: Whether a file is required
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                if 'file' not in request.files:
                    if required:
                        raise ValidationError("File upload is required")
                    return func(*args, **kwargs)
                
                file = request.files['file']
                
                if file.filename == '':
                    if required:
                        raise ValidationError("No file selected")
                    return func(*args, **kwargs)
                
                # Validate file extension
                if allowed_extensions:
                    if not file.filename or '.' not in file.filename:
                        raise ValidationError("Invalid file format")
                    
                    extension = file.filename.rsplit('.', 1)[1].lower()
                    if extension not in allowed_extensions:
                        raise ValidationError(f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}")
                
                # Validate file size
                if max_size:
                    file.seek(0, 2)  # Seek to end
                    file_size = file.tell()
                    file.seek(0)  # Reset to beginning
                    
                    if file_size > max_size:
                        raise ValidationError(f"File size exceeds maximum allowed size of {max_size} bytes")
                
                return func(*args, **kwargs)
            except ValidationError as e:
                raise e
        return wrapper
    return decorator


# Common validation patterns
def validate_oracle_request():
    """Decorator for oracle request validation"""
    return validate_json_body(
        required_fields=["question"],
        field_names={"question": "Question"}
    )


def validate_lookup_request():
    """Decorator for lookup request validation"""
    return validate_json_body(
        required_fields=["query"],
        field_names={"query": "Query"}
    )


def validate_generator_request():
    """Decorator for generator request validation"""
    return validate_json_body(
        required_fields=["category", "file", "table_id"],
        field_names={
            "category": "Category",
            "file": "File",
            "table_id": "Table ID"
        }
    )


def validate_adventure_request():
    """Decorator for adventure request validation"""
    return validate_json_body(
        required_fields=["adventure_name"],
        field_names={"adventure_name": "Adventure name"}
    ) 
"""
Error Handling Middleware for Oracle Forge

This module provides centralized error handling for all API endpoints,
including validation errors, service errors, and unexpected system errors.
"""

import logging
from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException, BadRequest, NotFound, MethodNotAllowed
from ..utils.responses import APIResponse, ValidationError, handle_validation_error

logger = logging.getLogger(__name__)


def register_error_handlers(app: Flask) -> None:
    """
    Register error handlers for the Flask application
    
    Args:
        app: Flask application instance
    """
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(error: ValidationError):
        """Handle validation errors"""
        logger.warning(f"Validation error: {error.message} (field: {error.field})")
        return handle_validation_error(error)
    
    @app.errorhandler(BadRequest)
    def handle_bad_request(error: BadRequest):
        """Handle bad request errors"""
        logger.warning(f"Bad request: {error.description}")
        return APIResponse.bad_request(
            message="Invalid request format",
            error_code="BAD_REQUEST",
            details={"description": error.description}
        )
    
    @app.errorhandler(NotFound)
    def handle_not_found(error: NotFound):
        """Handle not found errors"""
        logger.info(f"Not found: {request.url}")
        return APIResponse.not_found(
            message="Endpoint not found",
            error_code="ENDPOINT_NOT_FOUND"
        )
    
    @app.errorhandler(MethodNotAllowed)
    def handle_method_not_allowed(error: MethodNotAllowed):
        """Handle method not allowed errors"""
        logger.warning(f"Method not allowed: {request.method} {request.url}")
        return APIResponse.error(
            message=f"Method {request.method} not allowed",
            status_code=405,
            error_code="METHOD_NOT_ALLOWED"
        )
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(error: HTTPException):
        """Handle HTTP exceptions"""
        logger.error(f"HTTP error {error.code}: {error.description}")
        return APIResponse.error(
            message=error.description,
            status_code=error.code,
            error_code=f"HTTP_{error.code}"
        )
    
    @app.errorhandler(Exception)
    def handle_unexpected_error(error: Exception):
        """Handle unexpected errors"""
        logger.error(f"Unexpected error: {str(error)}", exc_info=True)
        return APIResponse.internal_error(
            message="An unexpected error occurred",
            error_code="INTERNAL_ERROR"
        )


def log_request_info():
    """Log request information for debugging"""
    logger.debug(f"Request: {request.method} {request.url}")
    if request.json:
        logger.debug(f"Request body: {request.json}")


def log_response_info(response):
    """Log response information for debugging"""
    logger.debug(f"Response status: {response[1] if isinstance(response, tuple) else response.status_code}")
    return response 
"""
Rate Limiting Middleware for Oracle Forge

This module provides rate limiting functionality to protect the API
from abuse and ensure fair usage across all endpoints.
"""

import time
import logging
from typing import Dict, Tuple, Optional
from flask import Flask, request, g
from ..utils.responses import APIResponse

logger = logging.getLogger(__name__)


class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self):
        self.requests: Dict[str, list] = {}
        self.limits = {
            "default": {"requests": 100, "window": 60},  # 100 requests per minute
            "oracle": {"requests": 30, "window": 60},    # 30 oracle requests per minute
            "generator": {"requests": 20, "window": 60}, # 20 generator requests per minute
            "lookup": {"requests": 50, "window": 60},    # 50 lookup requests per minute
            "upload": {"requests": 10, "window": 60},    # 10 upload requests per minute
        }
    
    def _get_client_id(self) -> str:
        """Get client identifier (IP address)"""
        # In production, you might want to use a more sophisticated method
        # like API keys or user authentication
        return request.remote_addr or "unknown"
    
    def _get_limit_key(self, endpoint: str) -> str:
        """Get rate limit key based on endpoint"""
        if "oracle" in endpoint:
            return "oracle"
        elif "generator" in endpoint:
            return "generator"
        elif "lookup" in endpoint:
            return "lookup"
        elif "upload" in endpoint:
            return "upload"
        else:
            return "default"
    
    def _clean_old_requests(self, client_id: str, window: int) -> None:
        """Remove requests older than the window"""
        current_time = time.time()
        if client_id in self.requests:
            self.requests[client_id] = [
                req_time for req_time in self.requests[client_id]
                if current_time - req_time < window
            ]
    
    def check_rate_limit(self, endpoint: str) -> Tuple[bool, Optional[Dict]]:
        """
        Check if request is within rate limits
        
        Returns:
            Tuple of (allowed, rate_limit_info)
        """
        client_id = self._get_client_id()
        limit_key = self._get_limit_key(endpoint)
        limit_config = self.limits[limit_key]
        
        # Clean old requests
        self._clean_old_requests(client_id, limit_config["window"])
        
        # Initialize client requests if not exists
        if client_id not in self.requests:
            self.requests[client_id] = []
        
        # Check if limit exceeded
        if len(self.requests[client_id]) >= limit_config["requests"]:
            return False, {
                "limit": limit_config["requests"],
                "window": limit_config["window"],
                "remaining": 0,
                "reset_time": self.requests[client_id][0] + limit_config["window"]
            }
        
        # Add current request
        self.requests[client_id].append(time.time())
        
        # Return rate limit info
        remaining = limit_config["requests"] - len(self.requests[client_id])
        return True, {
            "limit": limit_config["requests"],
            "window": limit_config["window"],
            "remaining": remaining,
            "reset_time": time.time() + limit_config["window"]
        }


# Global rate limiter instance
rate_limiter = RateLimiter()


def rate_limit_middleware():
    """Rate limiting middleware function"""
    endpoint = request.endpoint or "unknown"
    
    # Skip rate limiting for certain endpoints and static/Azgaar files
    if endpoint in ["health", "config_status", "static"]:
        return
    if request.path.startswith("/azgaar/") or request.path.startswith("/static/"):
        return
    
    # Check rate limit
    allowed, rate_info = rate_limiter.check_rate_limit(endpoint)
    
    if not allowed:
        logger.warning(f"Rate limit exceeded for {request.remote_addr} on {endpoint}")
        return APIResponse.error(
            message="Rate limit exceeded",
            status_code=429,
            error_code="RATE_LIMIT_EXCEEDED",
            details=rate_info
        )
    
    # Add rate limit headers to response
    g.rate_limit_info = rate_info


def register_rate_limiting(app: Flask) -> None:
    """Register rate limiting middleware with Flask app"""
    app.before_request(rate_limit_middleware)
    
    @app.after_request
    def add_rate_limit_headers(response):
        """Add rate limit headers to response"""
        if hasattr(g, 'rate_limit_info'):
            rate_info = g.rate_limit_info
            response.headers['X-RateLimit-Limit'] = str(rate_info['limit'])
            response.headers['X-RateLimit-Remaining'] = str(rate_info['remaining'])
            response.headers['X-RateLimit-Reset'] = str(int(rate_info['reset_time']))
        return response 
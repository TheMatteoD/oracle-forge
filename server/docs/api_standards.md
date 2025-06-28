# Oracle Forge API Standards

## Overview

This document outlines the standardized patterns, response formats, error handling, and validation rules for the Oracle Forge API.

## Response Format

### Success Response

All successful API responses follow this format:

```json
{
  "success": true,
  "message": "Success message",
  "data": {
    // Response data here
  }
}
```

### Error Response

All error responses follow this format:

```json
{
  "success": false,
  "error": {
    "message": "Error description",
    "code": "ERROR_CODE",
    "status_code": 400,
    "details": {
      // Optional additional error details
    }
  }
}
```

### List Response

List responses include pagination information:

```json
{
  "success": true,
  "data": {
    "items": [...],
    "count": 10,
    "total": 100,
    "pagination": {
      "page": 1,
      "page_size": 10,
      "total_pages": 10
    }
  }
}
```

## HTTP Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `204 No Content` - Resource deleted successfully
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Access denied
- `404 Not Found` - Resource not found
- `405 Method Not Allowed` - HTTP method not supported
- `500 Internal Server Error` - Server error

## Error Codes

### Common Error Codes

- `VALIDATION_ERROR` - Request validation failed
- `BAD_REQUEST` - Invalid request format
- `NOT_FOUND` - Resource not found
- `UNAUTHORIZED` - Authentication required
- `FORBIDDEN` - Access denied
- `METHOD_NOT_ALLOWED` - HTTP method not supported
- `INTERNAL_ERROR` - Unexpected server error

### Domain-Specific Error Codes

- `ADVENTURE_NOT_FOUND` - Adventure not found
- `GENERATOR_NOT_FOUND` - Generator not found
- `TABLE_NOT_FOUND` - Table not found
- `CHARACTER_NOT_FOUND` - Character not found
- `MONSTER_NOT_FOUND` - Monster not found
- `ITEM_NOT_FOUND` - Item not found
- `SPELL_NOT_FOUND` - Spell not found

## Request Validation

### JSON Body Validation

Use the `@validate_json_body` decorator for endpoints that require JSON data:

```python
@route.route("/endpoint", methods=["POST"])
@validate_json_body(required_fields=["field1", "field2"])
def endpoint():
    data = g.request_data  # Access validated data
    # Process request
```

### Query Parameter Validation

Use the `@validate_query_params` decorator for endpoints with query parameters:

```python
@route.route("/endpoint", methods=["GET"])
@validate_query_params(required_params=["param1"])
def endpoint():
    params = g.query_params  # Access validated parameters
    # Process request
```

### Field Validation

Use the `@validate_field` decorator for specific field validation:

```python
@route.route("/endpoint", methods=["POST"])
@validate_field("age", field_type=int, min_value=0, max_value=120)
@validate_field("name", field_type=str, min_length=1, max_length=50)
def endpoint():
    # Process request
```

### Common Validation Patterns

#### Oracle Request
```python
@validate_oracle_request()
def oracle_endpoint():
    # Validates required "question" field
```

#### Lookup Request
```python
@validate_lookup_request()
def lookup_endpoint():
    # Validates required "query" field
```

#### Generator Request
```python
@validate_generator_request()
def generator_endpoint():
    # Validates required "category", "file", "table_id" fields
```

## Route Patterns

### Standard CRUD Operations

#### List Resources
```
GET /{domain}/list
GET /{domain}/{category}/list
```

#### Get Resource
```
GET /{domain}/{resource_id}
GET /{domain}/{category}/{resource_id}
```

#### Create Resource
```
POST /{domain}
POST /{domain}/{category}
```

#### Update Resource
```
PUT /{domain}/{resource_id}
PUT /{domain}/{category}/{resource_id}
```

#### Delete Resource
```
DELETE /{domain}/{resource_id}
DELETE /{domain}/{category}/{resource_id}
```

### Domain-Specific Patterns

#### Adventure Domain
```
GET /adventures/list
POST /adventures/select/{adventure}
GET /adventures/active
POST /adventures/clear
GET /adventures/{adv}/world_state
POST /adventures/{adv}/world_state
GET /adventures/{adv}/world/{entity_type}
POST /adventures/{adv}/world/{entity_type}/{entity_name}
DELETE /adventures/{adv}/world/{entity_type}/{entity_name}
```

#### Oracle Domain
```
POST /oracle/yesno
POST /oracle/yesno/flavor
POST /oracle/scene
POST /oracle/meaning
POST /oracle/meaning/flavor
GET /oracle/meaning/tables
```

#### Lookup Domain
```
POST /lookup/monster
POST /lookup/item
POST /lookup/spell
POST /lookup/rule
```

#### Generator Domain
```
GET /generators/categories
GET /generators/{category}/files
GET /generators/{category}/{filename}/tables
POST /generators/roll
POST /generators/flavor
GET /generators/custom
POST /generators/custom/{category}/{system}/{generator_id}
```

#### Session Domain
```
GET /session/state
GET /session/log
POST /session/log
GET /session/character/{character_name}
POST /session/character/{character_name}
DELETE /session/character/{character_name}
POST /session/end
```

## Response Examples

### Success Examples

#### List Adventures
```json
{
  "success": true,
  "message": "Success",
  "data": [
    "adventure1",
    "adventure2",
    "adventure3"
  ]
}
```

#### Get Adventure
```json
{
  "success": true,
  "message": "Success",
  "data": {
    "name": "adventure1",
    "world_state": {...},
    "characters": [...]
  }
}
```

#### Create Adventure
```json
{
  "success": true,
  "message": "Adventure created successfully",
  "data": {
    "name": "new_adventure",
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

### Error Examples

#### Validation Error
```json
{
  "success": false,
  "error": {
    "message": "Missing required fields: question",
    "code": "VALIDATION_ERROR",
    "status_code": 400,
    "details": {
      "field": "question"
    }
  }
}
```

#### Not Found Error
```json
{
  "success": false,
  "error": {
    "message": "Adventure 'nonexistent' not found",
    "code": "ADVENTURE_NOT_FOUND",
    "status_code": 404
  }
}
```

#### Internal Error
```json
{
  "success": false,
  "error": {
    "message": "An unexpected error occurred",
    "code": "INTERNAL_ERROR",
    "status_code": 500
  }
}
```

## Best Practices

### 1. Use Standardized Response Format
Always use the `APIResponse` class for consistent responses.

### 2. Implement Proper Validation
Use validation decorators to ensure data integrity.

### 3. Handle Errors Gracefully
Let the error handling middleware catch and format errors.

### 4. Log Appropriately
Log errors and important events for debugging.

### 5. Use Descriptive Error Messages
Provide clear, actionable error messages.

### 6. Follow RESTful Conventions
Use appropriate HTTP methods and status codes.

### 7. Document Your Endpoints
Include clear documentation for all API endpoints.

## Migration Guide

### Updating Existing Endpoints

1. **Replace direct jsonify calls** with `APIResponse` methods
2. **Add validation decorators** where appropriate
3. **Remove manual error handling** - let middleware handle it
4. **Update response format** to match standards

### Example Migration

#### Before
```python
@route.route("/endpoint", methods=["POST"])
def endpoint():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Process data
        result = process_data(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
```

#### After
```python
@route.route("/endpoint", methods=["POST"])
@validate_json_body(required_fields=["field1"])
def endpoint():
    data = g.request_data
    result = process_data(data)
    return APIResponse.success(result)
``` 
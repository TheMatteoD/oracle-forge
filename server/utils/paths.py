"""
Path utilities for Oracle Forge

This module provides utilities for working with file paths using the
centralized configuration system.
"""

import os
from pathlib import Path
from typing import Optional, List
from ..config import get_config, get_database_path


def get_vault_path() -> str:
    """Get the vault root path"""
    return get_database_path('vault')


def get_vault_templates_path() -> str:
    """Get the vault templates root path"""
    return get_database_path('vault_templates')


def get_adventures_path() -> str:
    """Get the adventures directory path"""
    return get_database_path('adventures')


def get_templates_path() -> str:
    """Get the templates directory path"""
    return get_database_path('templates')


def get_tables_path() -> str:
    """Get the tables directory path"""
    return get_database_path('tables')


def get_lookup_path() -> str:
    """Get the lookup directory path"""
    return get_database_path('lookup')


def get_rules_path() -> str:
    """Get the rules directory path"""
    return get_database_path('rules')


def get_index_path() -> str:
    """Get the index directory path"""
    return get_database_path('index')


def get_adventure_path(adventure_name: str) -> str:
    """Get the path for a specific adventure"""
    return os.path.join(get_adventures_path(), adventure_name)


def get_adventure_file_path(adventure_name: str, filename: str) -> str:
    """Get the path for a specific file within an adventure"""
    return os.path.join(get_adventure_path(adventure_name), filename)


def get_template_path(template_name: str) -> str:
    """Get the path for a specific template"""
    return os.path.join(get_templates_path(), template_name)


def get_vault_template_path(template_path: str) -> str:
    """Get the path for a specific template in the vault_templates directory"""
    return os.path.join(get_vault_templates_path(), template_path)


def get_table_path(category: str, filename: str) -> str:
    """Get the path for a specific table file"""
    return os.path.join(get_tables_path(), category, filename)


def get_lookup_file_path(category: str, filename: str) -> str:
    """Get the path for a specific lookup file"""
    return os.path.join(get_lookup_path(), category, filename)


def ensure_directory_exists(path: str) -> None:
    """Ensure a directory exists, creating it if necessary"""
    Path(path).mkdir(parents=True, exist_ok=True)


def list_yaml_files(directory: str) -> List[str]:
    """List all YAML files in a directory"""
    if not os.path.exists(directory):
        return []
    
    return [
        f for f in os.listdir(directory) 
        if f.endswith('.yaml') and not f.startswith('_')
    ]


def list_directories(parent_path: str) -> List[str]:
    """List all directories in a parent path"""
    if not os.path.exists(parent_path):
        return []
    
    return [
        d for d in os.listdir(parent_path)
        if os.path.isdir(os.path.join(parent_path, d))
    ]


def safe_filename(filename: str) -> str:
    """Convert a string to a safe filename"""
    import re
    # Remove or replace unsafe characters
    safe = re.sub(r'[^\w\-_.]', '_', filename)
    # Ensure it doesn't start with a dot or dash
    safe = safe.lstrip('.-')
    return safe


def file_exists(path: str) -> bool:
    """Check if a file exists"""
    return os.path.isfile(path)


def directory_exists(path: str) -> bool:
    """Check if a directory exists"""
    return os.path.isdir(path)


def get_file_size(path: str) -> int:
    """Get the size of a file in bytes"""
    if file_exists(path):
        return os.path.getsize(path)
    return 0


def is_within_vault(path: str) -> bool:
    """Check if a path is within the vault directory"""
    vault_path = Path(get_vault_path()).resolve()
    try:
        file_path = Path(path).resolve()
        return vault_path in file_path.parents or file_path == vault_path
    except (ValueError, RuntimeError):
        return False 
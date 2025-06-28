"""
Base DataAccess class for Oracle Forge

This module provides the foundation for all data access operations,
including file I/O, error handling, template loading, and validation.
"""

import os
import yaml
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from abc import ABC, abstractmethod

from ..config import get_config
from ..utils.paths import (
    get_vault_templates_path,
    get_vault_template_path,
    ensure_directory_exists,
    safe_filename,
    file_exists,
    directory_exists,
    list_yaml_files,
    list_directories,
)

logger = logging.getLogger(__name__)


class DataAccessError(Exception):
    """Base exception for data access operations"""
    pass


class TemplateNotFoundError(DataAccessError):
    """Raised when a template file is not found"""
    pass


class ValidationError(DataAccessError):
    """Raised when data validation fails"""
    pass


class BaseDataAccess(ABC):
    """Base class for all data access operations"""
    
    def __init__(self):
        self.config = get_config()
        self.templates_path = get_vault_templates_path()
    
    def _load_template(self, template_path: str) -> Dict[str, Any]:
        """Load a template from the template vault"""
        full_template_path = get_vault_template_path(template_path)
        
        if not file_exists(full_template_path):
            raise TemplateNotFoundError(f"Template not found: {template_path}")
        
        try:
            with open(full_template_path, 'r') as f:
                template = yaml.safe_load(f)
            return template or {}
        except Exception as e:
            raise DataAccessError(f"Failed to load template {template_path}: {e}")
    
    def _load_yaml(self, file_path: str) -> Dict[str, Any]:
        """Load a YAML file safely"""
        if not file_exists(file_path):
            return {}
        
        try:
            with open(file_path, 'r') as f:
                data = yaml.safe_load(f)
            return data or {}
        except Exception as e:
            raise DataAccessError(f"Failed to load YAML file {file_path}: {e}")
    
    def _save_yaml(self, file_path: str, data: Dict[str, Any]) -> None:
        """Save data to a YAML file safely"""
        try:
            # Ensure directory exists
            ensure_directory_exists(os.path.dirname(file_path))
            
            with open(file_path, 'w') as f:
                yaml.dump(data, f, default_flow_style=False, indent=2)
            
            logger.info(f"Saved data to {file_path}")
        except Exception as e:
            raise DataAccessError(f"Failed to save YAML file {file_path}: {e}")
    
    def _delete_file(self, file_path: str) -> bool:
        """Delete a file safely"""
        if not file_exists(file_path):
            return False
        
        try:
            os.remove(file_path)
            logger.info(f"Deleted file {file_path}")
            return True
        except Exception as e:
            raise DataAccessError(f"Failed to delete file {file_path}: {e}")
    
    def _list_files(self, directory: str, pattern: str = "*.yaml") -> List[str]:
        """List files in a directory"""
        if not directory_exists(directory):
            return []
        
        try:
            files = []
            for file in os.listdir(directory):
                if file.endswith('.yaml') and not file.startswith('_'):
                    files.append(file)
            return sorted(files)
        except Exception as e:
            raise DataAccessError(f"Failed to list files in {directory}: {e}")
    
    def _list_directories(self, parent_path: str) -> List[str]:
        """List directories in a parent path"""
        if not directory_exists(parent_path):
            return []
        
        try:
            return list_directories(parent_path)
        except Exception as e:
            raise DataAccessError(f"Failed to list directories in {parent_path}: {e}")
    
    def _validate_required_fields(self, data: Dict[str, Any], template: Dict[str, Any]) -> None:
        """Validate that required fields are present"""
        # For now, we'll use a simple validation approach
        # In the future, this could be enhanced with JSON Schema validation
        
        # Check for basic required fields that most templates have
        required_fields = ['id', 'name']
        
        for field in required_fields:
            if field in template and field not in data:
                raise ValidationError(f"Required field '{field}' is missing")
    
    def _merge_with_template(self, data: Dict[str, Any], template_path: str) -> Dict[str, Any]:
        """Merge data with template defaults"""
        template = self._load_template(template_path)
        
        # Create a deep copy of the template
        result = template.copy()
        
        # Override template values with provided data
        result.update(data)
        
        return result
    
    def _create_from_template(self, template_path: str, data: Dict[str, Any], 
                            target_path: str) -> Dict[str, Any]:
        """Create a new file from template with provided data"""
        # Merge data with template
        merged_data = self._merge_with_template(data, template_path)
        
        # Validate the merged data
        template = self._load_template(template_path)
        self._validate_required_fields(merged_data, template)
        
        # Save to target path
        self._save_yaml(target_path, merged_data)
        
        return merged_data
    
    def _safe_filename(self, filename: str) -> str:
        """Convert a string to a safe filename"""
        return safe_filename(filename)
    
    def _ensure_directory(self, path: str) -> None:
        """Ensure a directory exists"""
        ensure_directory_exists(path)
    
    @abstractmethod
    def get_domain_name(self) -> str:
        """Return the domain name for this data access class"""
        pass
    
    def log_operation(self, operation: str, details: str) -> None:
        """Log an operation for debugging"""
        logger.info(f"[{self.get_domain_name()}] {operation}: {details}") 
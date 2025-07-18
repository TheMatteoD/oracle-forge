"""
Table DataAccess class for Oracle Forge

This module provides data access operations for tables including:
- Oracle tables (event focus, character descriptors, etc.)
- Generator tables (dungeon generators, etc.)
- Table management and validation
"""

import os
from typing import Dict, List, Optional, Any
from pathlib import Path

from .base_data import BaseDataAccess, DataAccessError, ValidationError
from ..utils.paths import (
    get_tables_path,
)


class TableDataAccess(BaseDataAccess):
    """Data access class for table-related operations"""
    
    def get_domain_name(self) -> str:
        return "Tables"
    
    # Oracle Table Management
    def _get_oracle_path(self) -> str:
        """Get the path for oracle tables"""
        return os.path.join(get_tables_path(), "oracle")
    
    def _get_oracle_template_path(self, table_type: str) -> str:
        """Get the template path for an oracle table type"""
        return f"tables/oracle/{table_type}_template.yaml"
    
    def list_oracle_tables(self) -> List[str]:
        """List all available oracle tables"""
        oracle_path = self._get_oracle_path()
        return self._list_files(oracle_path)
    
    def get_oracle_table(self, table_name: str) -> Dict[str, Any]:
        """Get a specific oracle table"""
        table_path = os.path.join(self._get_oracle_path(), table_name)
        data = self._load_yaml(table_path)
        if not isinstance(data, dict):
            raise DataAccessError(f"Oracle table '{table_name}' is not a dict (type: {type(data).__name__})")
        return data
    
    def update_oracle_table(self, table_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a specific oracle table"""
        table_path = os.path.join(self._get_oracle_path(), table_name)
        self._save_yaml(table_path, data)
        self.log_operation("update_oracle_table", f"Updated {table_name}")
        return data
    
    def create_oracle_table(self, table_name: str, table_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new oracle table"""
        # Generate safe filename
        safe_filename = self._safe_filename(table_name) + '.yaml'
        
        # Create table file from template
        table_path = os.path.join(self._get_oracle_path(), safe_filename)
        table_data = self._create_from_template(
            "tables/oracle/oracle_table_template.yaml",
            table_data,
            table_path
        )
        
        self.log_operation("create_oracle_table", f"Created oracle table {table_name}")
        return table_data
    
    def delete_oracle_table(self, table_name: str) -> bool:
        """Delete a specific oracle table"""
        table_path = os.path.join(self._get_oracle_path(), table_name)
        return self._delete_file(table_path)
    
    def search_oracle_tables(self, query: str, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search for oracle tables"""
        results = []
        tables = self.list_oracle_tables()
        
        for table_file in tables:
            table_data = self.get_oracle_table(table_file)
            
            # Apply category filter
            if category and category.lower() not in table_data.get('category', '').lower():
                continue
            
            # Search in name, description, and content
            searchable_text = f"{table_data.get('name', '')} {table_data.get('description', '')}".lower()
            if query.lower() in searchable_text:
                table_data['filename'] = table_file  # Add filename info
                results.append(table_data)
        
        return results
    
    def roll_oracle_table(self, table_name: str, roll: Optional[int] = None) -> Dict[str, Any]:
        """Roll on an oracle table and return the result"""
        table_data = self.get_oracle_table(table_name)
        
        if not table_data:
            raise DataAccessError(f"Oracle table '{table_name}' not found")
        
        # Get the table entries
        entries = table_data.get('entries', [])
        if not entries:
            raise DataAccessError(f"Oracle table '{table_name}' has no entries")
        
        # Generate random roll if not provided
        if roll is None:
            import random
            # Determine roll range from entries
            min_roll = 1
            max_roll = len(entries)
            roll = random.randint(min_roll, max_roll)
        
        # Find the entry for this roll
        for entry in entries:
            # Handle both old 'roll' format and new 'range' format
            if 'roll' in entry and entry.get('roll') == roll:
                return {
                    'table': table_name,
                    'roll': roll,
                    'result': entry.get('result', ''),
                    'description': entry.get('description', ''),
                    'table_data': table_data
                }
            elif 'range' in entry:
                # Handle range format [min, max] or single number
                range_val = entry['range']
                if isinstance(range_val, list) and len(range_val) == 2:
                    min_range, max_range = range_val
                    if min_range <= roll <= max_range:
                        return {
                            'table': table_name,
                            'roll': roll,
                            'result': entry.get('result', ''),
                            'description': entry.get('description', ''),
                            'table_data': table_data
                        }
                elif isinstance(range_val, int) and range_val == roll:
                    return {
                        'table': table_name,
                        'roll': roll,
                        'result': entry.get('result', ''),
                        'description': entry.get('description', ''),
                        'table_data': table_data
                    }
        
        raise DataAccessError(f"No entry found for roll {roll} in table '{table_name}'")
    
    # Generator Table Management
    def _get_generator_path(self, generator_type: str) -> str:
        """Get the path for a generator type"""
        return os.path.join(get_tables_path(), "generators", generator_type)
    
    def _get_generator_template_path(self, generator_type: str) -> str:
        """Get the template path for a generator type"""
        return f"tables/generators/{generator_type}/{generator_type}_template.yaml"
    
    def list_generator_types(self) -> List[str]:
        """List all available generator types"""
        generators_path = os.path.join(get_tables_path(), "generators")
        return self._list_directories(generators_path)
    
    def list_generators(self, generator_type: str) -> List[str]:
        """List all generators of a specific type"""
        generator_path = self._get_generator_path(generator_type)
        return self._list_files(generator_path)
    
    def get_generator(self, generator_type: str, generator_name: str) -> Dict[str, Any]:
        """Get a specific generator"""
        generator_path = os.path.join(self._get_generator_path(generator_type), generator_name)
        return self._load_yaml(generator_path)
    
    def update_generator(self, generator_type: str, generator_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a specific generator"""
        generator_path = os.path.join(self._get_generator_path(generator_type), generator_name)
        self._save_yaml(generator_path, data)
        self.log_operation("update_generator", f"Updated {generator_type} generator {generator_name}")
        return data
    
    def create_generator(self, generator_type: str, generator_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new generator"""
        # Generate safe filename from generator name
        generator_name = generator_data.get('name', 'unknown')
        safe_filename = self._safe_filename(generator_name) + '.yaml'
        
        # Create generator file from template
        generator_path = os.path.join(self._get_generator_path(generator_type), safe_filename)
        generator_data = self._create_from_template(
            self._get_generator_template_path(generator_type),
            generator_data,
            generator_path
        )
        
        self.log_operation("create_generator", f"Created {generator_type} generator {generator_name}")
        return generator_data
    
    def delete_generator(self, generator_type: str, generator_name: str) -> bool:
        """Delete a specific generator"""
        generator_path = os.path.join(self._get_generator_path(generator_type), generator_name)
        return self._delete_file(generator_path)
    
    def search_generators(self, query: str, generator_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search for generators"""
        results = []
        
        generator_types = [generator_type] if generator_type else self.list_generator_types()
        
        for gen_type in generator_types:
            generators = self.list_generators(gen_type)
            for gen_file in generators:
                gen_data = self.get_generator(gen_type, gen_file)
                
                # Search in name and description
                searchable_text = f"{gen_data.get('name', '')} {gen_data.get('description', '')}".lower()
                if query.lower() in searchable_text:
                    gen_data['type'] = gen_type  # Add type info
                    gen_data['filename'] = gen_file  # Add filename info
                    results.append(gen_data)
        
        return results
    
    def execute_generator(self, generator_type: str, generator_name: str, 
                         parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a generator with given parameters"""
        generator_data = self.get_generator(generator_type, generator_name)
        
        if not generator_data:
            raise DataAccessError(f"Generator '{generator_name}' of type '{generator_type}' not found")
        
        # For now, return the generator data with parameters
        # In the future, this could integrate with actual generation logic
        return {
            'generator_type': generator_type,
            'generator_name': generator_name,
            'parameters': parameters or {},
            'generator_data': generator_data,
            'result': f"Generated {generator_type} using {generator_name}"
        }
    
    # Convenience methods for specific generator types
    def create_dungeon_generator(self, generator_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new dungeon generator"""
        return self.create_generator("dungeons", generator_data)
    
    def list_dungeon_generators(self) -> List[str]:
        """List all dungeon generators"""
        return self.list_generators("dungeons")
    
    def get_dungeon_generator(self, generator_name: str) -> Dict[str, Any]:
        """Get a specific dungeon generator"""
        return self.get_generator("dungeons", generator_name)
    
    def execute_dungeon_generator(self, generator_name: str, 
                                parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a dungeon generator"""
        return self.execute_generator("dungeons", generator_name, parameters)
    
    # Table Validation and Management
    def validate_table_structure(self, table_data: Dict[str, Any]) -> bool:
        """Validate that a table has the required structure"""
        required_fields = ['name', 'description', 'entries']
        
        for field in required_fields:
            if field not in table_data:
                raise ValidationError(f"Required field '{field}' is missing from table")
        
        # Validate entries structure
        entries = table_data.get('entries', [])
        if not isinstance(entries, list):
            raise ValidationError("Table entries must be a list")
        
        for entry in entries:
            if not isinstance(entry, dict):
                raise ValidationError("Each table entry must be a dictionary")
            
            if 'roll' not in entry or 'result' not in entry:
                raise ValidationError("Each table entry must have 'roll' and 'result' fields")
        
        return True
    
    def get_table_statistics(self, table_name: str) -> Dict[str, Any]:
        """Get statistics about a table"""
        table_data = self.get_oracle_table(table_name)
        
        if not table_data:
            raise DataAccessError(f"Table '{table_name}' not found")
        
        entries = table_data.get('entries', [])
        
        # Calculate statistics
        total_entries = len(entries)
        roll_range = None
        if entries:
            rolls = [entry.get('roll', 0) for entry in entries]
            roll_range = (min(rolls), max(rolls))
        
        return {
            'table_name': table_name,
            'total_entries': total_entries,
            'roll_range': roll_range,
            'categories': table_data.get('categories', []),
            'tags': table_data.get('tags', [])
        }
    
    def export_table(self, table_name: str, format: str = "yaml") -> str:
        """Export a table in the specified format"""
        table_data = self.get_oracle_table(table_name)
        
        if format.lower() == "yaml":
            import yaml
            return yaml.dump(table_data, default_flow_style=False, indent=2)
        elif format.lower() == "json":
            import json
            return json.dumps(table_data, indent=2)
        else:
            raise DataAccessError(f"Unsupported export format: {format}")
    
    def import_table(self, table_name: str, table_data: Dict[str, Any], 
                    overwrite: bool = False) -> Dict[str, Any]:
        """Import a table from data"""
        # Validate the table structure
        self.validate_table_structure(table_data)
        
        # Check if table already exists
        if not overwrite and table_name in self.list_oracle_tables():
            raise DataAccessError(f"Table '{table_name}' already exists. Use overwrite=True to replace it.")
        
        # Save the table
        return self.update_oracle_table(table_name, table_data) 
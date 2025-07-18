"""
Generator Service for Oracle Forge

This module provides business logic for generator operations including:
- Table-based generators (dungeons, etc.)
- Custom generators (programmatic generators)
- Generator flavoring and narration
- Generator execution and result processing
"""

import importlib
import logging
from typing import Dict, List, Optional, Any
from scripts.generators.registry import CUSTOM_GENERATORS
from scripts.llm.flavoring import narrate_generation

from ..data_access.tables import TableDataAccess, DataAccessError

logger = logging.getLogger(__name__)


class GeneratorService:
    """Service class for generator operations"""
    
    def __init__(self):
        self.table_data_access = TableDataAccess()
        self.logger = logger
    
    def get_domain_name(self) -> str:
        return "Generators"
    
    # Generator Type Management
    def list_generator_types(self) -> List[str]:
        """List all available generator types (dungeons, etc.)"""
        try:
            return self.table_data_access.list_generator_types()
        except DataAccessError as e:
            self.logger.error(f"Failed to list generator types: {e}")
            return []
    
    def list_generators(self, generator_type: str) -> List[str]:
        """List all generators of a specific type"""
        try:
            return self.table_data_access.list_generators(generator_type)
        except DataAccessError as e:
            self.logger.error(f"Failed to list {generator_type} generators: {e}")
            return []
    
    def get_generator(self, generator_type: str, generator_name: str) -> Dict[str, Any]:
        """Get a specific generator"""
        try:
            return self.table_data_access.get_generator(generator_type, generator_name)
        except DataAccessError as e:
            self.logger.error(f"Failed to get generator {generator_type}/{generator_name}: {e}")
            return {}
    
    def create_generator(self, generator_type: str, generator_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new generator"""
        try:
            result = self.table_data_access.create_generator(generator_type, generator_data)
            self.logger.info(f"Created generator {generator_type}/{generator_data.get('name', 'unknown')}")
            return {
                "success": True,
                "generator": result,
                "message": f"Generator created successfully"
            }
        except DataAccessError as e:
            self.logger.error(f"Failed to create {generator_type} generator: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def update_generator(self, generator_type: str, generator_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a specific generator"""
        try:
            result = self.table_data_access.update_generator(generator_type, generator_name, data)
            self.logger.info(f"Updated generator {generator_type}/{generator_name}")
            return {
                "success": True,
                "generator": result,
                "message": f"Generator updated successfully"
            }
        except DataAccessError as e:
            self.logger.error(f"Failed to update generator {generator_type}/{generator_name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def delete_generator(self, generator_type: str, generator_name: str) -> Dict[str, Any]:
        """Delete a specific generator"""
        try:
            success = self.table_data_access.delete_generator(generator_type, generator_name)
            if success:
                self.logger.info(f"Deleted generator {generator_type}/{generator_name}")
                return {
                    "success": True,
                    "message": f"Generator '{generator_name}' deleted successfully"
                }
            else:
                return {
                    "success": False,
                    "error": f"Generator '{generator_name}' not found"
                }
        except DataAccessError as e:
            self.logger.error(f"Failed to delete generator {generator_type}/{generator_name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def search_generators(self, query: str, generator_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search for generators"""
        try:
            return self.table_data_access.search_generators(query, generator_type)
        except DataAccessError as e:
            self.logger.error(f"Failed to search generators: {e}")
            return []
    
    # Generator Execution
    def execute_generator(self, generator_type: str, generator_name: str, 
                         parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a table-based generator"""
        try:
            result = self.table_data_access.execute_generator(generator_type, generator_name, parameters)
            return {
                "success": True,
                "result": result,
                "generator": generator_name,
                "type": generator_type
            }
        except DataAccessError as e:
            self.logger.error(f"Failed to execute generator {generator_type}/{generator_name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def roll_table(self, generator_type: str, generator_name: str, table_id: str) -> Dict[str, Any]:
        """Roll on a specific table within a generator"""
        try:
            generator_data = self.get_generator(generator_type, generator_name)
            if not generator_data:
                return {
                    "success": False,
                    "error": f"Generator '{generator_name}' not found"
                }
            
            # Find the table by ID
            tables = generator_data.get('tables', [])
            target_table = None
            for table in tables:
                if table.get('id') == table_id:
                    target_table = table
                    break
            
            if not target_table:
                return {
                    "success": False,
                    "error": f"Table with ID '{table_id}' not found in generator {generator_name}"
                }
            
            # Execute the table roll
            result = self.table_data_access.roll_on_table(target_table)
            
            return {
                "success": True,
                "generator": generator_name,
                "table_id": table_id,
                "table_label": target_table.get('label', ''),
                "result": result
            }
        except DataAccessError as e:
            self.logger.error(f"Failed to roll on table {table_id} in generator {generator_type}/{generator_name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    # Custom Generators
    def list_custom_generators(self) -> Dict[str, Any]:
        """List all available custom generators"""
        try:
            output = {}
            for category, systems in CUSTOM_GENERATORS.items():
                output[category] = {}
                for system_name, system_data in systems.items():
                    output[category][system_name] = {
                        "label": system_data["label"],
                        "generators": [
                            {"id": gen_id, "label": gen_data["label"]}
                            for gen_id, gen_data in system_data["generators"].items()
                        ]
                    }
            return output
        except Exception as e:
            self.logger.error(f"Failed to list custom generators: {e}")
            return {}
    
    def execute_custom_generator(self, category: str, system: str, generator_id: str, 
                               parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a custom generator"""
        try:
            # Validate the generator exists
            if category not in CUSTOM_GENERATORS:
                return {
                    "success": False,
                    "error": f"Custom generator category '{category}' not found"
                }
            
            if system not in CUSTOM_GENERATORS[category]:
                return {
                    "success": False,
                    "error": f"Custom generator system '{system}' not found in category '{category}'"
                }
            
            if generator_id not in CUSTOM_GENERATORS[category][system]["generators"]:
                return {
                    "success": False,
                    "error": f"Custom generator '{generator_id}' not found in system '{system}'"
                }
            
            # Get the generator function
            system_data = CUSTOM_GENERATORS[category][system]
            gen_entry = system_data["generators"][generator_id]
            module_path, func_name = gen_entry["function"].rsplit(".", 1)
            
            # Import and execute the function
            module = importlib.import_module(module_path)
            func = getattr(module, func_name)
            
            # Execute with parameters if provided
            if parameters:
                result = func(**parameters)
            else:
                result = func()
            
            return {
                "success": True,
                'category': category,
                'system': system,
                'generator_id': generator_id,
                'result': result
            }
        except ImportError as e:
            self.logger.error(f"Failed to import custom generator module: {e}")
            return {
                "success": False,
                "error": f"Custom generator module not found: {str(e)}"
            }
        except AttributeError as e:
            self.logger.error(f"Failed to find custom generator function: {e}")
            return {
                "success": False,
                "error": f"Custom generator function not found: {str(e)}"
            }
        except Exception as e:
            self.logger.error(f"Failed to execute custom generator {category}/{system}/{generator_id}: {e}")
            return {
                "success": False,
                "error": f"Failed to execute custom generator: {str(e)}"
            }
    
    # Generator Flavoring
    def generate_flavor(self, context: str = "", data: Dict[str, Any] = None, 
                       category: str = "", source: str = "") -> Dict[str, Any]:
        """Generate flavored narration for generator results"""
        try:
            if data is None:
                data = {}
            
            result = narrate_generation(
                context=context,
                data=data,
                category=category,
                source=source
            )
            return {
                "success": True,
                "narration": result
            }
        except Exception as e:
            self.logger.error(f"Failed to generate flavor: {e}")
            return {
                "success": False,
                "error": f"Failed to generate flavor: {str(e)}"
            }
    
    # Specialized Generator Methods
    def list_dungeon_generators(self) -> List[str]:
        """List all dungeon generators"""
        try:
            return self.table_data_access.list_dungeon_generators()
        except DataAccessError as e:
            self.logger.error(f"Failed to list dungeon generators: {e}")
            return []
    
    def get_dungeon_generator(self, generator_name: str) -> Dict[str, Any]:
        """Get a specific dungeon generator"""
        try:
            return self.table_data_access.get_dungeon_generator(generator_name)
        except DataAccessError as e:
            self.logger.error(f"Failed to get dungeon generator {generator_name}: {e}")
            return {}
    
    def execute_dungeon_generator(self, generator_name: str, 
                                parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a dungeon generator"""
        try:
            result = self.table_data_access.execute_dungeon_generator(generator_name, parameters)
            return {
                "success": True,
                "result": result,
                "generator": generator_name,
                "type": "dungeon"
            }
        except DataAccessError as e:
            self.logger.error(f"Failed to execute dungeon generator {generator_name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    # Utility Methods
    def get_generator_statistics(self, generator_type: str, generator_name: str) -> Dict[str, Any]:
        """Get statistics about a generator"""
        try:
            generator_data = self.get_generator(generator_type, generator_name)
            if not generator_data:
                return {
                    "success": False,
                    "error": f"Generator '{generator_name}' not found"
                }
            
            tables = generator_data.get('tables', [])
            
            stats = {
                'name': generator_data.get('name', ''),
                'source': generator_data.get('source', ''),
                'category': generator_data.get('category', ''),
                'table_count': len(tables),
                'tables': []
            }
            
            for table in tables:
                table_stats = {
                    'id': table.get('id', ''),
                    'label': table.get('label', ''),
                    'dice': table.get('dice', ''),
                    'entry_count': len(table.get('entries', []))
                }
                stats['tables'].append(table_stats)
            
            return {
                "success": True,
                "statistics": stats
            }
        except Exception as e:
            self.logger.error(f"Failed to get generator statistics for {generator_type}/{generator_name}: {e}")
            return {
                "success": False,
                "error": f"Failed to get generator statistics: {str(e)}"
            }
    
    def validate_generator(self, generator_type: str, generator_name: str) -> Dict[str, Any]:
        """Validate a generator's structure"""
        try:
            generator_data = self.get_generator(generator_type, generator_name)
            if not generator_data:
                return {
                    "success": False,
                    "error": f"Generator '{generator_name}' not found"
                }
            
            validation_result = self.table_data_access.validate_table_structure(generator_data)
            return {
                "success": True,
                "validation": validation_result
            }
        except DataAccessError as e:
            self.logger.error(f"Failed to validate generator {generator_type}/{generator_name}: {e}")
            return {
                "success": False,
                "error": str(e)
            } 
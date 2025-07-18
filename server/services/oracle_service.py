"""
Oracle Service for Oracle Forge

This service contains business logic for oracle operations including:
- Yes/No oracle queries
- Meaning oracle queries
- Scene tests
- Oracle table management
- Narration generation
"""

import logging
from typing import Dict, List, Optional, Any

from ..data_access import TableDataAccess, DataAccessError
from scripts.oracle.oracle_driver import (
    handle_yes_no,
    handle_meaning,
    handle_scene_test,
    handle_yesno_flavor,
    handle_meaning_flavor,
    handle_scene_flavor
)

logger = logging.getLogger(__name__)


class OracleService:
    """Service class for oracle-related business logic"""
    
    def __init__(self):
        self.data_access = TableDataAccess()
    
    # Yes/No Oracle
    def yes_no_query(self, question: str, odds: str = "50/50", chaos: int = 5) -> Dict[str, Any]:
        """Handle a yes/no oracle query"""
        try:
            result = handle_yes_no(question=question, odds=odds, chaos=chaos)
            
            logger.info(f"Yes/No oracle query: '{question}' -> {result.get('result', 'unknown')}")
            return {
                "success": True,
                "question": question,
                "odds": odds,
                "chaos": chaos,
                "result": result
            }
        except Exception as e:
            logger.error(f"Failed to process yes/no oracle query: {e}")
            return {
                "success": False,
                "error": str(e),
                "question": question,
                "odds": odds,
                "chaos": chaos
            }
    
    def yes_no_narration(self, question: str, outcome: str, event_trigger: str = "") -> Dict[str, Any]:
        """Generate narration for a yes/no oracle result"""
        try:
            narration = handle_yesno_flavor(
                question=question,
                outcome=outcome,
                event_trigger=event_trigger
            )
            
            return {
                "success": True,
                "question": question,
                "outcome": outcome,
                "event_trigger": event_trigger,
                "narration": narration
            }
        except Exception as e:
            logger.error(f"Failed to generate yes/no narration: {e}")
            return {
                "success": False,
                "error": str(e),
                "question": question,
                "outcome": outcome,
                "event_trigger": event_trigger
            }
    
    # Scene Test Oracle
    def scene_test(self, chaos: int = 5, flavor: bool = False) -> Dict[str, Any]:
        """Handle a scene test oracle query"""
        try:
            result = handle_scene_test(chaos=chaos, flavor=flavor)
            
            logger.info(f"Scene test oracle: chaos={chaos}, flavor={flavor} -> {result.get('result', 'unknown')}")
            return {
                "success": True,
                "chaos": chaos,
                "flavor": flavor,
                "result": result
            }
        except Exception as e:
            logger.error(f"Failed to process scene test oracle: {e}")
            return {
                "success": False,
                "error": str(e),
                "chaos": chaos,
                "flavor": flavor
            }
    
    def scene_narration(self, focus: str, expectation: str) -> Dict[str, Any]:
        """Generate narration for a scene test result"""
        try:
            narration = handle_scene_flavor(focus=focus, expectation=expectation)
            
            return {
                "success": True,
                "focus": focus,
                "expectation": expectation,
                "narration": narration
            }
        except Exception as e:
            logger.error(f"Failed to generate scene narration: {e}")
            return {
                "success": False,
                "error": str(e),
                "focus": focus,
                "expectation": expectation
            }
    
    # Meaning Oracle
    def meaning_query(self, question: str, table: str) -> Dict[str, Any]:
        """Handle a meaning oracle query"""
        try:
            result = handle_meaning(question=question, table=table)
            
            logger.info(f"Meaning oracle query: '{question}' using table '{table}' -> {result.get('result', 'unknown')}")
            return {
                "success": True,
                "question": question,
                "table": table,
                "result": result
            }
        except Exception as e:
            logger.error(f"Failed to process meaning oracle query: {e}")
            return {
                "success": False,
                "error": str(e),
                "question": question,
                "table": table
            }
    
    def meaning_narration(self, question: str, keywords: List[str]) -> Dict[str, Any]:
        """Generate narration for a meaning oracle result"""
        try:
            narration = handle_meaning_flavor(question=question, keywords=keywords)
            
            return {
                "success": True,
                "question": question,
                "keywords": keywords,
                "narration": narration
            }
        except Exception as e:
            logger.error(f"Failed to generate meaning narration: {e}")
            return {
                "success": False,
                "error": str(e),
                "question": question,
                "keywords": keywords
            }
    
    # Oracle Table Management
    def list_oracle_tables(self) -> Dict[str, Any]:
        """List all available oracle tables"""
        try:
            tables = self.data_access.list_oracle_tables()
            
            # Get metadata for each table
            table_info = []
            for table_file in tables:
                try:
                    table_data = self.data_access.get_oracle_table(table_file)
                    table_info.append({
                        "filename": table_file,
                        "name": table_data.get('name', table_file),
                        "description": table_data.get('description', ''),
                        "category": table_data.get('category', ''),
                        "entries": len(table_data.get('entries', []))
                    })
                except DataAccessError:
                    # Skip invalid tables
                    continue
            
            return {
                "success": True,
                "tables": table_info,
                "count": len(table_info)
            }
        except Exception as e:
            logger.error(f"Failed to list oracle tables: {e}")
            return {
                "success": False,
                "error": str(e),
                "tables": [],
                "count": 0
            }
    
    def get_oracle_table(self, table_name: str) -> Dict[str, Any]:
        """Get a specific oracle table"""
        try:
            table_data = self.data_access.get_oracle_table(table_name)
            
            return {
                "success": True,
                "table": table_data
            }
        except DataAccessError as e:
            logger.error(f"Failed to get oracle table {table_name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def roll_oracle_table(self, table_name: str, roll: Optional[int] = None) -> Dict[str, Any]:
        """Roll on an oracle table"""
        try:
            result = self.data_access.roll_oracle_table(table_name, roll)
            
            logger.info(f"Rolled on oracle table '{table_name}': {result.get('roll', 'unknown')} = {result.get('result', 'unknown')}")
            return {
                "success": True,
                "table": table_name,
                "result": result
            }
        except DataAccessError as e:
            logger.error(f"Failed to roll on oracle table {table_name}: {e}")
            return {
                "success": False,
                "error": str(e),
                "table": table_name
            }
    
    def create_oracle_table(self, table_name: str, table_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new oracle table"""
        try:
            created_table = self.data_access.create_oracle_table(table_name, table_data)
            
            logger.info(f"Created oracle table: {table_name}")
            return {
                "success": True,
                "table": created_table,
                "message": f"Oracle table '{table_name}' created successfully"
            }
        except DataAccessError as e:
            logger.error(f"Failed to create oracle table {table_name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def update_oracle_table(self, table_name: str, table_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing oracle table"""
        try:
            updated_table = self.data_access.update_oracle_table(table_name, table_data)
            
            logger.info(f"Updated oracle table: {table_name}")
            return {
                "success": True,
                "table": updated_table,
                "message": f"Oracle table '{table_name}' updated successfully"
            }
        except DataAccessError as e:
            logger.error(f"Failed to update oracle table {table_name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def delete_oracle_table(self, table_name: str) -> Dict[str, Any]:
        """Delete an oracle table"""
        try:
            success = self.data_access.delete_oracle_table(table_name)
            
            if success:
                logger.info(f"Deleted oracle table: {table_name}")
                return {
                    "success": True,
                    "message": f"Oracle table '{table_name}' deleted successfully"
                }
            else:
                return {
                    "success": False,
                    "error": f"Oracle table '{table_name}' not found"
                }
        except DataAccessError as e:
            logger.error(f"Failed to delete oracle table {table_name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def search_oracle_tables(self, query: str, category: Optional[str] = None) -> Dict[str, Any]:
        """Search for oracle tables"""
        try:
            results = self.data_access.search_oracle_tables(query, category)
            
            return {
                "success": True,
                "query": query,
                "category": category,
                "results": results,
                "count": len(results)
            }
        except Exception as e:
            logger.error(f"Failed to search oracle tables: {e}")
            return {
                "success": False,
                "error": str(e),
                "query": query,
                "category": category,
                "results": [],
                "count": 0
            }
    
    def get_table_statistics(self, table_name: str) -> Dict[str, Any]:
        """Get statistics about an oracle table"""
        try:
            stats = self.data_access.get_table_statistics(table_name)
            
            return {
                "success": True,
                "table": table_name,
                "statistics": stats
            }
        except DataAccessError as e:
            logger.error(f"Failed to get statistics for oracle table {table_name}: {e}")
            return {
                "success": False,
                "error": str(e),
                "table": table_name
            }
    
    # Utility methods
    def get_available_categories(self) -> List[str]:
        """Get all available oracle table categories"""
        try:
            tables = self.data_access.list_oracle_tables()
            categories = set()
            
            for table_file in tables:
                try:
                    table_data = self.data_access.get_oracle_table(table_file)
                    category = table_data.get('category', '')
                    if category:
                        categories.add(category)
                except DataAccessError:
                    continue
            
            return sorted(list(categories))
        except Exception as e:
            logger.error(f"Failed to get available categories: {e}")
            return [] 
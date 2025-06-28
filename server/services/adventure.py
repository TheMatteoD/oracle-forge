"""
Adventure Service for Oracle Forge

This service contains business logic for adventure management including:
- Adventure creation and selection
- World state management
- World entity CRUD operations
- Map file management
"""

import os
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path

from ..data_access import AdventureDataAccess, DataAccessError
from ..config import get_config

logger = logging.getLogger(__name__)


class AdventureService:
    """Service class for adventure-related business logic"""
    
    def __init__(self):
        self.data_access = AdventureDataAccess()
        self.config = get_config()
        self.active_adventure_path = os.path.join("server", "state", "active_adventure.txt")
    
    # Adventure Management
    def list_adventures(self) -> List[str]:
        """List all available adventures"""
        try:
            return self.data_access.list_adventures()
        except DataAccessError as e:
            logger.error(f"Failed to list adventures: {e}")
            return []
    
    def create_adventure(self, adventure_name: str) -> Dict[str, Any]:
        """Create a new adventure with full structure"""
        try:
            # Create adventure using data access layer
            adventure_data = self.data_access.create_adventure(adventure_name)
            
            # Set as active adventure
            self._set_active_adventure(adventure_name)
            
            logger.info(f"Created adventure: {adventure_name}")
            return {
                "success": True,
                "adventure_name": adventure_name,
                "message": f"Adventure '{adventure_name}' created successfully"
            }
        except DataAccessError as e:
            logger.error(f"Failed to create adventure {adventure_name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def select_adventure(self, adventure_name: str) -> Dict[str, Any]:
        """Select an adventure as active"""
        try:
            # Verify adventure exists
            adventures = self.data_access.list_adventures()
            if adventure_name not in adventures:
                # Create it if it doesn't exist
                return self.create_adventure(adventure_name)
            
            # Set as active
            self._set_active_adventure(adventure_name)
            
            logger.info(f"Selected adventure: {adventure_name}")
            return {
                "success": True,
                "adventure_name": adventure_name,
                "message": f"Adventure '{adventure_name}' selected"
            }
        except Exception as e:
            logger.error(f"Failed to select adventure {adventure_name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_active_adventure(self) -> Optional[str]:
        """Get the currently active adventure"""
        try:
            if not os.path.exists(self.active_adventure_path):
                return None
            
            with open(self.active_adventure_path, 'r') as f:
                adventure = f.read().strip()
            
            # Verify the adventure still exists
            adventures = self.data_access.list_adventures()
            if adventure not in adventures:
                self.clear_active_adventure()
                return None
            
            return adventure
        except Exception as e:
            logger.error(f"Failed to get active adventure: {e}")
            return None
    
    def clear_active_adventure(self) -> Dict[str, Any]:
        """Clear the active adventure"""
        try:
            if os.path.exists(self.active_adventure_path):
                os.remove(self.active_adventure_path)
            
            logger.info("Cleared active adventure")
            return {
                "success": True,
                "message": "Active adventure cleared"
            }
        except Exception as e:
            logger.error(f"Failed to clear active adventure: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def delete_adventure(self, adventure_name: str) -> Dict[str, Any]:
        """Delete an adventure and all its data"""
        try:
            # Check if it's the active adventure
            active = self.get_active_adventure()
            if active == adventure_name:
                self.clear_active_adventure()
            
            # Delete the adventure
            success = self.data_access.delete_adventure(adventure_name)
            
            if success:
                logger.info(f"Deleted adventure: {adventure_name}")
                return {
                    "success": True,
                    "message": f"Adventure '{adventure_name}' deleted"
                }
            else:
                return {
                    "success": False,
                    "error": f"Adventure '{adventure_name}' not found"
                }
        except DataAccessError as e:
            logger.error(f"Failed to delete adventure {adventure_name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    # World State Management
    def get_world_state(self, adventure_name: str) -> Dict[str, Any]:
        """Get the world state for an adventure"""
        try:
            return self.data_access.get_world_state(adventure_name)
        except DataAccessError as e:
            logger.error(f"Failed to get world state for {adventure_name}: {e}")
            return {}
    
    def update_world_state(self, adventure_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update the world state for an adventure"""
        try:
            updated_state = self.data_access.update_world_state(adventure_name, data)
            logger.info(f"Updated world state for {adventure_name}")
            return {
                "success": True,
                "world_state": updated_state
            }
        except DataAccessError as e:
            logger.error(f"Failed to update world state for {adventure_name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    # World Entity Management
    def list_world_entities(self, adventure_name: str, entity_type: str) -> Dict[str, Any]:
        """List all entities of a specific type"""
        try:
            entities = self.data_access.list_world_entities(adventure_name, entity_type)
            return {
                "success": True,
                "entities": entities,
                "count": len(entities)
            }
        except DataAccessError as e:
            logger.error(f"Failed to list {entity_type} for {adventure_name}: {e}")
            return {
                "success": False,
                "error": str(e),
                "entities": []
            }
    
    def get_world_entity(self, adventure_name: str, entity_type: str, entity_name: str) -> Dict[str, Any]:
        """Get a specific world entity"""
        try:
            entity_data = self.data_access.get_world_entity(adventure_name, entity_type, entity_name)
            return {
                "success": True,
                "entity": entity_data
            }
        except DataAccessError as e:
            logger.error(f"Failed to get {entity_type} {entity_name} for {adventure_name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_world_entity(self, adventure_name: str, entity_type: str, entity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new world entity"""
        try:
            created_entity = self.data_access.create_world_entity(adventure_name, entity_type, entity_data)
            logger.info(f"Created {entity_type} {entity_data.get('name', 'unknown')} for {adventure_name}")
            return {
                "success": True,
                "entity": created_entity
            }
        except DataAccessError as e:
            logger.error(f"Failed to create {entity_type} for {adventure_name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def update_world_entity(self, adventure_name: str, entity_type: str, entity_name: str, entity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a world entity"""
        try:
            updated_entity = self.data_access.update_world_entity(adventure_name, entity_type, entity_name, entity_data)
            logger.info(f"Updated {entity_type} {entity_name} for {adventure_name}")
            return {
                "success": True,
                "entity": updated_entity
            }
        except DataAccessError as e:
            logger.error(f"Failed to update {entity_type} {entity_name} for {adventure_name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def delete_world_entity(self, adventure_name: str, entity_type: str, entity_name: str) -> Dict[str, Any]:
        """Delete a world entity"""
        try:
            success = self.data_access.delete_world_entity(adventure_name, entity_type, entity_name)
            if success:
                logger.info(f"Deleted {entity_type} {entity_name} for {adventure_name}")
                return {
                    "success": True,
                    "message": f"{entity_type.title()} '{entity_name}' deleted"
                }
            else:
                return {
                    "success": False,
                    "error": f"{entity_type.title()} '{entity_name}' not found"
                }
        except DataAccessError as e:
            logger.error(f"Failed to delete {entity_type} {entity_name} for {adventure_name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    # Map File Management
    def upload_map_file(self, adventure_name: str, file_data: bytes, filename: str) -> Dict[str, Any]:
        """Upload a map file for an adventure"""
        try:
            # Validate file type
            if not filename.endswith(".map"):
                return {
                    "success": False,
                    "error": "Invalid file type. Only .map files are allowed."
                }
            
            # Save the file
            map_dir = os.path.join(self.data_access._get_adventure_path(adventure_name), "world")
            os.makedirs(map_dir, exist_ok=True)
            
            map_path = os.path.join(map_dir, "map.map")
            with open(map_path, 'wb') as f:
                f.write(file_data)
            
            logger.info(f"Uploaded map file for {adventure_name}")
            return {
                "success": True,
                "message": "Map file uploaded successfully"
            }
        except Exception as e:
            logger.error(f"Failed to upload map file for {adventure_name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_map_file_path(self, adventure_name: str) -> Optional[str]:
        """Get the path to the map file for an adventure"""
        try:
            map_path = os.path.join(self.data_access._get_adventure_path(adventure_name), "world", "map.map")
            if os.path.exists(map_path):
                return map_path
            return None
        except Exception as e:
            logger.error(f"Failed to get map file path for {adventure_name}: {e}")
            return None
    
    # Custom Map Image Management
    def upload_custom_map_image(self, adventure_name: str, file_data: bytes, filename: str) -> Dict[str, Any]:
        """Upload a custom map image for an adventure"""
        try:
            # Validate file type
            allowed_extensions = {"png", "jpg", "jpeg"}
            file_ext = filename.rsplit(".", 1)[1].lower() if "." in filename else ""
            
            if file_ext not in allowed_extensions:
                return {
                    "success": False,
                    "error": f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
                }
            
            # Save the file
            map_dir = os.path.join(self.data_access._get_adventure_path(adventure_name), "world", "custom_maps")
            os.makedirs(map_dir, exist_ok=True)
            
            file_path = os.path.join(map_dir, filename)
            with open(file_path, 'wb') as f:
                f.write(file_data)
            
            logger.info(f"Uploaded custom map image {filename} for {adventure_name}")
            return {
                "success": True,
                "filename": filename,
                "message": "Custom map image uploaded successfully"
            }
        except Exception as e:
            logger.error(f"Failed to upload custom map image for {adventure_name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def list_custom_map_images(self, adventure_name: str) -> List[str]:
        """List all custom map images for an adventure"""
        try:
            map_dir = os.path.join(self.data_access._get_adventure_path(adventure_name), "world", "custom_maps")
            if not os.path.exists(map_dir):
                return []
            
            allowed_extensions = {"png", "jpg", "jpeg"}
            files = [
                f for f in os.listdir(map_dir)
                if f.rsplit(".", 1)[1].lower() in allowed_extensions
            ]
            return files
        except Exception as e:
            logger.error(f"Failed to list custom map images for {adventure_name}: {e}")
            return []
    
    def get_custom_map_image_path(self, adventure_name: str, filename: str) -> Optional[str]:
        """Get the path to a custom map image"""
        try:
            # Validate file type
            allowed_extensions = {"png", "jpg", "jpeg"}
            file_ext = filename.rsplit(".", 1)[1].lower() if "." in filename else ""
            
            if file_ext not in allowed_extensions:
                return None
            
            map_dir = os.path.join(self.data_access._get_adventure_path(adventure_name), "world", "custom_maps")
            file_path = os.path.join(map_dir, filename)
            
            if os.path.exists(file_path):
                return file_path
            return None
        except Exception as e:
            logger.error(f"Failed to get custom map image path for {adventure_name}: {e}")
            return None
    
    # Private helper methods
    def _set_active_adventure(self, adventure_name: str) -> None:
        """Set an adventure as active"""
        os.makedirs(os.path.dirname(self.active_adventure_path), exist_ok=True)
        with open(self.active_adventure_path, 'w') as f:
            f.write(adventure_name) 
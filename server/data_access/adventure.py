"""
Adventure DataAccess class for Oracle Forge

This module provides data access operations for adventures, sessions,
world entities (NPCs, factions, locations, story lines), and players.
"""

import os
from typing import Dict, List, Optional, Any
from pathlib import Path

from .base import BaseDataAccess, DataAccessError, ValidationError
from ..utils.paths import (
    get_adventures_path,
    get_adventure_path,
    get_adventure_file_path,
)


class AdventureDataAccess(BaseDataAccess):
    """Data access class for adventure-related operations"""
    
    def get_domain_name(self) -> str:
        return "Adventure"
    
    # Adventure Management
    def list_adventures(self) -> List[Dict[str, str]]:
        """List all available adventures as dicts with id and name"""
        adventures_path = get_adventures_path()
        self.log_operation("list_adventures", f"Scanning {adventures_path}")
        names = self._list_directories(adventures_path)
        return [{"id": name, "name": name} for name in names]
    
    def create_adventure(self, adventure_name: str) -> Dict[str, Any]:
        """Create a new adventure with default files"""
        adventure_path = get_adventure_path(adventure_name)
        
        if os.path.exists(adventure_path):
            raise DataAccessError(f"Adventure '{adventure_name}' already exists")
        
        self.log_operation("create_adventure", f"Creating {adventure_name}")
        
        # Create adventure directory structure
        self._ensure_directory(adventure_path)
        self._ensure_directory(os.path.join(adventure_path, "world"))
        self._ensure_directory(os.path.join(adventure_path, "world", "npcs"))
        self._ensure_directory(os.path.join(adventure_path, "world", "factions"))
        self._ensure_directory(os.path.join(adventure_path, "world", "locations"))
        self._ensure_directory(os.path.join(adventure_path, "world", "story_lines"))
        self._ensure_directory(os.path.join(adventure_path, "world", "custom_maps"))
        self._ensure_directory(os.path.join(adventure_path, "players"))
        self._ensure_directory(os.path.join(adventure_path, "sessions"))
        
        # Create default files from templates
        world_state = self._create_from_template(
            "adventures/world_state.yaml",
            {"chaos_factor": 5, "current_scene": 1, "days_passed": 0},
            get_adventure_file_path(adventure_name, "world_state.yaml")
        )
        
        player_states = self._create_from_template(
            "adventures/player_states.yaml",
            {"players": []},
            get_adventure_file_path(adventure_name, "player_states.yaml")
        )
        
        active_session_data = {"adventure": adventure_name, "session_id": "session_01"}
        active_session = self._create_from_template(
            "adventures/active_session.yaml",
            active_session_data,
            get_adventure_file_path(adventure_name, "active_session.yaml")
        )
        # Also create the first session file in sessions/
        session_file_path = os.path.join(adventure_path, "sessions", "session_01.yaml")
        self._create_from_template(
            "adventures/sessions/session_template.yaml",
            active_session_data,
            session_file_path
        )
        
        return {
            "adventure_name": adventure_name,
            "world_state": world_state,
            "player_states": player_states,
            "active_session": active_session
        }
    
    def delete_adventure(self, adventure_name: str) -> bool:
        """Delete an adventure and all its data"""
        adventure_path = get_adventure_path(adventure_name)
        
        if not os.path.exists(adventure_path):
            return False
        
        self.log_operation("delete_adventure", f"Deleting {adventure_name}")
        
        try:
            import shutil
            shutil.rmtree(adventure_path)
            return True
        except Exception as e:
            raise DataAccessError(f"Failed to delete adventure {adventure_name}: {e}")
    
    # World State Management
    def get_world_state(self, adventure_name: str) -> Dict[str, Any]:
        """Get the world state for an adventure"""
        file_path = get_adventure_file_path(adventure_name, "world_state.yaml")
        return self._load_yaml(file_path)
    
    def update_world_state(self, adventure_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update the world state for an adventure"""
        file_path = get_adventure_file_path(adventure_name, "world_state.yaml")
        self._save_yaml(file_path, data)
        self.log_operation("update_world_state", f"Updated {adventure_name}")
        return data
    
    # Player Management
    def get_player_states(self, adventure_name: str) -> Dict[str, Any]:
        """Get player states for an adventure"""
        file_path = get_adventure_file_path(adventure_name, "player_states.yaml")
        return self._load_yaml(file_path)
    
    def create_player(self, adventure_name: str, player_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new player character"""
        # Generate safe filename from player name
        player_name = player_data.get('name', 'unknown')
        safe_filename = self._safe_filename(player_name) + '.yaml'
        
        # Create player file from template
        player_path = os.path.join(get_adventure_path(adventure_name), "players", safe_filename)
        player_data = self._create_from_template(
            "adventures/players/player_template.yaml",
            player_data,
            player_path
        )
        
        # Update player_states.yaml to include new player
        player_states = self.get_player_states(adventure_name)
        players = player_states.get('players', [])
        if safe_filename not in players:
            players.append(safe_filename)
            player_states['players'] = players
            self.update_player_states(adventure_name, player_states)
        
        self.log_operation("create_player", f"Created player {player_name} in {adventure_name}")
        return player_data
    
    def get_player(self, adventure_name: str, player_filename: str) -> Dict[str, Any]:
        """Get a specific player character"""
        player_path = os.path.join(get_adventure_path(adventure_name), "players", player_filename)
        return self._load_yaml(player_path)
    
    def update_player(self, adventure_name: str, player_filename: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a player character"""
        player_path = os.path.join(get_adventure_path(adventure_name), "players", player_filename)
        self._save_yaml(player_path, data)
        self.log_operation("update_player", f"Updated {player_filename} in {adventure_name}")
        return data
    
    def delete_player(self, adventure_name: str, player_filename: str) -> bool:
        """Delete a player character"""
        player_path = os.path.join(get_adventure_path(adventure_name), "players", player_filename)
        
        # Remove from player_states.yaml
        player_states = self.get_player_states(adventure_name)
        players = player_states.get('players', [])
        if player_filename in players:
            players.remove(player_filename)
            player_states['players'] = players
            self.update_player_states(adventure_name, player_states)
        
        # Delete the file
        return self._delete_file(player_path)
    
    def update_player_states(self, adventure_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update player states for an adventure"""
        file_path = get_adventure_file_path(adventure_name, "player_states.yaml")
        self._save_yaml(file_path, data)
        return data
    
    # Session Management
    def get_active_session(self, adventure_name: str) -> Dict[str, Any]:
        """Get the active session for an adventure"""
        file_path = get_adventure_file_path(adventure_name, "active_session.yaml")
        return self._load_yaml(file_path)
    
    def update_active_session(self, adventure_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update the active session for an adventure"""
        file_path = get_adventure_file_path(adventure_name, "active_session.yaml")
        self._save_yaml(file_path, data)
        return data
    
    def create_session(self, adventure_name: str, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new session"""
        # Generate session filename
        session_id = session_data.get('session_id', 'session_01')
        session_filename = f"{session_id}.yaml"
        
        # Create session file from template
        session_path = os.path.join(get_adventure_path(adventure_name), "sessions", session_filename)
        session_data = self._create_from_template(
            "adventures/sessions/session_template.yaml",
            session_data,
            session_path
        )
        
        self.log_operation("create_session", f"Created session {session_id} in {adventure_name}")
        return session_data
    
    def get_session(self, adventure_name: str, session_filename: str) -> Dict[str, Any]:
        """Get a specific session"""
        session_path = os.path.join(get_adventure_path(adventure_name), "sessions", session_filename)
        return self._load_yaml(session_path)
    
    def list_sessions(self, adventure_name: str) -> List[str]:
        """List all sessions for an adventure"""
        sessions_path = os.path.join(get_adventure_path(adventure_name), "sessions")
        return self._list_files(sessions_path)
    
    # World Entity Management (NPCs, Factions, Locations, Story Lines)
    def _get_world_entity_path(self, adventure_name: str, entity_type: str) -> str:
        """Get the path for a world entity type"""
        return os.path.join(get_adventure_path(adventure_name), "world", entity_type)
    
    def _get_entity_template_path(self, entity_type: str) -> str:
        """Get the template path for an entity type"""
        # Convert plural to singular for template names
        singular_map = {
            "npcs": "npc",
            "factions": "faction", 
            "locations": "location",
            "story_lines": "story_line"
        }
        singular_type = singular_map.get(entity_type, entity_type.rstrip('s'))
        return f"adventures/world/{entity_type}/{singular_type}_template.yaml"
    
    def list_world_entities(self, adventure_name: str, entity_type: str) -> List[str]:
        """List all entities of a specific type"""
        entity_path = self._get_world_entity_path(adventure_name, entity_type)
        return self._list_files(entity_path)
    
    def create_world_entity(self, adventure_name: str, entity_type: str, 
                          entity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new world entity (NPC, faction, location, story line)"""
        # Generate safe filename from entity name
        entity_name = entity_data.get('name', 'unknown')
        safe_filename = self._safe_filename(entity_name) + '.yaml'
        
        # Create entity file from template
        entity_path = os.path.join(self._get_world_entity_path(adventure_name, entity_type), safe_filename)
        entity_data = self._create_from_template(
            self._get_entity_template_path(entity_type),
            entity_data,
            entity_path
        )
        
        self.log_operation("create_world_entity", f"Created {entity_type} {entity_name} in {adventure_name}")
        return entity_data
    
    def get_world_entity(self, adventure_name: str, entity_type: str, 
                        entity_filename: str) -> Dict[str, Any]:
        """Get a specific world entity"""
        entity_path = os.path.join(self._get_world_entity_path(adventure_name, entity_type), entity_filename)
        return self._load_yaml(entity_path)
    
    def update_world_entity(self, adventure_name: str, entity_type: str, 
                          entity_filename: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a world entity"""
        entity_path = os.path.join(self._get_world_entity_path(adventure_name, entity_type), entity_filename)
        self._save_yaml(entity_path, data)
        self.log_operation("update_world_entity", f"Updated {entity_type} {entity_filename} in {adventure_name}")
        return data
    
    def delete_world_entity(self, adventure_name: str, entity_type: str, 
                          entity_filename: str) -> bool:
        """Delete a world entity"""
        entity_path = os.path.join(self._get_world_entity_path(adventure_name, entity_type), entity_filename)
        return self._delete_file(entity_path)
    
    # Convenience methods for specific entity types
    def create_npc(self, adventure_name: str, npc_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new NPC"""
        return self.create_world_entity(adventure_name, "npcs", npc_data)
    
    def create_faction(self, adventure_name: str, faction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new faction"""
        return self.create_world_entity(adventure_name, "factions", faction_data)
    
    def create_location(self, adventure_name: str, location_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new location"""
        return self.create_world_entity(adventure_name, "locations", location_data)
    
    def create_story_line(self, adventure_name: str, story_line_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new story line"""
        return self.create_world_entity(adventure_name, "story_lines", story_line_data) 
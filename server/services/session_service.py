"""
Session Service for Oracle Forge

This service contains business logic for session management including:
- Character creation and management
- Session state management
- Session logging
- Session summarization
"""

import os
import logging
import re
from typing import Dict, List, Optional, Any
from datetime import datetime

from ..data_access import AdventureDataAccess, DataAccessError
from scripts.llm.flavoring import summarize_session_log_llm

logger = logging.getLogger(__name__)


class SessionService:
    """Service class for session-related business logic"""
    
    def __init__(self):
        self.data_access = AdventureDataAccess()
        self.active_adventure_path = os.path.join("server", "state", "active_adventure.txt")
    
    # Active Adventure Management
    def get_active_adventure(self) -> Optional[str]:
        """Get the currently active adventure"""
        try:
            if not os.path.exists(self.active_adventure_path):
                print("active adventure file didn't exist")
                return None
            
            with open(self.active_adventure_path, 'r') as f:
                adventure = f.read().strip()
            
            # Verify the adventure still exists
            adventures = self.data_access.list_adventures()
            adventure_names = [a['name'] for a in adventures]
            if adventure not in adventure_names:
                print("current adventure not in list of adventures. Clearing active")
                print("Current active: ", adventure)
                print("List of adventures: ", adventure_names)
                self._clear_active_adventure()
                return None
            
            return adventure
        except Exception as e:
            logger.error(f"Failed to get active adventure: {e}")
            return None
    
    def _clear_active_adventure(self) -> None:
        """Clear the active adventure file"""
        try:
            if os.path.exists(self.active_adventure_path):
                os.remove(self.active_adventure_path)
        except Exception as e:
            logger.error(f"Failed to clear active adventure: {e}")
    
    # Character Management
    def create_character(self, character_name: str) -> Dict[str, Any]:
        """Create a new character for the active adventure"""
        try:
            adventure_name = self.get_active_adventure()
            if not adventure_name:
                return {
                    "success": False,
                    "error": "No active adventure"
                }
            
            if not character_name.strip():
                return {
                    "success": False,
                    "error": "Character name is required"
                }
            
            # Create character using data access layer
            character_data = self.data_access.create_player(adventure_name, character_name)
            
            logger.info(f"Created character '{character_name}' for adventure '{adventure_name}'")
            return {
                "success": True,
                "character": character_data,
                "message": f"Character '{character_name}' created successfully"
            }
        except DataAccessError as e:
            logger.error(f"Failed to create character {character_name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_character(self, character_name: str) -> Dict[str, Any]:
        """Get a character by name"""
        try:
            adventure_name = self.get_active_adventure()
            if not adventure_name:
                return {
                    "success": False,
                    "error": "No active adventure"
                }
            
            character_data = self.data_access.get_player(adventure_name, character_name)
            
            return {
                "success": True,
                "character": character_data
            }
        except DataAccessError as e:
            logger.error(f"Failed to get character {character_name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def update_character(self, character_name: str, character_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a character"""
        try:
            adventure_name = self.get_active_adventure()
            if not adventure_name:
                return {
                    "success": False,
                    "error": "No active adventure"
                }
            
            updated_character = self.data_access.update_player(adventure_name, character_name, character_data)
            
            logger.info(f"Updated character '{character_name}' for adventure '{adventure_name}'")
            return {
                "success": True,
                "character": updated_character,
                "message": f"Character '{character_name}' updated successfully"
            }
        except DataAccessError as e:
            logger.error(f"Failed to update character {character_name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def delete_character(self, character_name: str) -> Dict[str, Any]:
        """Delete a character"""
        try:
            adventure_name = self.get_active_adventure()
            if not adventure_name:
                return {
                    "success": False,
                    "error": "No active adventure"
                }
            
            success = self.data_access.delete_player(adventure_name, character_name)
            
            if success:
                logger.info(f"Deleted character '{character_name}' from adventure '{adventure_name}'")
                return {
                    "success": True,
                    "message": f"Character '{character_name}' deleted successfully"
                }
            else:
                return {
                    "success": False,
                    "error": f"Character '{character_name}' not found"
                }
        except DataAccessError as e:
            logger.error(f"Failed to delete character {character_name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def list_characters(self) -> Dict[str, Any]:
        """List all characters in the active adventure"""
        try:
            adventure_name = self.get_active_adventure()
            if not adventure_name:
                return {
                    "success": False,
                    "error": "No active adventure",
                    "characters": []
                }
            
            characters = self.data_access.list_players(adventure_name)
            
            return {
                "success": True,
                "characters": characters,
                "count": len(characters)
            }
        except DataAccessError as e:
            logger.error(f"Failed to list characters: {e}")
            return {
                "success": False,
                "error": str(e),
                "characters": [],
                "count": 0
            }
    
    # Session State Management
    def get_session_state(self) -> Dict[str, Any]:
        """Get the current session state including world, players, and session data"""
        try:
            adventure_name = self.get_active_adventure()
            if not adventure_name:
                return {
                    "success": False,
                    "error": "No active adventure"
                }
            
            # Get world state
            world_state = self.data_access.get_world_state(adventure_name)
            
            # Get all players
            players = self.data_access.get_player_states(adventure_name)
            
            # Get active session
            active_session = self.data_access.get_active_session(adventure_name)
            
            return {
                "success": True,
                "world": world_state,
                "players": players,
                "session": active_session,
                "combat_log": active_session.get("combat_log", [])
            }
        except DataAccessError as e:
            logger.error(f"Failed to get session state: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def update_session_state(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update the active session state"""
        try:
            adventure_name = self.get_active_adventure()
            if not adventure_name:
                return {
                    "success": False,
                    "error": "No active adventure"
                }
            
            updated_session = self.data_access.update_active_session(adventure_name, session_data)
            
            logger.info(f"Updated session state for adventure '{adventure_name}'")
            return {
                "success": True,
                "session": updated_session,
                "message": "Session state updated successfully"
            }
        except DataAccessError as e:
            logger.error(f"Failed to update session state: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    # Session Logging
    def get_session_log(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Get the session log"""
        try:
            adventure_name = self.get_active_adventure()
            if not adventure_name:
                return {
                    "success": False,
                    "error": "No active adventure",
                    "log": []
                }

            if session_id:
                session_data = self.data_access.get_session(adventure_name, session_id)
            else:
                # Always get the active session for the current log
                session_data = self.data_access.get_active_session(adventure_name)

            log = session_data.get("log", [])
            return {
                "success": True,
                "log": log,
                "count": len(log)
            }
        except DataAccessError as e:
            logger.error(f"Failed to get session log: {e}")
            return {
                "success": False,
                "error": str(e),
                "log": [],
                "count": 0
            }
    
    def append_session_log(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        """Append an entry to the session log"""
        try:
            adventure_name = self.get_active_adventure()
            if not adventure_name:
                return {
                    "success": False,
                    "error": "No active adventure"
                }
            
            if not entry or not entry.get("content"):
                return {
                    "success": False,
                    "error": "Empty log entry"
                }
            
            # Create log entry with timestamp
            log_entry = {
                "timestamp": entry.get("timestamp") or datetime.now().isoformat(),
                "type": entry.get("type", "custom"),
                "content": entry["content"]
            }
            
            # Get current session and append entry
            active_session = self.data_access.get_active_session(adventure_name)
            log = active_session.get("log", [])
            log.append(log_entry)
            active_session["log"] = log
            
            # Update the session
            updated_session = self.data_access.update_active_session(adventure_name, active_session)
            
            logger.info(f"Appended log entry to session for adventure '{adventure_name}'")
            return {
                "success": True,
                "entry": log_entry,
                "message": "Log entry added successfully"
            }
        except DataAccessError as e:
            logger.error(f"Failed to append session log: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_session(self, session_id: str) -> Dict[str, Any]:
        """Create a new session"""
        try:
            adventure_name = self.get_active_adventure()
            if not adventure_name:
                return {
                    "success": False,
                    "error": "No active adventure"
                }
            
            session_data = self.data_access.create_session(adventure_name, session_id)
            
            logger.info(f"Created session '{session_id}' for adventure '{adventure_name}'")
            return {
                "success": True,
                "session": session_data,
                "message": f"Session '{session_id}' created successfully"
            }
        except DataAccessError as e:
            logger.error(f"Failed to create session {session_id}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def end_session(self) -> Dict[str, Any]:
        """End the current session and generate summary, archive it, and reset active session"""
        try:
            adventure_name = self.get_active_adventure()
            if not adventure_name:
                return {
                    "success": False,
                    "error": "No active adventure"
                }
            
            # Get current session log
            active_session = self.data_access.get_active_session(adventure_name)
            log = active_session.get("log", [])
            
            if not log:
                return {
                    "success": False,
                    "error": "No session log to summarize"
                }
            
            # Generate summary using LLM
            try:
                summary = summarize_session_log_llm(log)
            except Exception as e:
                logger.warning(f"Failed to generate LLM summary, using fallback: {e}")
                summary = self._generate_fallback_summary(log)
            
            # Update session with summary and end timestamp
            active_session["summary"] = summary
            active_session["end_time"] = datetime.now().isoformat()
            active_session["status"] = "ended"
            
            # Archive the finished session to sessions/session_XX.yaml
            from server.utils.paths import get_adventure_path
            import shutil
            sessions_dir = os.path.join(get_adventure_path(adventure_name), "sessions")
            os.makedirs(sessions_dir, exist_ok=True)
            # Find next session number
            existing = [f for f in os.listdir(sessions_dir) if f.startswith("session_") and f.endswith(".yaml")]
            numbers = [int(f.split("_")[1].split(".")[0]) for f in existing if f.split("_")[1].split(".")[0].isdigit()]
            next_num = max(numbers) + 1 if numbers else 1
            session_id = f"session_{next_num:02d}"
            session_filename = f"{session_id}.yaml"
            session_path = os.path.join(sessions_dir, session_filename)
            # Save the finished session
            import yaml
            with open(session_path, "w") as f:
                yaml.safe_dump(active_session, f, sort_keys=False, allow_unicode=True)
            
            # Create new active_session.yaml from template
            from server.utils.paths import get_vault_template_path, get_adventure_file_path
            template_path = get_vault_template_path("adventures/active_session.yaml")
            with open(template_path, "r") as f:
                template_data = yaml.safe_load(f)
            template_data["adventure"] = adventure_name
            template_data["session_id"] = f"session_{next_num+1:02d}"
            template_data["log"] = []
            # Optionally reset metadata
            if "metadata" in template_data:
                template_data["metadata"]["start_time"] = datetime.now().isoformat()
                template_data["metadata"]["duration"] = ""
                template_data["metadata"]["scene_count"] = 0
                template_data["metadata"]["oracle_questions"] = 0
            # Save new active_session.yaml
            active_session_path = get_adventure_file_path(adventure_name, "active_session.yaml")
            with open(active_session_path, "w") as f:
                yaml.safe_dump(template_data, f, sort_keys=False, allow_unicode=True)
            
            logger.info(f"Ended session for adventure '{adventure_name}', archived as {session_filename}")
            return {
                "success": True,
                "session": active_session,
                "summary": summary,
                "session_id": session_id,
                "message": "Session ended and archived successfully"
            }
        except DataAccessError as e:
            logger.error(f"Failed to end session: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_session_summary(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Get a summary of the session"""
        try:
            adventure_name = self.get_active_adventure()
            if not adventure_name:
                return {
                    "success": False,
                    "error": "No active adventure"
                }
            
            if session_id:
                session_data = self.data_access.get_session(adventure_name, session_id)
            else:
                # Get the latest session
                sessions = self.data_access.list_sessions(adventure_name)
                if not sessions:
                    return {
                        "success": False,
                        "error": "No session found"
                    }
                
                latest_session = sessions[-1]
                session_data = self.data_access.get_session(adventure_name, latest_session)
            
            log = session_data.get("log", [])
            summary = session_data.get("summary")
            
            if not summary and log:
                # Generate summary if not exists
                try:
                    summary = summarize_session_log_llm(log)
                except Exception as e:
                    logger.warning(f"Failed to generate LLM summary, using fallback: {e}")
                    summary = self._generate_fallback_summary(log)
            
            return {
                "success": True,
                "summary": summary,
                "log_count": len(log),
                "session_id": session_data.get("session_id")
            }
        except DataAccessError as e:
            logger.error(f"Failed to get session summary: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    # Utility methods
    def _generate_fallback_summary(self, log: List[Dict[str, Any]]) -> str:
        """Generate a simple fallback summary when LLM is not available"""
        if not log:
            return "No session log entries found."
        
        entry_types = {}
        for entry in log:
            entry_type = entry.get("type", "custom")
            entry_types[entry_type] = entry_types.get(entry_type, 0) + 1
        
        summary_parts = [f"Session contained {len(log)} total entries:"]
        for entry_type, count in entry_types.items():
            summary_parts.append(f"- {count} {entry_type} entries")
        
        return " ".join(summary_parts)
    
    def sanitize_filename(self, name: str) -> str:
        """Convert character name to a safe filename"""
        # Remove special characters and replace spaces with underscores
        safe_name = re.sub(r'[^a-zA-Z0-9\s]', '', name)
        safe_name = re.sub(r'\s+', '_', safe_name).lower()
        return safe_name 
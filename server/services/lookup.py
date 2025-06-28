"""
Lookup Service for Oracle Forge

This service contains business logic for lookup operations including:
- Item, monster, spell, and rule lookups
- Filtering and searching logic
- Narration generation
- Random selection
"""

import logging
from typing import Dict, List, Optional, Any

from ..data_access import LookupDataAccess, DataAccessError
from scripts.llm.flavoring import narrate_items, narrate_monsters, narrate_spells, rewrite_narration

logger = logging.getLogger(__name__)


class LookupService:
    """Service class for lookup-related business logic"""
    
    def __init__(self):
        self.data_access = LookupDataAccess()
    
    # Monster Lookup
    def lookup_monsters(self, query: str = "", system: str = "", tag: str = "", 
                       environment: str = "", random_count: int = 0, 
                       narrate: bool = False, context: str = "", theme: str = "") -> Dict[str, Any]:
        """Lookup monsters with filtering and optional narration"""
        try:
            # Get all monsters
            systems = [system] if system else self.data_access.list_monster_systems()
            all_monsters = []
            
            for sys in systems:
                try:
                    monster_data = self.data_access.get_monster_data(sys)
                    monsters = monster_data.get('monsters', [])
                    for monster in monsters:
                        monster['system'] = sys
                        all_monsters.append(monster)
                except DataAccessError:
                    continue
            
            # Apply filters
            filtered_monsters = all_monsters
            
            if query:
                filtered_monsters = [
                    m for m in filtered_monsters
                    if query.lower() in m.get('name', '').lower() or 
                       query.lower() in m.get('description', '').lower()
                ]
            
            if system:
                filtered_monsters = [
                    m for m in filtered_monsters
                    if system.lower() in m.get('system', '').lower()
                ]
            
            if tag:
                filtered_monsters = [
                    m for m in filtered_monsters
                    if any(tag.lower() in t.lower() for t in m.get('tags', []))
                ]
            
            if environment:
                filtered_monsters = [
                    m for m in filtered_monsters
                    if environment.lower() in m.get('environment', '').lower()
                ]
            
            # Apply random selection
            if random_count > 0:
                import random
                filtered_monsters = random.sample(
                    filtered_monsters, 
                    min(random_count, len(filtered_monsters))
                )
            
            # Generate narration if requested
            narration = None
            if narrate and filtered_monsters:
                try:
                    narration = narrate_monsters(filtered_monsters, context, environment, theme, True)
                except Exception as e:
                    logger.warning(f"Failed to generate monster narration: {e}")
            
            return {
                "success": True,
                "items": filtered_monsters,
                "count": len(filtered_monsters),
                "narration": narration
            }
            
        except Exception as e:
            logger.error(f"Failed to lookup monsters: {e}")
            return {
                "success": False,
                "error": str(e),
                "items": [],
                "count": 0
            }
    
    # Spell Lookup
    def lookup_spells(self, query: str = "", system: str = "", spell_class: str = "", 
                     level: Optional[int] = None, tag: str = "", random_count: int = 0,
                     narrate: bool = False, context: str = "", theme: str = "") -> Dict[str, Any]:
        """Lookup spells with filtering and optional narration"""
        try:
            # Get all spells
            systems = [system] if system else self.data_access.list_spell_systems()
            all_spells = []
            
            for sys in systems:
                try:
                    spell_data = self.data_access.get_spell_data(sys)
                    spells = spell_data.get('spells', [])
                    for spell in spells:
                        spell['system'] = sys
                        all_spells.append(spell)
                except DataAccessError:
                    continue
            
            # Apply filters
            filtered_spells = all_spells
            
            if query:
                filtered_spells = [
                    s for s in filtered_spells
                    if query.lower() in s.get('name', '').lower() or 
                       query.lower() in s.get('description', '').lower()
                ]
            
            if system:
                filtered_spells = [
                    s for s in filtered_spells
                    if system.lower() in s.get('system', '').lower()
                ]
            
            if spell_class:
                filtered_spells = [
                    s for s in filtered_spells
                    if spell_class.lower() in s.get('class', '').lower()
                ]
            
            if level is not None:
                filtered_spells = [
                    s for s in filtered_spells
                    if s.get('level') == level
                ]
            
            if tag:
                filtered_spells = [
                    s for s in filtered_spells
                    if any(tag.lower() in t.lower() for t in s.get('tags', []))
                ]
            
            # Apply random selection
            if random_count > 0:
                import random
                filtered_spells = random.sample(
                    filtered_spells, 
                    min(random_count, len(filtered_spells))
                )
            
            # Generate narration if requested
            narration = None
            if narrate and filtered_spells:
                try:
                    narration = narrate_spells(filtered_spells, context, theme, True)
                except Exception as e:
                    logger.warning(f"Failed to generate spell narration: {e}")
            
            return {
                "success": True,
                "items": filtered_spells,
                "count": len(filtered_spells),
                "narration": narration
            }
            
        except Exception as e:
            logger.error(f"Failed to lookup spells: {e}")
            return {
                "success": False,
                "error": str(e),
                "items": [],
                "count": 0
            }
    
    # Item Lookup
    def lookup_items(self, query: str = "", system: str = "", category: str = "", 
                    subcategory: str = "", tag: str = "", random_count: int = 0,
                    narrate: bool = False, context: str = "", environment: str = "", 
                    quality: str = "", theme: str = "") -> Dict[str, Any]:
        """Lookup items with filtering and optional narration"""
        try:
            # Get all items
            categories = [category] if category else self.data_access.list_item_categories()
            all_items = []
            
            for cat in categories:
                try:
                    items = self.data_access.list_items_in_category(cat)
                    for item_file in items:
                        item_data = self.data_access.get_item(cat, item_file)
                        item_data['category'] = cat
                        all_items.append(item_data)
                except DataAccessError:
                    continue
            
            # Apply filters
            filtered_items = all_items
            
            if query:
                filtered_items = [
                    i for i in filtered_items
                    if query.lower() in i.get('name', '').lower() or 
                       query.lower() in i.get('description', '').lower()
                ]
            
            if system:
                filtered_items = [
                    i for i in filtered_items
                    if system.lower() in i.get('system', '').lower()
                ]
            
            if category:
                filtered_items = [
                    i for i in filtered_items
                    if category.lower() in i.get('category', '').lower()
                ]
            
            if subcategory:
                filtered_items = [
                    i for i in filtered_items
                    if subcategory.lower() in i.get('subcategory', '').lower()
                ]
            
            if tag:
                filtered_items = [
                    i for i in filtered_items
                    if any(tag.lower() in t.lower() for t in i.get('tags', []))
                ]
            
            # Apply random selection
            if random_count > 0:
                import random
                filtered_items = random.sample(
                    filtered_items, 
                    min(random_count, len(filtered_items))
                )
            
            # Generate narration if requested
            narration = None
            if narrate and filtered_items:
                try:
                    narration = narrate_items(filtered_items, context, environment, quality, theme, True)
                except Exception as e:
                    logger.warning(f"Failed to generate item narration: {e}")
            
            return {
                "success": True,
                "items": filtered_items,
                "count": len(filtered_items),
                "narration": narration
            }
            
        except Exception as e:
            logger.error(f"Failed to lookup items: {e}")
            return {
                "success": False,
                "error": str(e),
                "items": [],
                "count": 0
            }
    
    # Rule Lookup
    def lookup_rules(self, query: str = "", system: str = "", tag: str = "") -> Dict[str, Any]:
        """Lookup rules with filtering"""
        try:
            # Get all rules
            systems = [system] if system else self.data_access.list_rule_systems()
            all_rules = []
            
            for sys in systems:
                try:
                    rule_data = self.data_access.get_rule_data(sys)
                    rules = rule_data.get('rules', [])
                    for rule in rules:
                        rule['system'] = sys
                        all_rules.append(rule)
                except DataAccessError:
                    continue
            
            # Apply filters
            filtered_rules = all_rules
            
            if query:
                filtered_rules = [
                    r for r in filtered_rules
                    if query.lower() in r.get('title', '').lower() or 
                       query.lower() in r.get('content', '').lower()
                ]
            
            if system:
                filtered_rules = [
                    r for r in filtered_rules
                    if system.lower() in r.get('system', '').lower()
                ]
            
            if tag:
                filtered_rules = [
                    r for r in filtered_rules
                    if any(tag.lower() in t.lower() for t in r.get('tags', []))
                ]
            
            return {
                "success": True,
                "items": filtered_rules,
                "count": len(filtered_rules)
            }
            
        except Exception as e:
            logger.error(f"Failed to lookup rules: {e}")
            return {
                "success": False,
                "error": str(e),
                "items": [],
                "count": 0
            }
    
    # Narration Rewrite
    def rewrite_narration(self, original_narration: str, rewrite_instruction: str) -> Dict[str, Any]:
        """Rewrite an existing narration based on user instructions"""
        try:
            if not original_narration or not rewrite_instruction:
                return {
                    "success": False,
                    "error": "Both narration and instruction are required"
                }
            
            rewritten_narration = rewrite_narration(original_narration, rewrite_instruction, True)
            
            return {
                "success": True,
                "original_narration": original_narration,
                "rewrite_instruction": rewrite_instruction,
                "rewritten_narration": rewritten_narration
            }
            
        except Exception as e:
            logger.error(f"Failed to rewrite narration: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    # Utility methods
    def get_available_systems(self) -> Dict[str, List[str]]:
        """Get all available systems for each lookup type"""
        try:
            return {
                "monsters": self.data_access.list_monster_systems(),
                "spells": self.data_access.list_spell_systems(),
                "rules": self.data_access.list_rule_systems()
            }
        except Exception as e:
            logger.error(f"Failed to get available systems: {e}")
            return {
                "monsters": [],
                "spells": [],
                "rules": []
            }
    
    def get_available_categories(self) -> List[str]:
        """Get all available item categories"""
        try:
            return self.data_access.list_item_categories()
        except Exception as e:
            logger.error(f"Failed to get available categories: {e}")
            return [] 
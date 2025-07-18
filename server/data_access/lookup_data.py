"""
Lookup DataAccess class for Oracle Forge

This module provides data access operations for lookup data including:
- Items (equipment, valuables, trade goods, adventure gear, pets)
- Monsters
- Spells
- Rules
"""

import os
from typing import Dict, List, Optional, Any
from pathlib import Path

from .base_data import BaseDataAccess, DataAccessError, ValidationError
from ..utils.paths import (
    get_lookup_path,
    get_lookup_file_path,
)


class LookupDataAccess(BaseDataAccess):
    """Data access class for lookup-related operations"""
    
    def get_domain_name(self) -> str:
        return "Lookup"
    
    # Item Management
    def _get_item_category_path(self, category: str) -> str:
        """Get the path for an item category"""
        return os.path.join(get_lookup_path(), "items", category)
    
    def _get_item_template_path(self, category: str) -> str:
        """Get the template path for an item category"""
        return f"lookup/items/{category}/{category}_template.yaml"
    
    def list_item_categories(self) -> List[str]:
        """List all available item categories"""
        items_path = os.path.join(get_lookup_path(), "items")
        return self._list_directories(items_path)
    
    def list_items_in_category(self, category: str) -> List[str]:
        """List all items in a specific category"""
        category_path = self._get_item_category_path(category)
        return self._list_files(category_path)
    
    def get_item_category_data(self, category: str) -> Dict[str, Any]:
        """Get the main data file for an item category"""
        category_file = os.path.join(self._get_item_category_path(category), f"{category}.yaml")
        return self._load_yaml(category_file)
    
    def update_item_category_data(self, category: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update the main data file for an item category"""
        category_file = os.path.join(self._get_item_category_path(category), f"{category}.yaml")
        self._save_yaml(category_file, data)
        self.log_operation("update_item_category", f"Updated {category}")
        return data
    
    def create_item(self, category: str, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new item in a specific category"""
        # Generate safe filename from item name
        item_name = item_data.get('name', 'unknown')
        safe_filename = self._safe_filename(item_name) + '.yaml'
        
        # Create item file from template
        item_path = os.path.join(self._get_item_category_path(category), safe_filename)
        item_data = self._create_from_template(
            self._get_item_template_path(category),
            item_data,
            item_path
        )
        
        self.log_operation("create_item", f"Created {category} item {item_name}")
        return item_data
    
    def get_item(self, category: str, item_filename: str) -> Dict[str, Any]:
        """Get a specific item from a category"""
        item_path = os.path.join(self._get_item_category_path(category), item_filename)
        return self._load_yaml(item_path)
    
    def update_item(self, category: str, item_filename: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a specific item"""
        item_path = os.path.join(self._get_item_category_path(category), item_filename)
        self._save_yaml(item_path, data)
        self.log_operation("update_item", f"Updated {category} item {item_filename}")
        return data
    
    def delete_item(self, category: str, item_filename: str) -> bool:
        """Delete a specific item"""
        item_path = os.path.join(self._get_item_category_path(category), item_filename)
        return self._delete_file(item_path)
    
    def search_items(self, query: str, category: Optional[str] = None, 
                    system: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search for items across categories"""
        results = []
        
        categories = [category] if category else self.list_item_categories()
        
        for cat in categories:
            items = self.list_items_in_category(cat)
            for item_file in items:
                item_data = self.get_item(cat, item_file)
                
                # Apply filters
                if system and system.lower() not in item_data.get('system', '').lower():
                    continue
                
                # Search in name and description
                searchable_text = f"{item_data.get('name', '')} {item_data.get('description', '')}".lower()
                if query.lower() in searchable_text:
                    item_data['category'] = cat  # Add category info
                    results.append(item_data)
        
        return results
    
    # Monster Management
    def _get_monster_system_path(self, system: str = "OSE:AF") -> str:
        """Get the path for a monster system"""
        return os.path.join(get_lookup_path(), "monsters", system)
    
    def _get_monster_template_path(self) -> str:
        """Get the template path for monsters"""
        return "lookup/monsters/monster_template.yaml"
    
    def list_monster_systems(self) -> List[str]:
        """List all available monster systems"""
        monsters_path = os.path.join(get_lookup_path(), "monsters")
        return self._list_directories(monsters_path)
    
    def get_monster_data(self, system: str = "OSE:AF") -> Dict[str, Any]:
        """Get the main monster data for a system"""
        monster_file = os.path.join(self._get_monster_system_path(system), "monsters.yaml")
        return self._load_yaml(monster_file)
    
    def update_monster_data(self, system: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update the main monster data for a system"""
        monster_file = os.path.join(self._get_monster_system_path(system), "monsters.yaml")
        self._save_yaml(monster_file, data)
        self.log_operation("update_monster_data", f"Updated {system} monsters")
        return data
    
    def create_monster(self, system: str, monster_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new monster"""
        # Generate safe filename from monster name
        monster_name = monster_data.get('name', 'unknown')
        safe_filename = self._safe_filename(monster_name) + '.yaml'
        
        # Create monster file from template
        monster_path = os.path.join(self._get_monster_system_path(system), safe_filename)
        monster_data = self._create_from_template(
            self._get_monster_template_path(),
            monster_data,
            monster_path
        )
        
        self.log_operation("create_monster", f"Created monster {monster_name} in {system}")
        return monster_data
    
    def get_monster(self, system: str, monster_filename: str) -> Dict[str, Any]:
        """Get a specific monster"""
        monster_path = os.path.join(self._get_monster_system_path(system), monster_filename)
        return self._load_yaml(monster_path)
    
    def update_monster(self, system: str, monster_filename: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a specific monster"""
        monster_path = os.path.join(self._get_monster_system_path(system), monster_filename)
        self._save_yaml(monster_path, data)
        self.log_operation("update_monster", f"Updated {system} monster {monster_filename}")
        return data
    
    def delete_monster(self, system: str, monster_filename: str) -> bool:
        """Delete a specific monster"""
        monster_path = os.path.join(self._get_monster_system_path(system), monster_filename)
        return self._delete_file(monster_path)
    
    def search_monsters(self, query: str, system: Optional[str] = None, 
                       environment: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search for monsters"""
        results = []
        
        systems = [system] if system else self.list_monster_systems()
        
        for sys in systems:
            monsters = self.get_monster_data(sys)
            monster_list = monsters.get('monsters', [])
            
            for monster in monster_list:
                # Apply filters
                if environment and environment.lower() not in monster.get('environment', '').lower():
                    continue
                
                # Search in name and description
                searchable_text = f"{monster.get('name', '')} {monster.get('description', '')}".lower()
                if query.lower() in searchable_text:
                    monster['system'] = sys  # Add system info
                    results.append(monster)
        
        return results
    
    # Spell Management
    def _get_spell_system_path(self, system: str = "OSE:AF") -> str:
        """Get the path for a spell system"""
        return os.path.join(get_lookup_path(), "spells", system)
    
    def _get_spell_template_path(self) -> str:
        """Get the template path for spells"""
        return "lookup/spells/spell_template.yaml"
    
    def list_spell_systems(self) -> List[str]:
        """List all available spell systems"""
        spells_path = os.path.join(get_lookup_path(), "spells")
        return self._list_directories(spells_path)
    
    def get_spell_data(self, system: str = "OSE:AF") -> Dict[str, Any]:
        """Get the main spell data for a system"""
        spell_file = os.path.join(self._get_spell_system_path(system), "spells.yaml")
        return self._load_yaml(spell_file)
    
    def update_spell_data(self, system: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update the main spell data for a system"""
        spell_file = os.path.join(self._get_spell_system_path(system), "spells.yaml")
        self._save_yaml(spell_file, data)
        self.log_operation("update_spell_data", f"Updated {system} spells")
        return data
    
    def create_spell(self, system: str, spell_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new spell"""
        # Generate safe filename from spell name
        spell_name = spell_data.get('name', 'unknown')
        safe_filename = self._safe_filename(spell_name) + '.yaml'
        
        # Create spell file from template
        spell_path = os.path.join(self._get_spell_system_path(system), safe_filename)
        spell_data = self._create_from_template(
            self._get_spell_template_path(),
            spell_data,
            spell_path
        )
        
        self.log_operation("create_spell", f"Created spell {spell_name} in {system}")
        return spell_data
    
    def get_spell(self, system: str, spell_filename: str) -> Dict[str, Any]:
        """Get a specific spell"""
        spell_path = os.path.join(self._get_spell_system_path(system), spell_filename)
        return self._load_yaml(spell_path)
    
    def update_spell(self, system: str, spell_filename: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a specific spell"""
        spell_path = os.path.join(self._get_spell_system_path(system), spell_filename)
        self._save_yaml(spell_path, data)
        self.log_operation("update_spell", f"Updated {system} spell {spell_filename}")
        return data
    
    def delete_spell(self, system: str, spell_filename: str) -> bool:
        """Delete a specific spell"""
        spell_path = os.path.join(self._get_spell_system_path(system), spell_filename)
        return self._delete_file(spell_path)
    
    def search_spells(self, query: str, system: Optional[str] = None, 
                     spell_class: Optional[str] = None, level: Optional[int] = None) -> List[Dict[str, Any]]:
        """Search for spells"""
        results = []
        
        systems = [system] if system else self.list_spell_systems()
        
        for sys in systems:
            spells = self.get_spell_data(sys)
            spell_list = spells.get('spells', [])
            
            for spell in spell_list:
                # Apply filters
                if spell_class and spell_class.lower() not in spell.get('class', '').lower():
                    continue
                if level is not None and spell.get('level') != level:
                    continue
                
                # Search in name and description
                searchable_text = f"{spell.get('name', '')} {spell.get('description', '')}".lower()
                if query.lower() in searchable_text:
                    spell['system'] = sys  # Add system info
                    results.append(spell)
        
        return results
    
    # Rule Management
    def _get_rule_system_path(self, system: str = "OSE:AF") -> str:
        """Get the path for a rule system"""
        return os.path.join(get_lookup_path(), "rules", system)
    
    def list_rule_systems(self) -> List[str]:
        """List all available rule systems"""
        rules_path = os.path.join(get_lookup_path(), "rules")
        return self._list_directories(rules_path)
    
    def get_rule_data(self, system: str = "OSE:AF") -> Dict[str, Any]:
        """Get the main rule data for a system"""
        rule_file = os.path.join(self._get_rule_system_path(system), "rules.yaml")
        return self._load_yaml(rule_file)
    
    def update_rule_data(self, system: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update the main rule data for a system"""
        rule_file = os.path.join(self._get_rule_system_path(system), "rules.yaml")
        self._save_yaml(rule_file, data)
        self.log_operation("update_rule_data", f"Updated {system} rules")
        return data
    
    def search_rules(self, query: str, system: Optional[str] = None, 
                    tag: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search for rules"""
        results = []
        
        systems = [system] if system else self.list_rule_systems()
        
        for sys in systems:
            rules = self.get_rule_data(sys)
            rule_list = rules.get('rules', [])
            
            for rule in rule_list:
                # Apply filters
                if tag and tag.lower() not in [t.lower() for t in rule.get('tags', [])]:
                    continue
                
                # Search in title and content
                searchable_text = f"{rule.get('title', '')} {rule.get('content', '')}".lower()
                if query.lower() in searchable_text:
                    rule['system'] = sys  # Add system info
                    results.append(rule)
        
        return results 
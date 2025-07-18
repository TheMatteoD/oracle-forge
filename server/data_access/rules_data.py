"""
Rule DataAccess class for Oracle Forge

This module provides data access operations for rules including:
- Rule files stored as markdown
- Rule system management
- Rule searching and content extraction
"""

import os
import re
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path

from .base import BaseDataAccess, DataAccessError, ValidationError
from ..utils.paths import (
    get_rules_path,
)

logger = logging.getLogger(__name__)

class RuleDataAccess(BaseDataAccess):
    """Data access class for rule-related operations"""
    
    def get_domain_name(self) -> str:
        return "Rules"
    
    # Rule System Management
    def _get_rule_system_path(self, system: str = "OSE:AF") -> str:
        """Get the path for a rule system"""
        return os.path.join(get_rules_path(), system)
    
    def list_rule_systems(self) -> List[str]:
        """List all available rule systems"""
        rules_path = get_rules_path()
        return self._list_directories(rules_path)
    
    def list_rules(self, system: str = "OSE:AF") -> List[str]:
        """List all rules in a specific system"""
        system_path = self._get_rule_system_path(system)
        return self._list_files(system_path, "*.md")
    
    def get_rule(self, system: str, rule_name: str) -> Dict[str, Any]:
        """Get a specific rule file"""
        rule_path = os.path.join(self._get_rule_system_path(system), rule_name)
        return self._load_markdown(rule_path)
    
    def update_rule(self, system: str, rule_name: str, content: str) -> Dict[str, Any]:
        """Update a specific rule file"""
        rule_path = os.path.join(self._get_rule_system_path(system), rule_name)
        self._save_markdown(rule_path, content)
        self.log_operation("update_rule", f"Updated {system} rule {rule_name}")
        return {"system": system, "name": rule_name, "content": content}
    
    def create_rule(self, system: str, rule_name: str, content: str) -> Dict[str, Any]:
        """Create a new rule file"""
        # Generate safe filename
        safe_filename = self._safe_filename(rule_name) + '.md'
        
        # Create rule file
        rule_path = os.path.join(self._get_rule_system_path(system), safe_filename)
        self._save_markdown(rule_path, content)
        
        self.log_operation("create_rule", f"Created {system} rule {rule_name}")
        return {"system": system, "name": rule_name, "content": content}
    
    def delete_rule(self, system: str, rule_name: str) -> bool:
        """Delete a specific rule file"""
        rule_path = os.path.join(self._get_rule_system_path(system), rule_name)
        return self._delete_file(rule_path)
    
    def search_rules(self, query: str, system: Optional[str] = None, 
                    category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search for rules across systems"""
        results = []
        
        systems = [system] if system else self.list_rule_systems()
        
        for sys in systems:
            rules = self.list_rules(sys)
            for rule_file in rules:
                rule_data = self.get_rule(sys, rule_file)
                
                # Apply category filter (if we can extract it from content)
                if category and category.lower() not in rule_data.get('content', '').lower():
                    continue
                
                # Search in content
                if query.lower() in rule_data.get('content', '').lower():
                    rule_data['system'] = sys  # Add system info
                    rule_data['filename'] = rule_file  # Add filename info
                    results.append(rule_data)
        
        return results
    
    def get_rule_metadata(self, system: str, rule_name: str) -> Dict[str, Any]:
        """Extract metadata from a rule file"""
        rule_data = self.get_rule(system, rule_name)
        content = rule_data.get('content', '')
        
        # Extract title from first heading
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else rule_name.replace('.md', '')
        
        # Extract categories/tags from content
        categories = []
        if 'combat' in content.lower():
            categories.append('combat')
        if 'adventure' in content.lower():
            categories.append('adventure')
        if 'character' in content.lower():
            categories.append('character')
        if 'movement' in content.lower():
            categories.append('movement')
        
        # Count sections (## headings)
        sections = len(re.findall(r'^##\s+', content, re.MULTILINE))
        
        # Estimate word count
        word_count = len(content.split())
        
        return {
            'system': system,
            'name': rule_name,
            'title': title,
            'categories': categories,
            'sections': sections,
            'word_count': word_count,
            'filename': rule_name
        }
    
    def get_rule_sections(self, system: str, rule_name: str) -> List[Dict[str, Any]]:
        """Extract sections from a rule file"""
        rule_data = self.get_rule(system, rule_name)
        content = rule_data.get('content', '')
        
        sections = []
        lines = content.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            if line.startswith('## '):
                # Save previous section
                if current_section:
                    sections.append({
                        'title': current_section,
                        'content': '\n'.join(current_content).strip()
                    })
                
                # Start new section
                current_section = line[3:].strip()
                current_content = []
            elif current_section:
                current_content.append(line)
        
        # Add final section
        if current_section:
            sections.append({
                'title': current_section,
                'content': '\n'.join(current_content).strip()
            })
        
        return sections
    
    def search_rule_content(self, query: str, system: str, rule_name: str) -> List[Dict[str, Any]]:
        """Search within a specific rule file"""
        rule_data = self.get_rule(system, rule_name)
        content = rule_data.get('content', '')
        
        results = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            if query.lower() in line.lower():
                # Get context (previous and next lines)
                context_start = max(0, i - 3)
                context_end = min(len(lines), i + 3)
                context = lines[context_start:context_end]
                
                results.append({
                    'line_number': i,
                    'line': line.strip(),
                    'context': '\n'.join(context)
                })
        
        return results
    
    # Markdown-specific methods
    def _load_markdown(self, file_path: str) -> Dict[str, Any]:
        """Load a markdown file safely"""
        if not os.path.exists(file_path):
            return {}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return {"content": content}
        except Exception as e:
            raise DataAccessError(f"Failed to load markdown file {file_path}: {e}")
    
    def _save_markdown(self, file_path: str, content: str) -> None:
        """Save content to a markdown file safely"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"Saved markdown to {file_path}")
        except Exception as e:
            raise DataAccessError(f"Failed to save markdown file {file_path}: {e}")
    
    def _list_files(self, directory: str, pattern: str = "*.yaml") -> List[str]:
        """List files in a directory with custom pattern"""
        if not os.path.exists(directory):
            return []
        
        try:
            files = []
            for file in os.listdir(directory):
                if file.endswith(pattern[1:]) and not file.startswith('_'):
                    files.append(file)
            return sorted(files)
        except Exception as e:
            raise DataAccessError(f"Failed to list files in {directory}: {e}")
    
    # Rule System Management
    def create_rule_system(self, system_name: str) -> Dict[str, Any]:
        """Create a new rule system directory"""
        system_path = self._get_rule_system_path(system_name)
        
        if os.path.exists(system_path):
            raise DataAccessError(f"Rule system '{system_name}' already exists")
        
        self._ensure_directory(system_path)
        
        # Create a README file for the system
        readme_content = f"# {system_name} Rules\n\nThis directory contains rule files for the {system_name} system."
        readme_path = os.path.join(system_path, "README.md")
        self._save_markdown(readme_path, readme_content)
        
        self.log_operation("create_rule_system", f"Created rule system {system_name}")
        return {"system_name": system_name, "path": system_path}
    
    def delete_rule_system(self, system_name: str) -> bool:
        """Delete a rule system and all its rules"""
        system_path = self._get_rule_system_path(system_name)
        
        if not os.path.exists(system_path):
            return False
        
        self.log_operation("delete_rule_system", f"Deleting {system_name}")
        
        try:
            import shutil
            shutil.rmtree(system_path)
            return True
        except Exception as e:
            raise DataAccessError(f"Failed to delete rule system {system_name}: {e}")
    
    # Convenience methods
    def get_combat_rules(self, system: str = "OSE:AF") -> List[Dict[str, Any]]:
        """Get all combat-related rules"""
        return self.search_rules("combat", system)
    
    def get_adventure_rules(self, system: str = "OSE:AF") -> List[Dict[str, Any]]:
        """Get all adventure-related rules"""
        return self.search_rules("adventure", system)
    
    def get_character_rules(self, system: str = "OSE:AF") -> List[Dict[str, Any]]:
        """Get all character-related rules"""
        return self.search_rules("character", system)
    
    def get_rule_summary(self, system: str = "OSE:AF") -> Dict[str, Any]:
        """Get a summary of all rules in a system"""
        rules = self.list_rules(system)
        
        summary = {
            'system': system,
            'total_rules': len(rules),
            'rules': []
        }
        
        for rule_file in rules:
            metadata = self.get_rule_metadata(system, rule_file)
            summary['rules'].append(metadata)
        
        return summary
    
    def export_rule_system(self, system: str, format: str = "markdown") -> str:
        """Export all rules in a system"""
        rules = self.list_rules(system)
        
        if format.lower() == "markdown":
            content = f"# {system} Rules\n\n"
            for rule_file in rules:
                rule_data = self.get_rule(system, rule_file)
                content += f"## {rule_file}\n\n"
                content += rule_data.get('content', '') + "\n\n"
            return content
        else:
            raise DataAccessError(f"Unsupported export format: {format}")
    
    def import_rule_system(self, system: str, rules_data: Dict[str, str], 
                          overwrite: bool = False) -> Dict[str, Any]:
        """Import rules into a system"""
        # Create system if it doesn't exist
        if not os.path.exists(self._get_rule_system_path(system)):
            self.create_rule_system(system)
        
        imported_rules = []
        for rule_name, content in rules_data.items():
            if not overwrite and rule_name in self.list_rules(system):
                continue
            
            self.create_rule(system, rule_name, content)
            imported_rules.append(rule_name)
        
        return {
            'system': system,
            'imported_rules': imported_rules,
            'total_imported': len(imported_rules)
        } 
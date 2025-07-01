"""
Centralized Configuration Management for Oracle Forge

This module provides a type-safe, environment-aware configuration system
that loads from environment variables with YAML fallback, validates required
configuration, and supports different environments (dev, staging, prod).
"""

import os
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class DatabaseConfig:
    """Database configuration settings"""
    vault_path: str = "vault"
    vault_templates_path: str = "vault_templates"
    adventures_path: str = "vault/adventures"
    templates_path: str = "vault/templates"
    tables_path: str = "vault/tables"
    lookup_path: str = "vault/lookup"
    rules_path: str = "vault/rules"
    index_path: str = "vault/index"


@dataclass
class LLMConfig:
    """LLM configuration settings"""
    model_path: str = "./models/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
    chaos_factor: int = 5
    max_tokens: int = 2048
    temperature: float = 0.7


@dataclass
class ServerConfig:
    """Server configuration settings"""
    host: str = "0.0.0.0"
    port: int = 5000
    debug: bool = False
    cors_origins: List[str] = field(default_factory=lambda: ["http://localhost:5173"])
    secret_key: Optional[str] = None


@dataclass
class AppConfig:
    """Main application configuration"""
    environment: str = "development"
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    llm: LLMConfig = field(default_factory=LLMConfig)
    server: ServerConfig = field(default_factory=ServerConfig)
    
    # Additional app-specific settings
    log_level: str = "INFO"
    enable_rate_limiting: bool = True
    max_file_size: int = 10 * 1024 * 1024  # 10MB


class ConfigManager:
    """Manages application configuration with environment variable support and validation"""
    
    def __init__(self, config_path: str = "config/settings.yaml"):
        self.config_path = Path(config_path)
        self._config: Optional[AppConfig] = None
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from YAML file and environment variables"""
        # Start with defaults
        config = AppConfig()
        
        # Load from YAML file if it exists
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    yaml_config = yaml.safe_load(f) or {}
                config = self._merge_yaml_config(config, yaml_config)
                logger.info(f"Loaded configuration from {self.config_path}")
            except Exception as e:
                logger.warning(f"Failed to load YAML config from {self.config_path}: {e}")
        
        # Override with environment variables
        config = self._apply_environment_overrides(config)
        
        # Validate configuration
        self._validate_config(config)
        
        self._config = config
        logger.info(f"Configuration loaded for environment: {config.environment}")
    
    def _merge_yaml_config(self, base_config: AppConfig, yaml_data: Dict[str, Any]) -> AppConfig:
        """Merge YAML configuration with base configuration"""
        # Database config
        if 'database' in yaml_data:
            db_data = yaml_data['database']
            base_config.database.vault_path = db_data.get('vault_path', base_config.database.vault_path)
            base_config.database.vault_templates_path = db_data.get('vault_templates_path', base_config.database.vault_templates_path)
            base_config.database.adventures_path = db_data.get('adventures_path', base_config.database.adventures_path)
            base_config.database.templates_path = db_data.get('templates_path', base_config.database.templates_path)
            base_config.database.tables_path = db_data.get('tables_path', base_config.database.tables_path)
            base_config.database.lookup_path = db_data.get('lookup_path', base_config.database.lookup_path)
            base_config.database.rules_path = db_data.get('rules_path', base_config.database.rules_path)
            base_config.database.index_path = db_data.get('index_path', base_config.database.index_path)
        
        # LLM config
        if 'llm' in yaml_data:
            llm_data = yaml_data['llm']
            base_config.llm.model_path = llm_data.get('model_path', base_config.llm.model_path)
            base_config.llm.chaos_factor = llm_data.get('chaos_factor', base_config.llm.chaos_factor)
            base_config.llm.max_tokens = llm_data.get('max_tokens', base_config.llm.max_tokens)
            base_config.llm.temperature = llm_data.get('temperature', base_config.llm.temperature)
        
        # Server config
        if 'server' in yaml_data:
            server_data = yaml_data['server']
            base_config.server.host = server_data.get('host', base_config.server.host)
            base_config.server.port = server_data.get('port', base_config.server.port)
            base_config.server.debug = server_data.get('debug', base_config.server.debug)
            base_config.server.cors_origins = server_data.get('cors_origins', base_config.server.cors_origins)
            base_config.server.secret_key = server_data.get('secret_key', base_config.server.secret_key)
        
        # App config
        base_config.environment = yaml_data.get('environment', base_config.environment)
        base_config.log_level = yaml_data.get('log_level', base_config.log_level)
        base_config.enable_rate_limiting = yaml_data.get('enable_rate_limiting', base_config.enable_rate_limiting)
        base_config.max_file_size = yaml_data.get('max_file_size', base_config.max_file_size)
        
        return base_config
    
    def _apply_environment_overrides(self, config: AppConfig) -> AppConfig:
        """Apply environment variable overrides to configuration"""
        # Environment
        config.environment = os.getenv('ORACLE_FORGE_ENV', config.environment)
        
        # Database paths
        config.database.vault_path = os.getenv('ORACLE_FORGE_VAULT_PATH', config.database.vault_path)
        config.database.vault_templates_path = os.getenv('ORACLE_FORGE_VAULT_TEMPLATES_PATH', config.database.vault_templates_path)
        config.database.adventures_path = os.getenv('ORACLE_FORGE_ADVENTURES_PATH', config.database.adventures_path)
        config.database.templates_path = os.getenv('ORACLE_FORGE_TEMPLATES_PATH', config.database.templates_path)
        config.database.tables_path = os.getenv('ORACLE_FORGE_TABLES_PATH', config.database.tables_path)
        config.database.lookup_path = os.getenv('ORACLE_FORGE_LOOKUP_PATH', config.database.lookup_path)
        config.database.rules_path = os.getenv('ORACLE_FORGE_RULES_PATH', config.database.rules_path)
        config.database.index_path = os.getenv('ORACLE_FORGE_INDEX_PATH', config.database.index_path)
        
        # LLM settings
        config.llm.model_path = os.getenv('ORACLE_FORGE_MODEL_PATH', config.llm.model_path)
        config.llm.chaos_factor = int(os.getenv('ORACLE_FORGE_CHAOS_FACTOR', str(config.llm.chaos_factor)))
        config.llm.max_tokens = int(os.getenv('ORACLE_FORGE_MAX_TOKENS', str(config.llm.max_tokens)))
        config.llm.temperature = float(os.getenv('ORACLE_FORGE_TEMPERATURE', str(config.llm.temperature)))
        
        # Server settings
        config.server.host = os.getenv('ORACLE_FORGE_HOST', config.server.host)
        config.server.port = int(os.getenv('ORACLE_FORGE_PORT', str(config.server.port)))
        config.server.debug = os.getenv('ORACLE_FORGE_DEBUG', str(config.server.debug)).lower() == 'true'
        config.server.secret_key = os.getenv('ORACLE_FORGE_SECRET_KEY', config.server.secret_key)
        
        # CORS origins (comma-separated)
        cors_origins = os.getenv('ORACLE_FORGE_CORS_ORIGINS')
        if cors_origins:
            config.server.cors_origins = [origin.strip() for origin in cors_origins.split(',')]
        
        # App settings
        config.log_level = os.getenv('ORACLE_FORGE_LOG_LEVEL', config.log_level)
        config.enable_rate_limiting = os.getenv('ORACLE_FORGE_RATE_LIMITING', str(config.enable_rate_limiting)).lower() == 'true'
        config.max_file_size = int(os.getenv('ORACLE_FORGE_MAX_FILE_SIZE', str(config.max_file_size)))
        
        return config
    
    def _validate_config(self, config: AppConfig) -> None:
        """Validate required configuration values"""
        errors = []
        
        # Validate required paths exist
        required_paths = [
            ('vault_path', config.database.vault_path),
            ('vault_templates_path', config.database.vault_templates_path),
            ('adventures_path', config.database.adventures_path),
            ('templates_path', config.database.templates_path),
            ('tables_path', config.database.tables_path),
            ('lookup_path', config.database.lookup_path),
            ('rules_path', config.database.rules_path),
        ]
        
        for name, path in required_paths:
            if not Path(path).exists():
                errors.append(f"Required path '{name}' does not exist: {path}")
        
        # Validate LLM model path
        if not Path(config.llm.model_path).exists():
            errors.append(f"LLM model not found: {config.llm.model_path}")
        
        # Validate chaos factor range
        if not 1 <= config.llm.chaos_factor <= 9:
            errors.append(f"Chaos factor must be between 1 and 9, got: {config.llm.chaos_factor}")
        
        # Validate server port
        if not 1 <= config.server.port <= 65535:
            errors.append(f"Server port must be between 1 and 65535, got: {config.server.port}")
        
        if errors:
            error_msg = "Configuration validation failed:\n" + "\n".join(f"  - {error}" for error in errors)
            logger.error(error_msg)
            raise ValueError(error_msg)
    
    def get_database_path(self, path_type: str) -> str:
        """Get a database path by type, always absolute from project root"""
        path_map = {
            'vault': self.config.database.vault_path,
            'vault_templates': self.config.database.vault_templates_path,
            'adventures': self.config.database.adventures_path,
            'templates': self.config.database.templates_path,
            'tables': self.config.database.tables_path,
            'lookup': self.config.database.lookup_path,
            'rules': self.config.database.rules_path,
            'index': self.config.database.index_path,
        }
        rel_path = path_map.get(path_type, self.config.database.vault_path)
        # Project root is one level up from server/
        base = Path(__file__).parent.parent.resolve()
        abs_path = (base / rel_path).resolve()
        return str(abs_path)
    
    @property
    def config(self) -> AppConfig:
        """Get the current configuration"""
        if self._config is None:
            self._load_config()
        # Always return AppConfig, never None
        assert self._config is not None, "Config failed to load."
        return self._config
    
    def reload(self) -> None:
        """Reload configuration from disk"""
        self._config = None
        self._load_config()
    
    def export_to_yaml(self, path: str) -> None:
        """Export current configuration to YAML file"""
        config_dict = {
            'environment': self.config.environment,
            'database': {
                'vault_path': self.config.database.vault_path,
                'vault_templates_path': self.config.database.vault_templates_path,
                'adventures_path': self.config.database.adventures_path,
                'templates_path': self.config.database.templates_path,
                'tables_path': self.config.database.tables_path,
                'lookup_path': self.config.database.lookup_path,
                'rules_path': self.config.database.rules_path,
                'index_path': self.config.database.index_path,
            },
            'llm': {
                'model_path': self.config.llm.model_path,
                'chaos_factor': self.config.llm.chaos_factor,
                'max_tokens': self.config.llm.max_tokens,
                'temperature': self.config.llm.temperature,
            },
            'server': {
                'host': self.config.server.host,
                'port': self.config.server.port,
                'debug': self.config.server.debug,
                'cors_origins': self.config.server.cors_origins,
                'secret_key': self.config.server.secret_key,
            },
            'log_level': self.config.log_level,
            'enable_rate_limiting': self.config.enable_rate_limiting,
            'max_file_size': self.config.max_file_size,
        }
        
        with open(path, 'w') as f:
            yaml.dump(config_dict, f, default_flow_style=False, indent=2)


# Global configuration instance
config_manager = ConfigManager()


def get_config() -> AppConfig:
    """Get the global configuration instance"""
    return config_manager.config


def get_database_path(path_type: str) -> str:
    """Get a database path by type"""
    return config_manager.get_database_path(path_type)


def reload_config() -> None:
    """Reload the global configuration"""
    config_manager.reload() 
import logging
from flask import Flask
from flask_cors import CORS
from .routes.oracle_routes import oracle
from .routes.lookup_routes import lookup
from .routes.adventure_routes import adventure
from .routes.generators_routes import generators
from .routes.combat_routes import combat_bp
from .routes.session_routes import session
from .config import get_config, config_manager
from .middleware.error_handlers import register_error_handlers
from .middleware.rate_limiting import register_rate_limiting
from .services.adventure_service import AdventureService

# Configure logging
logging.basicConfig(
    level=getattr(logging, get_config().log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

# Get configuration
config = get_config()

# Configure CORS
CORS(app, origins=config.server.cors_origins)

# Set Flask secret key
if config.server.secret_key:
    app.secret_key = config.server.secret_key
else:
    app.secret_key = 'dev-secret-key-change-in-production'

# Register middleware
register_error_handlers(app)
register_rate_limiting(app)

# Register blueprints
app.register_blueprint(oracle)
app.register_blueprint(lookup)
app.register_blueprint(adventure)
app.register_blueprint(generators)
app.register_blueprint(combat_bp)
app.register_blueprint(session)

# Game Init - clears active adventure on startup
adventure_service = AdventureService()
adventure_service.clear_active_adventure()

# Add configuration endpoint for debugging
@app.route("/config/status", methods=["GET"])
def config_status():
    """Return current configuration status (for debugging)"""
    return {
        "environment": config.environment,
        "database_paths": {
            "vault": config.database.vault_path,
            "adventures": config.database.adventures_path,
            "templates": config.database.templates_path,
        },
        "llm": {
            "model_path": config.llm.model_path,
            "chaos_factor": config.llm.chaos_factor,
        },
        "server": {
            "host": config.server.host,
            "port": config.server.port,
            "debug": config.server.debug,
        }
    }

# Add API health check endpoint
@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for API monitoring"""
    return {
        "status": "healthy",
        "service": "Oracle Forge API",
        "version": "1.0.0"
    }

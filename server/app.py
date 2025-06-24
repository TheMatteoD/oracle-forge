import yaml
from flask import Flask
from flask_cors import CORS
from .routes.oracle import oracle
from .routes.lookup import lookup
from .routes.adventure import adventure, reset_active_adventure
from .routes.generators import generators
from .routes.combat import combat_bp
from .routes.session import session

app = Flask(__name__)

with open('config/settings.yaml', 'r') as f:
    settings = yaml.safe_load(f)

CORS(app, origins=settings.get('cors_origins', []))

# Register blueprints
app.register_blueprint(oracle)
app.register_blueprint(lookup)
app.register_blueprint(adventure)
app.register_blueprint(generators)
app.register_blueprint(combat_bp)
app.register_blueprint(session)

# Game Init - clears active adventure on startup
reset_active_adventure()

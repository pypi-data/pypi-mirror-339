from flask import Flask
from app.routes import register_routes

def create_app(config_class="app.config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register all routes
    register_routes(app)

    return app
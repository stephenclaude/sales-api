from flask import Flask
import os


def create_app():
    app = Flask(__name__)

    # Configuration
    app.config["DATABASE"] = os.path.join(os.path.dirname(__file__), "..", "data.db")

    # Register routes
    from app.routes import api_bp

    app.register_blueprint(api_bp)

    return app

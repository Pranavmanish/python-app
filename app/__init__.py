from flask import Flask
from .models import db
from .routes import routes
from .config import Config

def create_app():
    app = Flask(__name__)

    # 👇 Add this print BEFORE config is set
    print("Pre-config value (should be empty):", app.config.get("SQLALCHEMY_DATABASE_URI"))

    # ✅ Load config
    app.config.from_object(Config)

    # 👇 Add this print AFTER config is set
    print("APP CONFIG DEBUG (after setting):", app.config.get("SQLALCHEMY_DATABASE_URI"))

    db.init_app(app)
    app.register_blueprint(routes)

    return app

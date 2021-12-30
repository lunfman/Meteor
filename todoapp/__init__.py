from flask import Flask
from config import DevelopmentConfig
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    from .dashboard import dashboard
    from .service import service
    from .category import category
    from .help import help
    app.register_blueprint(dashboard)
    app.register_blueprint(service)
    app.register_blueprint(category)
    app.register_blueprint(help)

    return app
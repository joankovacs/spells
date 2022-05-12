from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/spells_development'

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes.spell import spells_bp
    app.register_blueprint(spells_bp)

    from app.models.spell import Spell

    return app

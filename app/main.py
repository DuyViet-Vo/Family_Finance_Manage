# main.py

from flasgger import Swagger
from flask import Flask
from flask_migrate import Migrate

from config.settings import SECRET_KEY  # flake8: noqa
from config.settings import SQLALCHEMY_DATABASE_URI, SWAGGER_SETTINGS
from models import db
from routes.group_routers import group_db
from routes.product_routes import product_bp
from routes.user_routes import user_bp


def create_app():
    app = Flask(__name__)
    app.config.update(SWAGGER_SETTINGS)
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SECRET_KEY"] = SECRET_KEY

    db.init_app(app)
    migrate = Migrate(app, db)  # noqa

    with app.app_context():
        db.create_all()

    app.register_blueprint(user_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(group_db)

    Swagger(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

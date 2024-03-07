# main.py

from flask import Flask
from config.settings import SWAGGER_SETTINGS, SQLALCHEMY_DATABASE_URI
from models import db
from routes.user_routes import user_bp
from routes.product_routes import product_bp
from routes.group_routers import group_db
from flasgger import Swagger
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config.update(SWAGGER_SETTINGS)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

    db.init_app(app)
    migrate = Migrate(app, db)  # Thêm dòng này để khởi tạo Flask-Migrate

    with app.app_context():
        db.create_all()

    app.register_blueprint(user_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(group_db)

    Swagger(app)

    return app
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

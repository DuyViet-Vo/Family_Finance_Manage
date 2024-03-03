from flask import Flask
from config.settings import SWAGGER_SETTINGS, SQLALCHEMY_DATABASE_URI
from models import db
from routes.user_routes import user_bp
from routes.product_routes import product_bp
from flasgger import Swagger

def create_app():
    app = Flask(__name__)
    app.config.update(SWAGGER_SETTINGS)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(user_bp)
    app.register_blueprint(product_bp)

    Swagger(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

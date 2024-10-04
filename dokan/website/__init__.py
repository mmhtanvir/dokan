from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "dokan"

def create_app():
    app = Flask(__name__, static_url_path='/website/static')
    app.config['UPLOAD_FOLDER'] = 'static/product'
    app.config['SECRET_KEY'] = "secretkey"
    app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql://root:@localhost/{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .admin import admin

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(admin, url_prefix="/")

    from .models import User, Role, Item, Cart, Order

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists("website/" + DB_NAME):
        with app.app_context():
            db.create_all()
        print("Database created!")
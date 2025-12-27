# app/__init__.py

from flask import Flask
from flask_login import LoginManager
from app.extensions.postgres import db, init_db
from config import Config

# 在 app/__init__.py 中添加
from app.models.user import User
from app.models.honor import Honor, UserHonor
from app.models.forum import Post, Comment, Like, Bookmark, Message, Follow

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Register blueprints
    from app.routes.main import bp as main_bp
    from app.routes.auth import bp as auth_bp
    from app.routes.admin import bp as admin_bp
    from app.routes.member import bp as member_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(member_bp, url_prefix='/member')
    
    # Create tables
    with app.app_context():
        init_db()
    
    return app

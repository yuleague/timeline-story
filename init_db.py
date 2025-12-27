from app import create_app
from app.extensions.postgres import db

app = create_app()

with app.app_context():
    # Create all tables
    db.create_all()
    print("数据库表已创建")
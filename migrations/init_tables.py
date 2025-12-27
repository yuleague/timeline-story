#!/usr/bin/env python3
"""
数据库表初始化脚本
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions.postgres import db
from app.models.user import User
from app.models.honor import Honor, UserHonor
from app.models.forum import Post, Comment, Like, Bookmark, Message, Follow

def init_database():
    """初始化数据库表"""
    app = create_app()
    
    with app.app_context():
        # 删除所有表（危险操作，仅用于开发）
        # db.drop_all()
        
        # 创建所有表
        db.create_all()
        
        print("✅ 数据库表创建成功！")
        print("创建的表包括：")
        print("  - users (用户表)")
        print("  - honors (荣誉表)")
        print("  - user_honors (用户荣誉关联表)")
        print("  - follows (关注关系表)")
        print("  - posts (帖子表)")
        print("  - comments (评论表)")
        print("  - likes (点赞表)")
        print("  - bookmarks (收藏表)")
        print("  - messages (私信表)")
        
        # 创建默认管理员账户
        create_default_admin()
        
def create_default_admin():
    """创建默认管理员账户"""
    from werkzeug.security import generate_password_hash
    
    admin = User.query.filter_by(mobile='13800138000').first()
    if not admin:
        admin = User(
            mobile='13800138000',
            email='admin@jqd.yuleague.cn',
            username='系统管理员',
            password_hash=generate_password_hash('xiaoshong123'),
            preset_code='123456',
            join_year=1987,
            role='admin',
            is_active=True
        )
        db.session.add(admin)
        db.session.commit()
        print("👑 默认管理员账户已创建")
        print("  手机号: 13800138000")
        print("  密码: xiaoshong123")
        print("  预设码: 123456")
    
    print("🎉 数据库初始化完成！")

if __name__ == '__main__':
    init_database()
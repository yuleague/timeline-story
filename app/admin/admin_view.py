# app/admin/admin_view.py
"""
系统管理员数据中台视图

这是管理员登录之后的跳转页面
1. 会员管理模块
2. 数据操作模块
3. 数据统计模块
---以下功能模块暂不需要---
4. 系统设置模块
5. 系统日志模块
6. 系统监控模块
"""

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.user import User
from app.utils.forms import PostForm, CommentForm, TagForm, CategoryForm
from app.extensions.cf_d1 import db
from app.utils import redirect_back

admin_view = Blueprint('admin_view', __name__)

@admin_view.route('/admin')
@login_required
def admin():
    return render_template('admin/admin.html')

def admin_required(func):
    @login_required
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            flash('Admins only!')
            return redirect_back()
        return func(*args, **kwargs)
    return wrapper

class UserAdminView:
    def __init__(self):
        self.user = User.query.all()
        self.user_count = len(self.user)
        self.user_list = [user.username for user in self.user]
        self.user_list.sort()
        self.user_list = list(set(self.user_list))
        self.user_list.sort()

    def get_user(self, username):
        user = User.query.filter_by(username=username).first()
        return user

    def get_user_by_id(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        return user

    def get_user_by_moblie(self, moblie):
        user = User.query.filter_by(moblie=moblie).first()
        return user

    def delete_user(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        db.session.delete(user)
        db.session.commit()

    def freeze_user(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        user.is_freeze = True
        db.session.commit()

    def unfreeze_user(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        user.is_freeze = False
        db.session.commit()

from app.models.events import Events
class EventsDataAdminView:

# app/admin/admin.py
"""
系统管理员模块

1. 管理员模型
2. 管理员登录：鉴权
3. 管理员视图及路由
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User, Role
from extentions.cf_d1 import db
from utils.forms import LoginForm, RegistrationForm, EditProfileForm

admin = Blueprint('admin', __name__)

@admin.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('admin.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('admin.index'))
    return render_template('admin/login.html', title='Sign In', form=form)

@admin.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))

# ========= 以下内容应该是User模型相关，暂放在此处 =========
# 不应该使用admin.route装饰器，应该使用app.route装饰器
@admin.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data, moblie=form.moblie.data, avatar=form.avatar.data, role_id=1)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('admin.login'))
    return render_template('admin/register.html', title='Register', form=form)

@admin.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.moblie = form.moblie.data
        current_user.avatar = form.avatar.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('admin.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.moblie.data = current_user.moblie
        form.avatar.data = current_user.avatar
    return render_template('admin/edit_profile.html', title='Edit Profile', form=form)

@admin.route('/admin')
@login_required
def admin():
    return render_template('admin/templates/admin.html', title='System Management')
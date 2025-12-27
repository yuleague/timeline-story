from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.extensions.postgres import db
from app.models.user import User
from datetime import datetime

bp = Blueprint('profile', __name__)

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        mobile = request.form['mobile']
        username = request.form['username']
        password = request.form['password']
        
        try:
            user = User.query.filter_by(id=current_user.id).first()
            user.mobile = mobile
            user.username = username
            user.password = password
            db.session.commit()
            
            flash('Profile updated successfully', 'success')
            return redirect(url_for('profile.profile'))
            
        except Exception as e:
            flash(f'Profile update failed: {str(e)}', 'error')
    
    return render_template('profile/profile.html')

@bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        
        # Check if email is in whitelist
        whitelist_entry = Whitelist.query.filter_by(email=email, status='approved').first()
        if not whitelist_entry:
            flash('邮箱不在白名单中，请联系管理员', 'error')
            return redirect(url_for('profile.forgot_password'))
        
        try:
            # Send password reset email
            profile_response = supabase.profile.send_reset_password_email(email)
            
            if profile_response:
                flash('密码重置邮件已发送，请检查邮箱', 'success')
                return redirect(url_for('auth.login'))
            
        except Exception as e:
            flash(f'发送失败: {str(e)}', 'error')
    
    return render_template('profile/forgot_password.html')

@bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        token = request.args.get('token')
        password = request.form['password']
        
        try:
            # Reset password with Supabase
            auth_response = supabase.auth.update({
                "password": password
            }, token)
            
            if auth_response.user:
                flash('密码重置成功，请登录', 'success')
                return redirect(url_for('auth.login'))
            
        except Exception as e:
            flash(f'重置失败: {str(e)}', 'error')
    
    return render_template('profile/reset_password.html')

@bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        
        try:
            # Authenticate with Supabase
            auth_response = supabase.auth.sign_in_with_password({
                "mobile": current_user.mobile,
                "password": <PASSWORD>
            })
            
            if auth_response.user:
                # Update password with Supabase
                auth_response = supabase.auth.update({
                    "password": <PASSWORD>
                }, auth_response.access_token)
                
                if auth_response.user:
                    flash('密码修改成功', 'success')
                    return redirect(url_for('profile'))
            
        except Exception as e:
            flash(f'修改失败: {str(e)}', 'error')
    
    return render_template('profile/change_password.html')

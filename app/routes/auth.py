from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.extensions.postgres import db, supabase
from app.models.user import User
from app.models.whitelist import Whitelist
from datetime import datetime

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        
        # Check if email is in whitelist
        whitelist_entry = Whitelist.query.filter_by(email=email, status='approved').first()
        if not whitelist_entry:
            flash('邮箱不在白名单中，请联系管理员', 'error')
            return redirect(url_for('auth.register'))
        
        try:
            # Create user in Supabase Auth
            auth_response = supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            
            if auth_response.user:
                # Create user in our database
                user = User(
                    email=email,
                    username=username,
                    role='member'
                )
                db.session.add(user)
                db.session.commit()
                
                flash('注册成功！请登录', 'success')
                return redirect(url_for('auth.login'))
                
        except Exception as e:
            flash(f'注册失败: {str(e)}', 'error')
    
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        try:
            # Authenticate with Supabase
            auth_response = supabase.auth.sign_in_with_password({
                "mobile": mobile,
                "password": password
            })
            
            if auth_response.user:
                # Find user in our database
                user = User.query.filter_by(mobile=mobile).first()
                if user:
                    user.last_login = datetime.utcnow()
                    db.session.commit()
                    login_user(user)
                    return redirect(url_for('main.index'))
            
        except Exception as e:
            flash('登录失败，请检查手机和密码', 'error')
    
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已退出登录', 'success')
    return redirect(url_for('home'))

@bp.route('/member', methods=['GET', 'POST'])
@login_required
def member():
    """
    定义会员页面，登录后的会员可以访问。
    展示会员List：
    1. 显示会员名、头像、入队时间、荣誉
    2. 点击会员List的条目，可以查看会员个人主页==profile_detail.html
    """
    def get_member_list():
        """
        从数据库获取会员列表
        """
        members = User.query.filter_by(role='member').all()
        return members
    
    members = get_member_list()
    
    return render_template('auth/member.html', members=members)

@bp.route('/member/<int:member_id>')
@login_required
def member_detail(member_id):
    """
    定义会员个人主页，登录后的会员可以访问。
    展示会员个人主页：
    1. 显示会员名、头像
    2. 入队时间
    3. 荣誉List
    4. 社交帐号List，当前只收录：
        - 微信
        - QQ
        - 微博
        - 知乎
        - 抖音
    """
    member = User.query.filter_by(id=member_id).first()
    if not member:
        flash('会员不存在', 'error')
        return redirect(url_for('auth.member'))
    
    return render_template('auth/member_detail.html', member=member)


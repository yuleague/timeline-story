# app/models/user.py
"""
    会员模型说明：
    1. 会员注册必须是通过白名单验证，白名单由管理员维护。
    2. 会员角色分为管理员和普通会员：
        - 管理员可以管理会员：删除、冻结、恢复、查看会员注册资料。
        - 普通会员可查看其它member_detail，可修改自己的Profile。
    3. 会员的验证字段为mobile，即手机号码。
    4. 增加一个预设校验字段(6位数字)，由会员注册自己填写，用于在恢复密码时验证身份。
       加一段说明："预设码为忘记密码时验证用，请填写一个你易记的6位数字，不要与支付密码相同。"
    5. email字段可以为空，但mobile字段不能为空。
    6. "加入年" 字段，这代表了会员在这个团队中的辈份。限制为表示年份的4位数字，并限制在1987-2015之间。
    7. 社交帐号字段为数组，当前只收录：微信、微博、QQ、抖音、哔哩哔哩、Telegram、E-mail。
    8. 荣誉：为外链字段，单独存储在honors表中。
       Honors表结构：
       id = db.Column(db.Integer, primary_key=True)
       year = db.Column(db.Integer, nullable=False)
       month = db.Column(db.Integer, nullable=True)
       # 团体荣誉为数组，包含：荣誉名称、团队成员、荣誉图片URL
       team = 请AI协助生成
       # 个人荣誉为数组，包含：荣誉名称、荣誉图片URL
       person = 请AI协助生成
       # 如何为荣誉创建关联关系？请AI协助生成
    9. 为以后的内部论坛开发留下接口：关注、赞、收藏、评论、私信、回复
    10. Avatar字段为头像图片的URL，头像图片存储在本地目录/static/images/avatar/目录中。
        Avatar的上传、压缩、存储、修改等操作由utils/avatar.py实现，
        初始默认为：/static/images/avatar/default.png。
"""
from app.extensions.postgres import db
from flask_login import UserMixin
from datetime import datetime
import json

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    mobile = db.Column(db.String(20), unique=True, nullable=False)  # 手机号码，唯一且不能为空
    email = db.Column(db.String(120), unique=True, nullable=True)    # 邮箱，可以为空
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    preset_code = db.Column(db.String(6))  # 6位预设校验码
    join_year = db.Column(db.Integer)       # 加入年，1987-2015之间
    avatar_url = db.Column(db.String(500), default='/static/images/avatar/default.png')
    role = db.Column(db.String(20), default='member')  # admin, member, visitor
    is_active = db.Column(db.Boolean, default=True)
    is_frozen = db.Column(db.Boolean, default=False)   # 是否被冻结
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # 社交账号（PostgreSQL JSONB类型存储数组）
    social_accounts = db.Column(db.JSON, default=list)
    
    # 论坛相关字段（预留接口）
    followers_count = db.Column(db.Integer, default=0)
    following_count = db.Column(db.Integer, default=0)
    posts_count = db.Column(db.Integer, default=0)
    likes_count = db.Column(db.Integer, default=0)
    comments_count = db.Column(db.Integer, default=0)
    
    # 关系
    honors = db.relationship('UserHonor', back_populates='user')
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', back_populates='sender')
    received_messages = db.relationship('Message', foreign_keys='Message.receiver_id', back_populates='receiver')
    likes = db.relationship('Like', back_populates='user')
    comments = db.relationship('Comment', back_populates='user')
    bookmarks = db.relationship('Bookmark', back_populates='user')
    
    # 关注关系（多对多）
    following = db.relationship(
        'User',
        secondary='follows',
        primaryjoin='User.id==follows.c.follower_id',
        secondaryjoin='User.id==follows.c.followed_id',
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 初始化社交账号结构
        if not self.social_accounts:
            self.social_accounts = self.default_social_accounts()
    
    def default_social_accounts(self):
        """默认社交账号结构"""
        return [
            {"platform": "微信", "account": "", "visible": True},
            {"platform": "微博", "account": "", "visible": True},
            {"platform": "QQ", "account": "", "visible": True},
            {"platform": "抖音", "account": "", "visible": False},
            {"platform": "哔哩哔哩", "account": "", "visible": False},
            {"platform": "Telegram", "account": "", "visible": False},
            {"platform": "E-mail", "account": "", "visible": True}
        ]
    
    def get_social_account(self, platform):
        """获取指定平台的社交账号"""
        for account in self.social_accounts:
            if account.get('platform') == platform:
                return account.get('account', '')
        return ''
    
    def set_social_account(self, platform, account, visible=True):
        """设置指定平台的社交账号"""
        for i, acc in enumerate(self.social_accounts):
            if acc.get('platform') == platform:
                self.social_accounts[i] = {"platform": platform, "account": account, "visible": visible}
                return
        
        # 如果平台不存在，添加新的
        self.social_accounts.append({"platform": platform, "account": account, "visible": visible})
    
    def get_visible_social_accounts(self):
        """获取可见的社交账号"""
        return [acc for acc in self.social_accounts if acc.get('visible', False)]
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_member(self):
        return self.role == 'member'
    
    def is_active_member(self):
        return self.role == 'member' and self.is_active and not self.is_frozen
    
    def can_view_profile(self, other_user):
        """判断是否可以查看其他用户的资料"""
        if self.is_admin():
            return True
        if self.id == other_user.id:
            return True
        if self.is_member() and other_user.is_member():
            return True
        return False
    
    def to_dict(self, include_private=False):
        """转换为字典，用于API响应"""
        data = {
            'id': self.id,
            'username': self.username,
            'avatar_url': self.avatar_url,
            'join_year': self.join_year,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'stats': {
                'followers': self.followers_count,
                'following': self.following_count,
                'posts': self.posts_count
            }
        }
        
        if include_private:
            data.update({
                'mobile': self.mobile if self.can_view_profile(self) else None,
                'email': self.email,
                'social_accounts': self.get_visible_social_accounts(),
                'is_active': self.is_active,
                'is_frozen': self.is_frozen
            })
        
        return data
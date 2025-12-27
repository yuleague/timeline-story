from app.extensions.postgres import db
from datetime import datetime
import json

class Honor(db.Model):
    __tablename__ = 'honors'
    
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)  # 荣誉年份
    month = db.Column(db.Integer, nullable=True)  # 荣誉月份（可选）
    title = db.Column(db.String(200), nullable=False)  # 荣誉标题
    description = db.Column(db.Text)  # 荣誉描述
    type = db.Column(db.String(20), nullable=False)  # team（团体）或 person（个人）
    
    # 团体荣誉结构
    team_info = db.Column(db.JSON, default=dict)  # 存储团体荣誉信息
    
    # 个人荣誉结构
    person_info = db.Column(db.JSON, default=dict)  # 存储个人荣誉信息
    
    # 荣誉图片
    image_url = db.Column(db.String(500))
    thumbnail_url = db.Column(db.String(500))
    
    # 分类标签
    tags = db.Column(db.JSON, default=list)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # 关系
    users = db.relationship('UserHonor', back_populates='honor')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 初始化团队荣誉和个人荣誉的默认结构
        if self.type == 'team' and not self.team_info:
            self.team_info = self.default_team_info()
        elif self.type == 'person' and not self.person_info:
            self.person_info = self.default_person_info()
    
    def default_team_info(self):
        """默认团队荣誉结构"""
        return {
            "team_name": "",
            "members": [],  # 成员列表 [{"user_id": 1, "name": "张三", "role": "队长"}]
            "competition": "",  # 比赛/活动名称
            "level": "",  # 级别（国际/国家/省级/市级）
            "rank": "",   # 名次（冠军/亚军/季军）
            "details": {}  # 其他详细信息
        }
    
    def default_person_info(self):
        """默认个人荣誉结构"""
        return {
            "category": "",  # 类别（学术/体育/艺术等）
            "level": "",     # 级别
            "organization": "",  # 颁发机构
            "details": {}  # 其他详细信息
        }
    
    def to_dict(self):
        """转换为字典"""
        data = {
            'id': self.id,
            'year': self.year,
            'month': self.month,
            'title': self.title,
            'description': self.description,
            'type': self.type,
            'image_url': self.image_url,
            'thumbnail_url': self.thumbnail_url,
            'tags': self.tags,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if self.type == 'team':
            data['team_info'] = self.team_info
        elif self.type == 'person':
            data['person_info'] = self.person_info
        
        return data

class UserHonor(db.Model):
    """用户和荣誉的多对多关联表"""
    __tablename__ = 'user_honors'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    honor_id = db.Column(db.Integer, db.ForeignKey('honors.id'), nullable=False)
    
    # 额外信息
    user_role = db.Column(db.String(50))  # 用户在荣誉中的角色（队长/成员/获奖者等）
    contribution = db.Column(db.Text)     # 贡献描述
    is_primary = db.Column(db.Boolean, default=False)  # 是否主要获奖者
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    user = db.relationship('User', back_populates='honors')
    honor = db.relationship('Honor', back_populates='users')
    
    # 唯一约束
    __table_args__ = (
        db.UniqueConstraint('user_id', 'honor_id', name='unique_user_honor'),
    )

# 关注关系表（多对多）
class Follow(db.Model):
    __tablename__ = 'follows'
    
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
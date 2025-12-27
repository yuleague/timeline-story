# app/models/events.py
"""
TimelineJS Postgres 数据模型
"""

from app.extensions.postgres import db
from datetime import datetime

class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(100), unique=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    display_date = db.Column(db.String(200))
    headline = db.Column(db.Text)
    text = db.Column(db.Text)
    media_url = db.Column(db.String(500))
    media_caption = db.Column(db.Text)
    media_credit = db.Column(db.String(200))
    group = db.Column(db.String(100))
    background_url = db.Column(db.String(500))
    background_color = db.Column(db.String(50))
    autolink = db.Column(db.Boolean, default=True)
    is_published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
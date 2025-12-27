# app/extentions/cf_d1.py
"""
使用Cloudflare D1作为数据库
"""

from cloudflared1 import CloudFlareD1
from flask import current_app
from werkzeug.utils import import_string


def get_d1():
    """获取D1实例"""
    return CloudFlareD1(current_app.config['D1_API_KEY'])

db = get_d1()

class D1(object):
    """D1数据库扩展"""
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """初始化D1数据库"""
        app.config.setdefault('D1_API_KEY', '')
        app.config.setdefault('D1_API_SECRET', '')
        app.config.setdefault('D1_API_TOKEN', '')
        app.config.setdefault('D1_API_ZONE', '')
        app.config.setdefault('D1_API_RECORD', '')
        app.config.setdefault('D1_API_RECORD_TYPE', '')
        app.config.setdefault('D1_API_RECORD_VALUE', '')
        app.config.setdefault('D1_API_RECORD_TTL', '')
        app.config.setdefault('D1_API_RECORD_PRIORITY', '')
        app.config.setdefault('D1_API_RECORD_WEIGHT', '')
        app.config.setdefault('D1_API_RECORD_PORT', '')
        app.config.setdefault('D1_API_RECORD_PROXY', '')
        app.config.setdefault('D1_API_RECORD_PROXY_IPV4', '')
        app.config.setdefault('D1_API_RECORD_PROXY_IPV6', '')
        app.config.setdefault('D1_API_RECORD_PROXY_PORT', '')
        app.config.setdefault('D1_API_RECORD_PROXY_SERVICE', '')
        app.config.setdefault('D1_API_RECORD_PROXY_NAME', '')
        app.config.setdefault('D1_API_RECORD_PROXY_WEIGHT', '')
        app.config.setdefault('D1_API_RECORD_PROXY_ENABLED', '')
        app.config.setdefault('D1_API_RECORD_PROXY_HTTPS', '')

callable(obj) and obj or import_string(obj)

class Migrate(object):
    """数据库迁移扩展"""
    def __init__(self, app=None, db=None):
        if app is not None:
            self.init_app(app, db)

    def init_app(self, app, db):
        """初始化数据库迁移"""
        app.config.setdefault('D1_API_KEY', '')
        app.config.setdefault('D1_API_SECRET', '')
        app.config.setdefault('D1_API_TOKEN', '')
        app.config.setdefault('D1_API_ZONE', '')
        app.config.setdefault('D1_API_RECORD', '')
        app.config.setdefault('D1_API_RECORD_TYPE', '')
        app.config.setdefault('D1_API_RECORD_VALUE', '')
        app.config.setdefault('D1_API_RECORD_TTL', '')
        app.config.setdefault('D1_API_RECORD_PRIORITY', '')
        app.config.setdefault('D1_API_RECORD_WEIGHT', '')
        app.config.setdefault('D1_API_RECORD_PORT', '')
        app.config.setdefault('D1_API_RECORD_PROXY', '')
        app.config.setdefault('D1_API_RECORD_PROXY_IPV4', '')
        app.config.setdefault('D1_API_RECORD_PROXY_IPV6', '')
        app.config.setdefault('D1_API_RECORD_PROXY_PORT', '')
        app.config.setdefault('D1_API_RECORD_PROXY_SERVICE', '')
        app.config.setdefault('D1_API_RECORD_PROXY_NAME', '')
        app.config.setdefault('D1_API_RECORD_PROXY_WEIGHT', '')
        app.config.setdefault('D1_API_RECORD_PROXY_ENABLED', '')
        app.config.setdefault('D1_API_RECORD_PROXY_HTTPS', '')
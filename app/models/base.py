# app/models/base.py

from app.extentions.cf_d1 import db

class Base(db.Model):
    __abstract__ = True
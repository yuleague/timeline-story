# app/routes/home.py
from flask import Blueprint, render_template
from datetime import datetime

bp = Blueprint('/', __name__)

@bp.route('/')
def home():
    return render_template('index.html')
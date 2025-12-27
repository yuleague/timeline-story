from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from app.extensions.postgres import db
from app.models.event import Event
from app.models.user import User
from app.models.whitelist import Whitelist
from app.utils.postgres_to_json import generate_timeline_json
from datetime import datetime

bp = Blueprint('admin', __name__)

@bp.before_request
@login_required
def require_admin():
    if not current_user.is_admin():
        return redirect(url_for('main.index'))

@bp.route('/dashboard')
def dashboard():
    stats = {
        'total_events': Event.query.count(),
        'total_users': User.query.count(),
        'total_members': User.query.filter_by(role='member').count(),
        'pending_whitelist': Whitelist.query.filter_by(status='pending').count()
    }
    return render_template('admin/dashboard.html', stats=stats)

@bp.route('/events')
def events():
    events_list = Event.query.order_by(Event.created_at.desc()).all()
    return render_template('admin/events.html', events=events_list)

@bp.route('/events/create', methods=['POST'])
def create_event():
    data = request.get_json()
    
    event = Event(
        unique_id=data.get('unique_id'),
        start_date=datetime.strptime(data['start_date'], '%Y-%m-%d'),
        headline=data['headline'],
        text=data.get('text'),
        media_url=data.get('media_url'),
        group=data.get('group'),
        user_id=current_user.id
    )
    
    db.session.add(event)
    db.session.commit()
    
    # Regenerate JSON
    generate_timeline_json()
    
    return jsonify({'success': True, 'id': event.id})

@bp.route('/whitelist')
def whitelist():
    entries = Whitelist.query.order_by(Whitelist.created_at.desc()).all()
    return render_template('admin/whitelist.html', entries=entries)

@bp.route('/users')
def users():
    users_list = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users_list)
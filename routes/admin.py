from flask import Blueprint, redirect, render_template, session, url_for, request
import dbfunc
from functools import wraps

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        if session.get('user_role') == 'admin':
            return f(*args, **kwargs)
        if dbfunc.isUserAdmin(session.get('user_id')):
            session['user_role'] = 'admin'
            return f(*args, **kwargs)
        return redirect(url_for('main.home'))
    return decorated_function

@admin_bp.route('/admin')
@admin_required
def admin_dashboard():
    users = dbfunc.getAllUsers()
    events = dbfunc.getAllEvents()
    return render_template('admin_dashboard.html', users=users, events=events)

@admin_bp.route('/admin/users', methods=['GET'])
@admin_required
def admin_users():
    users = dbfunc.getAllUsers()
    return render_template('admin_users.html', users=users)

@admin_bp.route('/admin/users/create', methods=['POST'])
@admin_required
def admin_create_user():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role', 'user')
    
    if not username or not email or not password:
        return redirect(url_for('admin.admin_users'))
    dbfunc.createUser(username, email, password, user_role=role)
    return redirect(url_for('admin.admin_users'))

@admin_bp.route('/admin/users/update/<int:user_id>', methods=['POST'])
@admin_required
def admin_update_user(user_id):
    username = request.form.get('username')
    email = request.form.get('email')
    phone = request.form.get('phone')
    dob = request.form.get('dob')
    role = request.form.get('role')
    dbfunc.updateUser(user_id, username=username, email=email, phone=phone, dob=dob, user_role=role)
    return redirect(url_for('admin.admin_users'))

@admin_bp.route('/admin/users/delete/<int:user_id>', methods=['POST'])
@admin_required
def admin_delete_user(user_id):
    dbfunc.deleteUser(user_id)
    return redirect(url_for('admin.admin_users'))

@admin_bp.route('/admin/events', methods=['GET'])
@admin_required
def admin_events():
    events = dbfunc.getAllEvents()
    event_types = dbfunc.getEventTypes()
    venues = dbfunc.getVenues()
    return render_template('admin_events.html', events=events, event_types=event_types, venues=venues)

@admin_bp.route('/admin/events/create', methods=['POST'])
@admin_required
def admin_create_event():
    name = request.form.get('event_name')
    date = request.form.get('event_date')
    price = request.form.get('event_price')
    capacity = request.form.get('event_capacity')
    eventType_id = request.form.get('eventType_id')
    venue_id = request.form.get('venue_id')
    desc = request.form.get('event_custom_description')
    dbfunc.createEvent(name, date, price, capacity, eventType_id, venue_id, event_custom_description=desc)
    return redirect(url_for('admin.admin_events'))

@admin_bp.route('/admin/events/delete/<int:event_id>', methods=['POST'])
@admin_required
def admin_delete_event(event_id):
    dbfunc.deleteEvent(event_id)
    return redirect(url_for('admin.admin_events'))
from flask import Blueprint, redirect, render_template, session, url_for, request
import dbfunc

main_bp = Blueprint('main', __name__)

@main_bp.route('/debug')
def debug():
    return str(session)

@main_bp.route('/')
@main_bp.route('/index')
def home():
    return render_template('index.html')

@main_bp.route('/aboutus')
def about():
    return render_template('aboutUs.html')

@main_bp.route('/account', methods=['GET', 'POST'])
def account():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')
        dob = request.form.get('dob')

        dbfunc.updateUserProfile(user_id, username, email, phone, dob)

    user = dbfunc.getUserById(user_id)
    bookings = dbfunc.getUserBookings(user_id)

    return render_template('account.html', user=user, bookings=bookings)

@main_bp.route('/credits')
def credits():
    venues = dbfunc.getVenues()
    return render_template('credits.html', venues=venues)

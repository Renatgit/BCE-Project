from flask import Blueprint, redirect, render_template, session, url_for, jsonify, request
from werkzeug.security import check_password_hash
import dbfunc

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_input = request.form.get('login')
        password = request.form.get('password')

        user = dbfunc.getUserByLogin(login_input)

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['user_id']
            session['user_name'] = user['user_name']
            session['user_role'] = user.get('user_role', 'user') if user.get('user_role') else 'user'
            return redirect(url_for('main.home'))
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            return render_template('signUp.html', error='Passwords do not match')

        if dbfunc.emailExists(email):
            return render_template('signUp.html', error='Email already exists')

        if dbfunc.usernameExists(username):
            return render_template('signUp.html', error='Username already taken')

        dbfunc.createUser(username, email, password)
        return redirect(url_for('auth.login'))

    return render_template('signUp.html')

@auth_bp.route('/check_user')
def check_user():
    email = request.args.get('email')
    username = request.args.get('username')

    response = {}

    if email:
        response['emailExists'] = dbfunc.emailExists(email)

    if username:
        response['usernameExists'] = dbfunc.usernameExists(username)

    return jsonify(response)

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.home'))

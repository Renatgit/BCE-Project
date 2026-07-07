# Student ID: 25060488
# Name: Renat Bershadskyi
from flask import Flask
from config import SECRET_KEY
from routes.auth import auth_bp
from routes.events import events_bp
from routes.bookings import bookings_bp
from routes.main import main_bp
from routes.admin import admin_bp

app = Flask(__name__)
app.secret_key = SECRET_KEY

app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(events_bp)
app.register_blueprint(bookings_bp)
app.register_blueprint(admin_bp)

if __name__ == '__main__':
    for i in range(10000, 18000):
        try:
            app.run(debug=True, port=i)
            break
        except OSError:
            continue

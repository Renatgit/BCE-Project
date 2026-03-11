from flask import Flask, render_template
import dbfunc

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def home():
    return render_template("index.html")

@app.route("/events")
def events():
    events = dbfunc.getAllEvents()
    return render_template(
        "events.html",
        events=events
    )

@app.route("/event/<int:event_id>")
def event(event_id):
    event = dbfunc.getEventById(event_id)
    if event is None:
        return "Event not found", 404

    return render_template("event.html", event=event)

@app.route("/aboutus")
def about():
    return render_template("aboutUs.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signUp.html")

@app.route("/account")
def account():
    return render_template("account.html")

if __name__ == '__main__':
    for i in range(10000, 18000):
        try:
            app.run(debug = True, port = i)
            break
        except OSError as e:
            print("Port {i} not available".format(i))
from flask import Flask, redirect, render_template, session, url_for, jsonify, request  #request allows Flask to read query parameters from the URL
from werkzeug.security import check_password_hash
import dbfunc
import secrets
from datetime import datetime, timedelta

app = Flask(__name__)
#app.secret_key = secrets.token_hex(32)
app.secret_key = '^xHM$[5A1!vxS><9GTuzif|S;,&$=m0S'

@app.route("/debug")
def debug():
    return str(session)

@app.route("/")
@app.route("/index")
def home():
    return render_template("index.html")

@app.route("/events")
def events():
    # Filtering / sorting parameters come from query string
    event_type = request.args.get("event_type")
    venue_id = request.args.get("venue_id")
    sort_option = request.args.get("sort_option")
    sort_by = request.args.get("sort_by", "date")
    sort_dir = request.args.get("sort_dir", "asc")
    search = request.args.get("q")

    # Support a combined sort option like date_asc, venue_desc for simpler UI
    if sort_option:
        parts = sort_option.split("_")
        if len(parts) == 2:
            sort_by, sort_dir = parts[0], parts[1]

    # Convert numeric IDs 
    try:
        event_type = int(event_type) if event_type else None
    except ValueError:
        event_type = None

    try:
        venue_id = int(venue_id) if venue_id else None
    except ValueError:
        venue_id = None

    events = dbfunc.getAllEvents(
        event_type_id=event_type,
        venue_id=venue_id,
        sort_by=sort_by,
        sort_dir=sort_dir,
        search=search,
    )

    event_types = dbfunc.getEventTypes()
    venues = dbfunc.getVenues()

    # Keep the sort option string for template convenience
    selected_sort_option = f"{sort_by}_{sort_dir}"

    # Resolve selected names so template doesn't need filters
    selected_event_type_name = None
    if event_type and event_types:
        for et in event_types:
            if et.get("eventType_id") == event_type:
                selected_event_type_name = et.get("event_name")
                break

    selected_venue_name = None
    if venue_id and venues:
        for v in venues:
            if v.get("venue_id") == venue_id:
                selected_venue_name = v.get("venue_name")
                break

    sort_labels = {
        "date_asc": "Date (closest first)",
        "date_desc": "Date (furthest first)",
        "venue_asc": "Venue (A–Z)",
        "venue_desc": "Venue (Z–A)",
    }
    selected_sort_label = sort_labels.get(selected_sort_option, "Date (closest first)")

    return render_template(
        "events.html",
        events=events,
        event_types=event_types,
        venues=venues,
        selected_event_type=event_type,
        selected_venue=venue_id,
        selected_event_type_name=selected_event_type_name,
        selected_venue_name=selected_venue_name,
        selected_sort_by=sort_by,
        selected_sort_dir=sort_dir,
        selected_sort_option=selected_sort_option,
        selected_sort_label=selected_sort_label,
        search=search,
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

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login_input = request.form.get("login")
        password = request.form.get("password")

        user = dbfunc.getUserByLogin(login_input)

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["user_id"]
            session["user_name"] = user["user_name"]

            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Password match
        if password != confirm_password:
            return render_template("signUp.html", error="Passwords do not match")

        # Email exists check
        if dbfunc.emailExists(email):
            return render_template("signUp.html", error="Email already exists")

        # Username exists check
        if dbfunc.usernameExists(username):
            return render_template("signUp.html", error="Username already taken")

        # Create user
        dbfunc.createUser(username, email, password)

        return redirect(url_for("login"))

    return render_template("signUp.html")

@app.route("/check_user")
def check_user():
    email = request.args.get("email")
    username = request.args.get("username")

    response = {}

    if email:
        response["emailExists"] = dbfunc.emailExists(email)

    if username:
        response["usernameExists"] = dbfunc.usernameExists(username)

    return jsonify(response)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))  # or index

@app.route("/account", methods=["GET", "POST"])
def account():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        phone = request.form.get("phone")
        dob = request.form.get("dob")

        dbfunc.updateUserProfile(user_id, username, email, phone, dob)

    user = dbfunc.getUserById(user_id)
    bookings = dbfunc.getUserBookings(user_id)

    return render_template("account.html", user=user, bookings=bookings)

@app.route("/cancel_booking/<int:enrol_id>", methods=["POST"])
def cancel_booking(enrol_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    success = dbfunc.cancelBooking(enrol_id)
    
    if not success:
        # If cancellation failed, redirect back to account with an error message
        return redirect(url_for("account"))
    
    return redirect(url_for("account"))

@app.route("/update_profile", methods=["POST"])
def update_profile():
    if "user_id" not in session:
        return jsonify({"success": False})

    user_id = session["user_id"]

    field = request.json.get("field")
    value = request.json.get("value")

    allowed_fields = ["user_name", "user_email", "user_phoneNo", "user_dob"]

    if field not in allowed_fields:
        return jsonify({"success": False})
    
    dbfunc.updateSingleField(user_id, field, value)

    if field == "user_name":
        session["user_name"] = value
    return jsonify({"success": True})

@app.route("/booking/<int:event_id>", methods=["GET", "POST"])
def booking(event_id):
    # Check if user is logged in
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    user_id = session["user_id"]
    user = dbfunc.getUserById(user_id)
    event = dbfunc.getEventById(event_id)
    
    if event is None:
        return "Event not found", 404
    
    event_date = event["event_date"]
    if isinstance(event_date, str):
        event_date = datetime.strptime(event_date, '%d/%m/%Y %H:%M')

    days_until_event = (event_date - datetime.now()).days

    discount = dbfunc.getApplicableDiscount(days_until_event)
    discount_percent = discount["discount_percentage"] if discount else 0

    original_price = float(event["event_price"])
    final_price = original_price * (1 - discount_percent / 100)

    if request.method == "POST":
        try:
            ticket_quantity = int(request.form.get("ticket_quantity", 1))
            
            # Validate ticket quantity
            if ticket_quantity < 1 or ticket_quantity > 6:
                return render_template("booking.html", event=event, user=user, error="Please select between 1 and 6 tickets", original_price=original_price, final_price=final_price, discount_percent=discount_percent)
            
            # Check if the booking is not more than 2 month in advance
            event_date = event["event_date"]
            if isinstance(event_date, str):
                event_date = datetime.strptime(event_date, '%d/%m/%Y %H:%M')

            if event_date > datetime.now() + timedelta(days=60):
                return render_template (
                    "booking.html",
                    event=event,
                    user=user,
                    error="You can only book events within 2 months",
                    original_price=original_price,
                    final_price=final_price,
                    discount_percent=discount_percent
                )
            # Check if the there are enough tickets
            booked = dbfunc.getBookedTickets(event_id)
            capacity = event["event_capacity"]
            if booked + ticket_quantity > capacity:
                return render_template(
                    "booking.html",
                    event=event,
                    user=user,
                    error="Not enough tickets available",
                    original_price=original_price,
                    final_price=final_price,
                    discount_percent=discount_percent
                )
            
            # Check if user has already booked this event
            if dbfunc.hasUserBookedEvent(user_id, event_id):
                return render_template(
                    "booking.html",
                    event=event,
                    user=user,
                    error="You have already booked this event",
                    original_price=original_price,
                    final_price=final_price,
                    discount_percent=discount_percent
                )
            
            total_price = final_price * ticket_quantity

            # Create the booking
            dbfunc.createBooking(user_id, event_id, ticket_quantity, total_price)
            return redirect(url_for("account"))
        except ValueError:
            return render_template("booking.html", event=event, user=user, error="Invalid ticket quantity", original_price=original_price, final_price=final_price, discount_percent=discount_percent)
    
    return render_template(
        "booking.html",
        event=event,
        user=user,
        original_price=original_price,
        final_price=final_price,
        discount_percent=discount_percent
    )

@app.route("/credits")
def credits():
    venues = dbfunc.getVenues()
    return render_template("credits.html", venues=venues)

if __name__ == '__main__':
    for i in range(10000, 18000):
        try:
            app.run(debug = True, port = i)
            break
        except OSError as e:
            print("Port {i} not available".format(i))
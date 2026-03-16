from flask import Flask, render_template, request #request allows Flask to read query parameters from the URL
import dbfunc

app = Flask(__name__)

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
import mysql.connector
from mysql.connector import errorcode
import datetime

hostname = "localhost"
username = "renat2bershadskyi"
passwd = "Ret_tein3011"
db = "renat2bershadskyi_prj"


def format_datetime_uk(dt):
    #Format a datetime as DD/MM/YYYY HH:MM (UK format)
    if dt is None:
        return ""

    if isinstance(dt, str):
        try:
            dt = datetime.datetime.fromisoformat(dt)
        except ValueError:
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
                try:
                    # datetime.datetime.strptime(date, format)
                    # Converts a string(passed from DB) into 
                    # a datetime object by matching it against a format pattern
                    dt = datetime.datetime.strptime(dt, fmt)
                    break
                except ValueError:
                    continue
            else:
                return dt

    # If date only (no time), coerce to datetime for formatting
    if isinstance(dt, datetime.date) and not isinstance(dt, datetime.datetime):
        dt = datetime.datetime(dt.year, dt.month, dt.day)

    return dt.strftime("%d/%m/%Y %H:%M")

def getConnection():
    try:
        conn = mysql.connector.connect(
            host=hostname,
            user=username,
            password=passwd,
            database=db
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('User name or Password is not working')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('Database does not exist')
        else:
            print(err)
    else:
        return conn

def getAllEvents(event_type_id=None, venue_id=None, sort_by="date", sort_dir="asc", search=None):
    conn = getConnection()

    if conn is None:
        print("Unable to establish database connection.")
        return []
    
    cur = conn.cursor(dictionary=True)

    # Build the query dynamically based on supplied filters.
    query = """
        SELECT 
            e.event_id,
            e.event_name,
            et.eventType_name AS event_type_name,
            COALESCE(e.event_custom_description, et.event_description) AS event_description,
            e.event_date,
            v.venue_name,
            v.venue_imgPath
        FROM Event e
        JOIN EventType et ON e.eventType_id = et.eventType_id
        JOIN Venue v ON e.venue_id = v.venue_id
    """

    where_clauses = []
    params = []

    if event_type_id:
        where_clauses.append("e.eventType_id = %s")
        params.append(event_type_id)

    if venue_id:
        where_clauses.append("e.venue_id = %s")
        params.append(venue_id)

    if search:
        # Search in event type, description, and venue name.
        search_term = f"%{search}%"
        where_clauses.append(
            "(e.event_name LIKE %s OR et.eventType_name LIKE %s OR e.event_custom_description LIKE %s OR et.event_description LIKE %s OR v.venue_name LIKE %s)"
        )
        params.extend([search_term] * 5)

    if where_clauses:
        query += "\n        WHERE " + " AND ".join(where_clauses)

    # Sorting options
    sort_map = {
        "date": "e.event_date",
        "venue": "v.venue_name",
        "event": "e.event_name",
    }

    order_column = sort_map.get(sort_by, "e.event_date")
    sort_dir = sort_dir.lower()
    if sort_dir not in ("asc", "desc"):
        sort_dir = "asc"

    query += f"\n        ORDER BY {order_column} {sort_dir.upper()};"

    cur.execute(query, params)
    events = cur.fetchall()

    # Format dates for display (UK style, without seconds)
    for e in events:
        if "event_date" in e:
            e["event_date"] = format_datetime_uk(e["event_date"])

    cur.close()
    conn.close()

    return events


def getEventTypes():
    conn = getConnection()

    if conn is None:
        print("Unable to establish database connection.")
        return []

    cur = conn.cursor(dictionary=True)
    query = """
        SELECT eventType_id, eventType_name AS event_name
        FROM EventType
        ORDER BY eventType_name ASC;
    """

    cur.execute(query)
    types = cur.fetchall()

    cur.close()
    conn.close()

    return types


def getVenues():
    conn = getConnection()

    if conn is None:
        print("Unable to establish database connection.")
        return []

    cur = conn.cursor(dictionary=True)
    query = """
        SELECT venue_id, venue_name
        FROM Venue
        ORDER BY venue_name ASC;
    """

    cur.execute(query)
    venues = cur.fetchall()

    cur.close()
    conn.close()

    return venues

def getEventById(event_id):

    conn = getConnection()
    cur = conn.cursor(dictionary=True)
    if conn is None:
        print("Unable to establish database connection.")
        return []
    
    query = """
        SELECT
            e.event_id,
            e.event_name,
            et.eventType_name AS event_type_name,
            COALESCE(e.event_custom_description, et.event_description) AS description,
            v.venue_name,
            v.venue_imgPath,
            v.venue_location,
            e.event_date,
            e.event_price
        FROM Event e
        JOIN EventType et ON e.eventType_id = et.eventType_id
        JOIN Venue v ON e.venue_id = v.venue_id
        WHERE e.event_id = %s
    """

    cur.execute(query, (event_id,))
    event = cur.fetchone()

    if event and "event_date" in event:
        event["event_date"] = format_datetime_uk(event["event_date"])

    cur.close()
    conn.close()

    return event
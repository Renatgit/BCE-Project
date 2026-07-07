# Student ID: 25060488
# Name: Renat Bershadskyi
import mysql.connector
from mysql.connector import errorcode
import datetime
from werkzeug.security import generate_password_hash

hostname = "localhost"
username = "renat2bershadskyi"
passwd = "Ret_tein3011"
db = "renat2bershadskyi_prj"

def emailExists(email):
    conn = getConnection()
    cur = conn.cursor()
    query  = "SELECT user_id FROM User WHERE user_email = %s"
    cur.execute(query, (email,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result is not None

def usernameExists(username):
    conn = getConnection()
    cur = conn.cursor()
    query = "SELECT user_id FROM User WHERE user_name = %s"
    cur.execute(query, (username,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result is not None

def createUser(username, email, password, phone=None, dob=None, is_student=0, user_role='user'):
    conn = getConnection()
    cur = conn.cursor()
    hashed_password = generate_password_hash(password)
    query = """
        INSERT INTO User 
        (user_name, user_email, password_hash, user_phoneNo, user_dob, is_student, is_deleted, user_role)
        VALUES (%s, %s, %s, %s, %s, %s, 0, %s)
    """
    cur.execute(query, (
        username,
        email,
        hashed_password,
        phone,
        dob,
        is_student,
        user_role
    ))
    conn.commit()
    cur.close()
    conn.close()

def getUserByLogin(login):
    conn = getConnection()
    cur = conn.cursor(dictionary=True)
    query = """
        SELECT * FROM User 
        WHERE user_email = %s OR user_name = %s
    """
    cur.execute(query, (login, login))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user

def getUserById(user_id):
    conn = getConnection()
    cur = conn.cursor(dictionary=True)
    query = "SELECT * FROM User WHERE user_id = %s"
    cur.execute(query, (user_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user

def updateSingleField(user_id, field, value):
    conn = getConnection()
    cur = conn.cursor()
    query = f"UPDATE User SET {field} = %s WHERE user_id = %s"
    cur.execute(query, (value, user_id))
    conn.commit()
    cur.close()
    conn.close()

def hasUserBookedEvent(user_id, event_id):
    conn = getConnection()
    cur = conn.cursor()
    query = "SELECT enrol_id FROM EventEnrol WHERE user_id = %s AND event_id = %s"
    cur.execute(query, (user_id, event_id))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result is not None

def createBooking(user_id, event_id, ticket_quantity, total_price):
    conn = getConnection()
    cur = conn.cursor()
    query = """
        INSERT INTO EventEnrol 
        (event_id, user_id, ticket_quantity, booking_status, total_price)
        VALUES (%s, %s, %s, 'confirmed', %s)
    """
    cur.execute(query, (event_id, user_id, ticket_quantity, total_price))
    conn.commit()
    cur.close()
    conn.close()
    return True

def getBookedTickets(event_id):
    conn = getConnection()
    cur = conn.cursor()
    query = """
        SELECT SUM(ticket_quantity)
        FROM EventEnrol
        WHERE event_id = %s
    """
    cur.execute(query, (event_id,))
    result = cur.fetchone()[0]
    cur.close()
    conn.close()
    return result if result else 0

def getApplicableDiscount(days_before):
    conn = getConnection()
    cur = conn.cursor(dictionary=True)
    query = """
        SELECT * FROM Discount
        WHERE min_days_before <= %s
        ORDER BY min_days_before DESC
        LIMIT 1
    """
    cur.execute(query, (days_before,))
    discount = cur.fetchone()
    cur.close()
    conn.close()
    return discount

def getUserBookings(user_id):
    conn = getConnection()
    cur = conn.cursor(dictionary=True)
    query = """
        SELECT 
            ee.enrol_id,
            ee.event_id,
            ee.ticket_quantity,
            ee.total_price,
            ee.booking_status,
            ee.booking_datetime,
            e.event_name,
            e.event_date,
            v.venue_name,
            v.venue_imgPath,
            et.eventType_name
        FROM EventEnrol ee
        JOIN Event e ON ee.event_id = e.event_id
        JOIN Venue v ON e.venue_id = v.venue_id
        JOIN EventType et ON e.eventType_id = et.eventType_id
        WHERE ee.user_id = %s
        ORDER BY e.event_date DESC
    """
    cur.execute(query, (user_id,))
    bookings = cur.fetchall()
    for booking in bookings:
        if "event_date" in booking:
            booking["event_date"] = format_datetime_uk(booking["event_date"])
    cur.close()
    conn.close()
    return bookings

def cancelBooking(enrol_id):
    conn = getConnection()
    cur = conn.cursor()
    try:
        query = "DELETE FROM EventEnrol WHERE enrol_id = %s"
        cur.execute(query, (enrol_id,))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Error cancelling booking: {e}")
        return False
    finally:
        cur.close()
        conn.close()

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
    query = """
        SELECT 
            e.event_id,
            e.event_name,
            et.eventType_name AS event_type_name,
            COALESCE(e.event_custom_description, et.event_description) AS event_description,
            e.event_date,
            v.venue_name,
            v.venue_imgPath,
            e.event_price,
            e.event_capacity
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
        search_term = f"%{search}%"
        where_clauses.append(
            "(e.event_name LIKE %s OR et.eventType_name LIKE %s OR e.event_custom_description LIKE %s OR et.event_description LIKE %s OR v.venue_name LIKE %s)"
        )
        params.extend([search_term] * 5)
    if where_clauses:
        query += "\n        WHERE " + " AND ".join(where_clauses)
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
        SELECT venue_id, venue_name, venue_img_credit_name AS credit_name, venue_img_credit_link AS credit_link
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
            e.event_price,
            e.event_capacity
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

def format_datetime_uk(dt):
    if dt is None:
        return ""
    if isinstance(dt, str):
        try:
            dt = datetime.datetime.fromisoformat(dt)
        except ValueError:
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
                try:
                    dt = datetime.datetime.strptime(dt, fmt)
                    break
                except ValueError:
                    continue
            else:
                return dt
    if isinstance(dt, datetime.date) and not isinstance(dt, datetime.datetime):
        dt = datetime.datetime(dt.year, dt.month, dt.day)
    return dt.strftime("%d/%m/%Y %H:%M")

# Admin/user/event management helpers

def updateUserProfile(user_id, username, email, phone=None, dob=None):
    conn = getConnection()
    cur = conn.cursor()
    query = "UPDATE User SET user_name = %s, user_email = %s, user_phoneNo = %s, user_dob = %s WHERE user_id = %s"
    cur.execute(query, (username, email, phone, dob, user_id))
    conn.commit()
    cur.close()
    conn.close()

def isUserAdmin(user_id):
    conn = getConnection()
    cur = conn.cursor()
    query = "SELECT user_role FROM User WHERE user_id = %s"
    cur.execute(query, (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        return False
    role = row[0] if isinstance(row, (list, tuple)) else row
    return role == 'admin'

def getAllUsers():
    conn = getConnection()
    cur = conn.cursor(dictionary=True)
    query = "SELECT user_id, user_name, user_email, user_phoneNo, user_dob, user_role FROM User WHERE is_deleted = 0 ORDER BY user_name ASC"
    cur.execute(query)
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users

def updateUser(user_id, username=None, email=None, phone=None, dob=None, user_role=None):
    conn = getConnection()
    cur = conn.cursor()
    fields = []
    params = []
    if username is not None:
        fields.append("user_name = %s"); params.append(username)
    if email is not None:
        fields.append("user_email = %s"); params.append(email)
    if phone is not None:
        fields.append("user_phoneNo = %s"); params.append(phone)
    if dob is not None:
        fields.append("user_dob = %s"); params.append(dob)
    if user_role is not None:
        fields.append("user_role = %s"); params.append(user_role)
    if not fields:
        cur.close(); conn.close(); return
    query = f"UPDATE User SET {', '.join(fields)} WHERE user_id = %s"
    params.append(user_id)
    cur.execute(query, tuple(params))
    conn.commit()
    cur.close()
    conn.close()

def deleteUser(user_id):
    conn = getConnection()
    cur = conn.cursor()
    query = "UPDATE User SET is_deleted = 1 WHERE user_id = %s"
    cur.execute(query, (user_id,))
    conn.commit()
    cur.close()
    conn.close()

def createEvent(event_name, event_date, event_price, event_capacity, eventType_id, venue_id, event_custom_description=None):
    conn = getConnection()
    cur = conn.cursor()
    query = """
        INSERT INTO Event (event_name, event_date, event_price, event_capacity, eventType_id, venue_id, event_custom_description)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cur.execute(query, (event_name, event_date, event_price, event_capacity, eventType_id, venue_id, event_custom_description))
    conn.commit()
    cur.close()
    conn.close()

def updateEvent(event_id, event_name=None, event_date=None, event_price=None, event_capacity=None, eventType_id=None, venue_id=None, event_custom_description=None):
    conn = getConnection()
    cur = conn.cursor()
    fields = []
    params = []
    if event_name is not None:
        fields.append("event_name = %s"); params.append(event_name)
    if event_date is not None:
        fields.append("event_date = %s"); params.append(event_date)
    if event_price is not None:
        fields.append("event_price = %s"); params.append(event_price)
    if event_capacity is not None:
        fields.append("event_capacity = %s"); params.append(event_capacity)
    if eventType_id is not None:
        fields.append("eventType_id = %s"); params.append(eventType_id)
    if venue_id is not None:
        fields.append("venue_id = %s"); params.append(venue_id)
    if event_custom_description is not None:
        fields.append("event_custom_description = %s"); params.append(event_custom_description)
    if not fields:
        cur.close(); conn.close(); return
    query = f"UPDATE Event SET {', '.join(fields)} WHERE event_id = %s"
    params.append(event_id)
    cur.execute(query, tuple(params))
    conn.commit()
    cur.close()
    conn.close()

def deleteEvent(event_id):
    conn = getConnection()
    cur = conn.cursor()
    query = "DELETE FROM Event WHERE event_id = %s"
    cur.execute(query, (event_id,))
    conn.commit()
    cur.close()
    conn.close()
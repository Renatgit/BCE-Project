import mysql.connector
from mysql.connector import errorcode

hostname = "localhost"
username = "renat2bershadskyi"
passwd = "Ret_tein3011"
db = "renat2bershadskyi_prj"

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

def getAllEvents():
    conn = getConnection()

    if conn is None:
        print("Unable to establish database connection.")
        return []
    
    # Dictionary means results will be returned in form -> "event_name": "Music Festival"
    # Instead of numeric indexes
    cur = conn.cursor(dictionary=True) 

    #COALESCE() uses first non null value 
    query = """
        SELECT 
            e.event_id,
            et.event_name,
            COALESCE(e.event_custom_description, et.event_description) AS event_description,
            e.event_date,
            v.venue_imgPath
        FROM Event e
        JOIN EventType et ON e.eventType_id = et.eventType_id
        JOIN Venue v ON e.venue_id = v.venue_id
        ORDER BY e.event_date ASC;
    """

    cur.execute(query)
    events = cur.fetchall()

    cur.close()
    conn.close()

    return events

def getEventById(event_id):

    conn = getConnection()
    cur = conn.cursor(dictionary=True)
    if conn is None:
        print("Unable to establish database connection.")
        return []
    
    query = """
        SELECT
            e.event_id,
            et.event_name,
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

    cur.close()
    conn.close()

    return event
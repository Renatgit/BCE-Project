# Student ID: 25060488
# Name: Renat Bershadskyi
from flask import Blueprint, render_template, request
import dbfunc

events_bp = Blueprint('events', __name__)

@events_bp.route('/events')
def events():
    event_type = request.args.get('event_type')
    venue_id = request.args.get('venue_id')
    sort_option = request.args.get('sort_option')
    sort_by = request.args.get('sort_by', 'date')
    sort_dir = request.args.get('sort_dir', 'asc')
    search = request.args.get('q')

    if sort_option:
        parts = sort_option.split('_')
        if len(parts) == 2:
            sort_by, sort_dir = parts[0], parts[1]

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

    selected_sort_option = f'{sort_by}_{sort_dir}'

    selected_event_type_name = None
    if event_type and event_types:
        for et in event_types:
            if et.get('eventType_id') == event_type:
                selected_event_type_name = et.get('event_name')
                break

    selected_venue_name = None
    if venue_id and venues:
        for v in venues:
            if v.get('venue_id') == venue_id:
                selected_venue_name = v.get('venue_name')
                break

    sort_labels = {
        'date_asc': 'Date (closest first)',
        'date_desc': 'Date (furthest first)',
        'venue_asc': 'Venue (A-Z)',
        'venue_desc': 'Venue (Z-A)',
    }
    selected_sort_label = sort_labels.get(selected_sort_option, 'Date (closest first)')

    return render_template(
        'events.html',
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

@events_bp.route('/event/<int:event_id>')
def event(event_id):
    event = dbfunc.getEventById(event_id)
    if event is None:
        return 'Event not found', 404

    return render_template('event.html', event=event)

from flask import Blueprint, redirect, render_template, session, url_for, jsonify, request
import dbfunc
from datetime import datetime, timedelta

bookings_bp = Blueprint('bookings', __name__)

@bookings_bp.route('/booking/<int:event_id>', methods=['GET', 'POST'])
def booking(event_id):
    if session.get('user_role') == 'admin':
        return redirect(url_for('admin.admin_dashboard'))

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    user = dbfunc.getUserById(user_id)
    event = dbfunc.getEventById(event_id)

    if event is None:
        return 'Event not found', 404

    event_date = event['event_date']
    if isinstance(event_date, str):
        event_date = datetime.strptime(event_date, '%d/%m/%Y %H:%M')

    days_until_event = (event_date - datetime.now()).days

    discount = dbfunc.getApplicableDiscount(days_until_event)
    discount_percent = discount['discount_percentage'] if discount else 0

    original_price = float(event['event_price'])
    final_price = original_price * (1 - discount_percent / 100)

    if request.method == 'POST':
        try:
            ticket_quantity = int(request.form.get('ticket_quantity', 1))

            if ticket_quantity < 1 or ticket_quantity > 6:
                return render_template('booking.html', event=event, user=user, error='Please select between 1 and 6 tickets', original_price=original_price, final_price=final_price, discount_percent=discount_percent)

            event_date = event['event_date']
            if isinstance(event_date, str):
                event_date = datetime.strptime(event_date, '%d/%m/%Y %H:%M')

            if event_date > datetime.now() + timedelta(days=60):
                return render_template(
                    'booking.html',
                    event=event,
                    user=user,
                    error='You can only book events within 2 months',
                    original_price=original_price,
                    final_price=final_price,
                    discount_percent=discount_percent
                )
            booked = dbfunc.getBookedTickets(event_id)
            capacity = event['event_capacity']
            if booked + ticket_quantity > capacity:
                return render_template(
                    'booking.html',
                    event=event,
                    user=user,
                    error='Not enough tickets available',
                    original_price=original_price,
                    final_price=final_price,
                    discount_percent=discount_percent
                )

            if dbfunc.hasUserBookedEvent(user_id, event_id):
                return render_template(
                    'booking.html',
                    event=event,
                    user=user,
                    error='You have already booked this event',
                    original_price=original_price,
                    final_price=final_price,
                    discount_percent=discount_percent
                )

            total_price = final_price * ticket_quantity

            dbfunc.createBooking(user_id, event_id, ticket_quantity, total_price)
            return redirect(url_for('main.account'))
        except ValueError:
            return render_template('booking.html', event=event, user=user, error='Invalid ticket quantity', original_price=original_price, final_price=final_price, discount_percent=discount_percent)

    return render_template(
        'booking.html',
        event=event,
        user=user,
        original_price=original_price,
        final_price=final_price,
        discount_percent=discount_percent
    )

@bookings_bp.route('/cancel_booking/<int:enrol_id>', methods=['POST'])
def cancel_booking(enrol_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    success = dbfunc.cancelBooking(enrol_id)

    if not success:
        return redirect(url_for('main.account'))

    return redirect(url_for('main.account'))

@bookings_bp.route('/update_profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return jsonify({'success': False})

    user_id = session['user_id']

    field = request.json.get('field')
    value = request.json.get('value')

    allowed_fields = ['user_name', 'user_email', 'user_phoneNo', 'user_dob']

    if field not in allowed_fields:
        return jsonify({'success': False})

    dbfunc.updateSingleField(user_id, field, value)

    if field == 'user_name':
        session['user_name'] = value
    return jsonify({'success': True})

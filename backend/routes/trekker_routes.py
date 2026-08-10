from flask import Blueprint, request, jsonify, current_app, send_file
from models.models import db, User, Trek, Booking
from flask_login import login_required, current_user
from datetime import date
import json
import os


trekker_bp = Blueprint('trekker', __name__)


# View open treks (with optional search/filter)
@trekker_bp.route('/api/trekker/treks', methods=['GET'])
@login_required
def view_treks():
    if current_user.role != 'trekker':
        return jsonify({"error": "Access Denied"}), 403
    
    difficulty = request.args.get('difficulty')
    location = request.args.get('location')
    
    # Sirf tab cache use karo jab koi filter na ho
    if not difficulty and not location:
        cached_data = current_app.redis_client.get('open_treks_cache')
        if cached_data:
            return jsonify(json.loads(cached_data)), 200
    
    query = Trek.query.filter_by(status='Open')
    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    if location:
        query = query.filter(Trek.location.ilike(f'%{location}%'))
    
    treks = query.all()
    result = [{"id": t.id, "name": t.name, "location": t.location, "difficulty": t.difficulty,
           "duration": t.duration, "available_slots": t.available_slots,
           "start_date": str(t.start_date), "end_date": str(t.end_date)} for t in treks]
    
    if not difficulty and not location:
        current_app.redis_client.setex('open_treks_cache', 30, json.dumps(result))
    
    return jsonify(result), 200

# Book a trek
@trekker_bp.route('/api/trekker/book/<int:trek_id>', methods=['POST'])
@login_required
def book_trek(trek_id):
    if current_user.role != 'trekker':
        return jsonify({"error": "Access Denied"}), 403
    
    trek = Trek.query.get(trek_id)
    if not trek:
        return jsonify({"error": "Trek not found"}), 404
    
    if trek.status != 'Open':
        return jsonify({"error": "Trek is not open for booking"}), 400
    
    if trek.available_slots <= 0:
        return jsonify({"error": "No slots available"}), 400
    
    existing_booking = Booking.query.filter_by(user_id=current_user.id, trek_id=trek_id, status='Booked').first()
    if existing_booking:
        return jsonify({"error": "You already booked this trek"}), 400
    
    new_booking = Booking(user_id=current_user.id, trek_id=trek_id, status='Booked', booking_date=date.today())
    trek.available_slots -= 1
    db.session.add(new_booking)
    db.session.commit()
    
    return jsonify({"message": "Trek booked successfully"}), 201


# View booking history/status
@trekker_bp.route('/api/trekker/my-bookings', methods=['GET'])
@login_required
def my_bookings():
    if current_user.role != 'trekker':
        return jsonify({"error": "Access Denied"}), 403
    
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    result = []
    for b in bookings:
        trek = Trek.query.get(b.trek_id)
        result.append({"trek_name": trek.name, "status": b.status, "booking_date": str(b.booking_date)})
    return jsonify(result), 200

@trekker_bp.route('/api/trekker/export-bookings', methods=['POST'])
@login_required
def export_bookings():
    if current_user.role != 'trekker':
        return jsonify({"error": "Access Denied"}), 403
    
    current_app.export_task.delay(current_user.id)
    return jsonify({"message": "Export started"}), 202

@trekker_bp.route('/api/trekker/download-export', methods=['GET'])
@login_required
def download_export():
    if current_user.role != 'trekker':
        return jsonify({"error": "Access Denied"}), 403
    
    filename = f'exports/bookings_user_{current_user.id}.csv'
    
    if not os.path.exists(filename):
        return jsonify({"error": "No export found. Please generate one first."}), 404
    
    return send_file(filename, as_attachment=True, download_name=f'my_bookings.csv')
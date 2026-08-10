from flask import Blueprint, request, jsonify,current_app
from models.models import db, User, Trek, Booking
from werkzeug.security import generate_password_hash
from flask_login import login_required, current_user
from datetime import datetime


admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/api/admin/add-staff', methods=['POST'])
@login_required
def add_staff():
    if current_user.role != 'admin':
        return jsonify({"error": "Access denied"}), 403
    
    data = request.get_json()
    name = data["name"]
    email = data["email"]
    password = data["password"]
    
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email already registered"}), 400
    
    hashed_password = generate_password_hash(password)
    new_staff = User(name=name, email=email, password=hashed_password, role="staff")
    db.session.add(new_staff)
    db.session.commit()
    
    return jsonify({"message": "Staff added successfully"}), 201

@admin_bp.route('/api/admin/create-trek', methods=['POST'])
@login_required
def create_trek():
    # 1. role check (admin hi allowed)
    if current_user.role != 'admin':
        return jsonify({"error": "Access Denied"}), 403
    
    # 2. data nikaalo request se: name, location, difficulty, duration, available_slots, start_date, end_date
    data = request.get_json()
    name = data["name"]
    location = data["location"]
    difficulty = data["difficulty"]
    duration = data["duration"]
    available_slots = data["available_slots"]
    start_date = datetime.strptime(data["start_date"], "%Y-%m-%d").date()
    end_date = datetime.strptime(data["end_date"], "%Y-%m-%d").date()
    
    # 3. naya Trek object banao
    
    new_trek = Trek(name= name, location=location, difficulty = difficulty,duration = duration, available_slots = available_slots , start_date = start_date, end_date= end_date )
    # 4. db mein save karo
    db.session.add(new_trek)
    db.session.commit()
    # 5. success response
    return jsonify({"message": "Trek added successfully"})

@admin_bp.route('/api/admin/update-trek/<int:trek_id>', methods=['PUT'])
@login_required
def update_trek(trek_id):

    if current_user.role != 'admin':
        return jsonify({"error": "Access Denied"}), 403

    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({"error": "Trek not found"}), 404

    data = request.get_json()

    trek.name = data["name"]
    trek.location = data["location"]
    trek.difficulty = data["difficulty"]
    trek.duration = data["duration"]
    trek.available_slots = data["available_slots"]
    trek.start_date = datetime.strptime(
        data["start_date"], "%Y-%m-%d"
    ).date()
    trek.end_date = datetime.strptime(
        data["end_date"], "%Y-%m-%d"
    ).date()

    db.session.commit()

    return jsonify({
        "message": "Trek updated successfully"
    })


@admin_bp.route('/api/admin/delete-trek/<int:trek_id>', methods=['DELETE'])
@login_required
def delete_trek(trek_id):
    if current_user.role != 'admin':
        return jsonify({"error": "Access Denied"}), 403

    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({"error": "Trek not found"}), 404

    db.session.delete(trek)
    db.session.commit()

    return jsonify({"message": "Trek deleted successfully"})

# Assign staff to a trek
@admin_bp.route('/api/admin/assign-staff', methods=['POST'])
@login_required
def assign_staff():
    if current_user.role != 'admin':
        return jsonify({"error": "Access Denied"}), 403
    
    data = request.get_json()
    trek_id = data["trek_id"]
    staff_id = data["staff_id"]
    
    trek = Trek.query.get(trek_id)
    staff = User.query.get(staff_id)
    
    if not trek or not staff or staff.role != 'staff':
        return jsonify({"error": "Invalid trek or staff ID"}), 400
    
    trek.assigned_staff_id = staff_id
    db.session.commit()
    return jsonify({"message": "Staff assigned successfully"}), 200


# Dashboard stats
@admin_bp.route('/api/admin/dashboard', methods=['GET'])
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return jsonify({"error": "Access Denied"}), 403
    
    total_treks = Trek.query.count()
    total_users = User.query.filter_by(role='trekker').count()
    total_staff = User.query.filter_by(role='staff').count()
    total_bookings = Booking.query.count()
    
    return jsonify({
        "total_treks": total_treks,
        "total_users": total_users,
        "total_staff": total_staff,
        "total_bookings": total_bookings
    }), 200


# View all treks
@admin_bp.route('/api/admin/treks', methods=['GET'])
@login_required
def view_all_treks():
    if current_user.role != 'admin':
        return jsonify({"error": "Access Denied"}), 403
    
    treks = Trek.query.all()
    result = []
    for t in treks:
        staff= User.query.get(t.assigned_staff_id) if t.assigned_staff_id else None
        result.append({
            "id": t.id,
            "name":t.name,
            "difficulty":t.difficulty,
            "duration":t.duration,
            "location": t.location,
            "status":t.status,
            "available_slots":t.available_slots,

            "start_date": str(t.start_date),
            "end_date": str(t.end_date),
            "assigned_staff": staff.name if staff else "Not Assigned"

        })
    return jsonify(result), 200    

# Search users/staff/treks (simple version — searches by name)
@admin_bp.route('/api/admin/search-users', methods=['GET'])
@login_required
def search_users():
    if current_user.role != 'admin':
        return jsonify({"error": "Access Denied"}), 403
    
    query = request.args.get('q', '')
    users = User.query.filter(User.name.ilike(f'%{query}%')).all()
    result = [{"id": u.id, "name": u.name, "email": u.email, "role": u.role, "status": u.status} for u in users]
    return jsonify(result), 200

@admin_bp.route('/api/admin/all-bookings', methods=['GET'])
@login_required
def view_all_bookings():
    if current_user.role != 'admin':
        return jsonify({"error": "Access Denied"}), 403
    
    bookings = Booking.query.all()
    result = []
    for b in bookings:
        user = User.query.get(b.user_id)
        trek = Trek.query.get(b.trek_id)
        result.append({
            "booking_id": b.id,
            "user_name": user.name if user else "Unknown",
            "trek_name": trek.name if trek else "Unknown",
            "status": b.status,
            "booking_date": str(b.booking_date)
        })
    return jsonify(result), 200


# Deactivate/blacklist a user
@admin_bp.route('/api/admin/blacklist-user', methods=['POST'])
@login_required
def blacklist_user():
    if current_user.role != 'admin':
        return jsonify({"error": "Access Denied"}), 403
    
    data = request.get_json()
    user_id = data["user_id"]
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    user.status = "blacklisted"
    db.session.commit()
    return jsonify({"message": "User blacklisted"}), 200

@admin_bp.route('/api/admin/unblacklist-user', methods=['POST'])
@login_required
def unblacklist_user():
    if current_user.role != 'admin':
        return jsonify({"error": "Access Denied"}), 403
    
    data = request.get_json()
    user_id = data["user_id"]
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    user.status = "active"
    db.session.commit()
    return jsonify({"message": "User reactivated"}), 200


@admin_bp.route('/api/admin/trigger-report', methods=['POST'])
@login_required
def trigger_report():
    if current_user.role != 'admin':
        return jsonify({"error": "Access Denied"}), 403
    
    current_app.report_task.delay()
    return jsonify({"message": "Report generated"}), 202





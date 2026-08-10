from flask import Blueprint, request, jsonify
from models.models import db, User, Trek, Booking
from flask_login import login_required, current_user

staff_bp = Blueprint('staff', __name__)


# @staff_bp.route('/api/staff/my-treks', methods=['GET'])
# @login_required
# def my_treks():
#     if current_user.role != 'staff':
#         return jsonify({"error": "Access Denied"}), 403
    
#     treks = Trek.query.filter_by(assigned_staff_id=current_user.id).all()
#     result = [{"id": t.id, "name": t.name, "status": t.status, "available_slots": t.available_slots} for t in treks]
#     return jsonify(result), 200
@staff_bp.route('/api/staff/my-treks', methods=['GET'])
@login_required
def my_treks():

    if current_user.role != 'staff':
        return jsonify({"error": "Access Denied"}), 403

    treks = Trek.query.filter_by(
        assigned_staff_id=current_user.id
    ).all()

    result = []

    for t in treks:

        bookings = Booking.query.filter_by(
            trek_id=t.id
        ).all()

        users = []

        for b in bookings:
            user = User.query.get(b.user_id)
            # print(user)
            if user:
                users.append({
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "status": b.status
                })
                     
        result.append({
            "id": t.id,
            "name": t.name,
            "status": t.status,
            "available_slots": t.available_slots,
            "registered_users": len(users),
            "users": users
        })

    return jsonify(result), 200


@staff_bp.route('/api/staff/update-trek/<int:trek_id>', methods=['PUT'])
@login_required
def update_trek(trek_id):
    if current_user.role != 'staff':
        return jsonify({"error": "Access Denied"}), 403
    
    trek = Trek.query.get(trek_id)
    if not trek or trek.assigned_staff_id != current_user.id:
        return jsonify({"error": "Trek not found or not assigned to you"}), 404
    
    data = request.get_json()
    if "available_slots" in data:
        trek.available_slots = data["available_slots"]
    if "status" in data:
        trek.status = data["status"]
    
    db.session.commit()
    return jsonify({"message": "Trek updated"}), 200



@staff_bp.route('/api/staff/trek-participants/<int:trek_id>', methods=['GET'])
@login_required
def trek_participants(trek_id):
    if current_user.role != 'staff':
        return jsonify({"error": "Access Denied"}), 403
    
    trek = Trek.query.get(trek_id)
    if not trek or trek.assigned_staff_id != current_user.id:
        return jsonify({"error": "Trek not found or not assigned to you"}), 404
    
    bookings = Booking.query.filter_by(trek_id=trek_id).all()
    result = [{"user_id": b.user_id, "status": b.status} for b in bookings]
    return jsonify(result), 200


@staff_bp.route('/api/staff/complete-trek/<int:trek_id>', methods=['POST'])
@login_required
def complete_trek(trek_id):
    if current_user.role != 'staff':
        return jsonify({"error": "Access Denied"}), 403
    
    trek = Trek.query.get(trek_id)
    if not trek or trek.assigned_staff_id != current_user.id:
        return jsonify({"error": "Trek not found or not assigned to you"}), 404
    
    trek.status = "Completed"
    db.session.commit()
    return jsonify({"message": "Trek marked as completed"}), 200
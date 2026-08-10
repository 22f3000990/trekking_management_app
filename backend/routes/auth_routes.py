from flask import Blueprint, request, jsonify
from models.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,login_required, logout_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data["name"]
    email = data["email"]
    password = data["password"]
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email already registered"}), 400
    hashed_password = generate_password_hash(password)
    new_user = User(name=name, email=email, password=hashed_password, role="trekker")
    db.session.add(new_user)
    db.session.commit()  
    return jsonify({"message": "Registered successfully"}), 201

@auth_bp.route('/api/login',methods=['POST'])
def login():
    data = request.get_json()
    email= data["email"]
    password = data["password"]

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "Email not registered"}), 401
    if not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid password"}), 401 
    if user.status == 'blacklisted':
        return jsonify({"error": "OMG! you're blacklisted by the admin."}), 403
    login_user(user)
    return jsonify({"message": "Login successful", "role": user.role}), 200

@auth_bp.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200
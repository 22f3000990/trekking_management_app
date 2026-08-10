from app import create_app
from models.models import db, User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    existing_admin = User.query.filter_by(email="rsuman@trek.com").first()
    if existing_admin:
        print("Admin Already Exists")
    else:
        password = "meadminhu"
        hashed_password = generate_password_hash(password)
        new_user = User(name="adminsuman", email="rsuman@trek.com", password=hashed_password, role="admin")
        db.session.add(new_user)
        db.session.commit()    
        print("admin Created")
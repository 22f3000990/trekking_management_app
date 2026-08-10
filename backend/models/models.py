from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id =db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email= db.Column(db.String(100), nullable = False, unique= True)
    password= db.Column(db.String(250),nullable= False)
    role = db.Column(db.String(25),nullable= False)
    status= db.Column(db.String(25), nullable= False, default= "active")

class Trek(db.Model):
    __tablename__= 'treks'
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(100), nullable = False)
    location= db.Column(db.String(200), nullable = False)
    difficulty= db.Column(db.String(20), nullable = False)
    duration= db.Column(db.Integer, nullable=False)
    available_slots= db.Column(db.Integer, nullable= False)
    assigned_staff_id= db.Column(db.Integer, db.ForeignKey('users.id'))
    status= db.Column(db.String(20), nullable = False, default= "pending")
    start_date= db.Column(db.Date, nullable = False)
    end_date= db.Column(db.Date, nullable = False)


class Booking (db.Model):
    __tablename__= 'bookings'
    id=db.Column(db.Integer, primary_key = True)
    user_id= db.Column(db.Integer, db.ForeignKey('users.id'))
    trek_id= db.Column(db.Integer, db.ForeignKey('treks.id'))
    booking_date= db.Column(db.Date, nullable= False)
    status= db.Column(db.String(50), nullable= False, default= "booked")
    payment_status= db.Column(db.String(50), nullable= True)     





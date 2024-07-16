from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from . import db 
#db = SQLAlchemy()

class booking(db.Model):
    __tablename__ = 'bookings' 
    bookingid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    mobile = db.Column(db.String(10), nullable=False, unique=True)
    tokenid = db.Column(db.Integer,db.ForeignKey('tokens.tokenid') ,nullable=False, unique=True)
    bookingtime = db.Column(db.Time, nullable=False)
    #token_date = db.Column(db.Date, nullable=False)
    #status = db.Column(db.String(20), nullable=False, default='Pending')
    employeeid = db.Column(db.Integer, db.ForeignKey('employees.employeeid'), nullable=False)

def __init__(self, name, age, gender, mobile, token_number, token_time, token_date, status, employee_id):
         self.name = name
         self.age = age
         self.gender = gender
         self.mobile = mobile
         self.token_number = token_number
         self.token_time = token_time
         self.token_date = token_date
         self.status = status
         self.employee_id = employee_id

         def __repr__(self):
           return f'<Token {self.id}>'

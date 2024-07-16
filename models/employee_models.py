from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from . import db 
#db = SQLAlchemy()

class Employee(db.Model):
    __tablename__ = 'employees'  
    employeeid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    department = db.Column(db.String(80), nullable=True)
    #created_at = db.Column(db.DateTime, default=datetime.utcnow)
    #tokens = db.relationship('Token', backref='employees', lazy=True)


    def __init__(self, name, department=None):
         self.name = name
         self.department = department

    def __repr__(self):
        return f'<Employee {self.id}>'

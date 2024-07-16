from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from . import db

class Token(db.Model):
    __tablename__ = 'tokens'
    tokenid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tokennumber = db.Column(db.Integer, nullable=False)
    tokendate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    tokentimestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    employeeid = db.Column(db.Integer, db.ForeignKey('employees.employeeid'), nullable=True)

    def __init__(self, tokennumber,tokentimestamp,tokendate, status,employeeid=None):
        self.tokennumber = tokennumber
        self.tokendate = datetime.utcnow()
        self.status = status
        self.tokentimestamp = datetime.utcnow()
        self.employeeid = employeeid

    def __repr__(self):
        return f'<Token {self.tokenid}>'

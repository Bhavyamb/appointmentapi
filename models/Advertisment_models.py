from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from . import db 
# db = SQLAlchemy()

class Advertisement(db.Model):
    __tablename__ = 'advertisements'
    adid = db.Column(db.Integer, primary_key=True)
    adcontent = db.Column(db.Text, nullable=False)
    startdate = db.Column(db.DateTime, nullable=False)
    enddate = db.Column(db.DateTime, nullable=False)
    isactive = db.Column(db.Boolean, default=True)
    image_path = db.Column(db.String(255), nullable=True)  # Add this line

    def __init__(self, adcontent, startdate, enddate, image_path=None, isactive=True):
        self.adcontent = adcontent
        self.startdate = startdate
        self.enddate = enddate
        self.image_path = image_path
        self.isactive = isactive

    def __repr__(self):
        return f'<Advertisement {self.adid}>'

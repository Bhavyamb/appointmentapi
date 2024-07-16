from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.booking_models import booking
from models.Advertisment_models import Advertisement
from models.employee_models import Employee
from models.token_models import Token

__all__ = ['db', 'booking', 'Advertisement', 'Employee','Token']


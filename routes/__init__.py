from flask import Blueprint

# Create blueprints for each route
from routes.appointment_routes import appointment_bp

# Optionally, import other blueprints as needed
# from routes.other_routes import other_bp

# Export the blueprints for use in the main application
__all__ = ['appointment_bp']  # Add other_bp here if importing others

# Alternatively, you can register blueprints directly in this file:
# app = Flask(__name__)
# app.register_blueprint(appointment_bp, url_prefix='/api')


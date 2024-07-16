from flask import Flask
from models import db  # Import db from your models package
from routes.appointment_routes import appointment_bp
from datetime import datetime

def create_app():
    app = Flask(__name__)
    
    # Load configuration from a separate file if needed
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/appointments'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize db with the Flask app
    db.init_app(app)
     # Set the upload folder path
    app.config['UPLOAD_FOLDER'] = 'C:/Users/bhavy/.vscode/images'

    # Register blueprints
    app.register_blueprint(appointment_bp, url_prefix='/api')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=8080)

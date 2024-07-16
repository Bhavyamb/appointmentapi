from datetime import datetime
import os
from flask import Blueprint, current_app, request, jsonify
from models import db, booking, Advertisement, Employee, Token  # Ensure Booking is imported
import models
from utils.appointment_utils import get_current_time, get_current_date
from werkzeug.utils import secure_filename

appointment_bp = Blueprint('appointment_bp', __name__)

# Example function using db
def get_token(employeeid):
    print('token')
    available_token = Token.query.filter(
        Token.tokennumber % 2 != 0,  # Use the correct attribute name
        Token.employeeid.is_(None),
        Token.status == 'pending'
    ).first()  # Fetch the first available token

    if available_token:
        available_token.employeeid = employeeid
        available_token.status = 'booked'
        available_token.tokentimestamp = get_current_time()
        available_token.tokendate = get_current_date()
        db.session.commit()
        return available_token.tokennumber

    # Generate a new odd token if no available token exists
    last_token = db.session.query(Token).order_by(Token.tokennumber.desc()).first()
    new_token_number = last_token.tokennumber + 2 if last_token else 1

    new_token = Token(
        tokennumber=new_token_number,
        tokentimestamp=get_current_time(),
        tokendate=get_current_date(),
        status='available',
        employeeid=None
    )

    db.session.add(new_token)
    db.session.commit()
    return new_token.tokennumber

# Token Booking Route
@appointment_bp.route('/book/token', methods=['POST'])
def book_token():
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')
    gender = data.get('gender')
    mobile = data.get('mobile')
    employeeid = 13  # Assuming employee ID 13 exists

    if not name or not age or not gender or not mobile:
        return jsonify({'error': 'Missing fields'}), 400

    tokens = db.session.query(Token.tokenid, Token.tokennumber).filter(
                Token.employeeid == employeeid,
                Token.status == 'pending'
                ).order_by(Token.tokennumber.asc()).all()
        
    odd_token = next((token for token in tokens if token.tokennumber % 2 != 0), None)
    if not odd_token:
        return jsonify({'error': 'No available odd-numbered token for employee 13'}), 404
    
    token_to_update = db.session.query(Token).filter_by(tokenid=odd_token.tokenid).first()
    token_to_update.status = 'booked'
    db.session.commit()

    bookingtime = datetime.now()

    new_booking = booking(  # Ensure you use the correct model name
        mobile=mobile,
        name=name,
        age=age,
        gender=gender,
        tokenid=odd_token.tokenid,
        bookingtime=bookingtime,
        employeeid=employeeid
    )

    db.session.add(new_booking)
    db.session.commit()

    return jsonify({'message': 'Token booked successfully', 'tokennumber': odd_token.tokennumber}), 200

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@appointment_bp.route('/advertisement/upload', methods=['POST'])
def upload_advertisement():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    adcontent = request.form.get('adcontent')
    startdate = request.form.get('startdate')
    enddate = request.form.get('enddate')
    isactive = request.form.get('isactive', 'True').lower() == 'true'

    # Check if the adcontent, startdate, and enddate are provided
    if not adcontent:
        return jsonify({'error': 'Advertisement content is required'}), 400

    if not startdate:
        return jsonify({'error': 'Start date is required'}), 400

    if not enddate:
        return jsonify({'error': 'End date is required'}), 400

    # Validate dates
    try:
        startdate = datetime.strptime(startdate, '%Y-%m-%d')
        enddate = datetime.strptime(enddate, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Save file path to the database
        new_advertisement = Advertisement(
            adcontent=adcontent,
            startdate=startdate,
            enddate=enddate,
            image_path=file_path,
            isactive=isactive
        )
        db.session.add(new_advertisement)
        db.session.commit()

        return jsonify({'message': 'Advertisement created successfully', 'image_path': file_path}), 201

    return jsonify({'error': 'Invalid file format'}), 400

@appointment_bp.route('/advertisements', methods=['GET'])
def get_advertisements():
    advertisements = Advertisement.query.all()
    result = []
    for ad in advertisements:
        start_date_str = ad.startdate.strftime('%Y-%m-%d') if ad.startdate else None
        end_date_str = ad.enddate.strftime('%Y-%m-%d') if ad.enddate else None
        result.append({
            'adid': ad.adid,
            'adcontent': ad.adcontent,
            'startdate': start_date_str,
            'enddate': end_date_str,
            'isactive': ad.isactive,
            'image_path': ad.image_path
        })
    return jsonify(result), 200

# Route to update token to 'in progress'
@appointment_bp.route('/token/inprogress', methods=['POST'])
def update_token_inprogress():
    data = request.get_json()
    token_number = data.get('token_number')
    employee_id = data.get('employee_id')

    if not token_number or not employee_id:
        return jsonify({'error': 'Token number and employee ID are required'}), 400

    # Validate employee ID (assuming ID 13 is authorized)
    if int(employee_id) != 13:
        return jsonify({'error': 'Unauthorized employee ID'}), 403

    token = Token.query.filter_by(tokennumber=token_number, status='booked').first()
    if not token:
        return jsonify({'error': 'Token not found or not in booked status'}), 404

    token.status = 'inprogress'
    db.session.commit()
    return jsonify({'message': 'Token status updated to in progress'})

# Route to fetch tokens in 'in progress' status
@appointment_bp.route('/tokens/inprogress', methods=['GET'])
def get_inprogress_tokens():
    tokens = Token.query.filter_by(status='inprogress').all()
    result = []
    for token in tokens:
        result.append({
            'tokenid': token.tokenid,
            'tokennumber': token.tokennumber,
            'status': token.status,
            'employeeid': token.employeeid
        })
    return jsonify(result), 200

# Route to close a token (mark as 'completed' or another status)
@appointment_bp.route('/token/close', methods=['POST'])
def close_token():
    data = request.get_json()
    token_number = data.get('token_number')
    employee_id = data.get('employee_id')

    if not token_number or not employee_id:
        return jsonify({'error': 'Token number and employee ID are required'}), 400

    # Validate employee ID (assuming ID 13 is authorized)
    if int(employee_id) != 13:
        return jsonify({'error': 'Unauthorized employee ID'}), 403

    token = Token.query.filter_by(tokennumber=token_number, status='inprogress').first()
    if not token:
        return jsonify({'error': 'Token not found or not in progress status'}), 404

    token.status = 'completed'  # Or any other status that signifies closure
    db.session.commit()
    return jsonify({'message': 'Token status updated to completed'})

# New route to validate mobile number and fetch booking details
@appointment_bp.route('/prevoiusbooking/validatemobile', methods=['POST'])
def validate_mobile():
    data = request.get_json()
    mobile_number = data.get('mobile_number')

    if not mobile_number:
        return jsonify({'error': 'Mobile number is required'}), 400

    # Check if the mobile number is valid
    if not is_valid_mobile_number(mobile_number):
        return jsonify({'error': 'Invalid mobile number'}), 400
    
    # Check if the mobile number is already registered in the bookings table
    booking_details = models.booking.query.filter_by(mobile=mobile_number).all()
    
    if booking_details:
        booking_dict = {}
        
        # Group bookings by name and keep the first booking entry
        for booking in booking_details:
            name = booking.name
            if name not in booking_dict:
                booking_dict[name] = {
                    'booking_id': booking.bookingid,
                    'age': booking.age,
                    'gender': booking.gender,
                    'token_id': booking.tokenid,
                    'booking_time': booking.bookingtime.strftime('%Y-%m-%d %H:%M:%S'),
                    'employee_id': booking.employeeid
                }
        
        # Convert dictionary to list format
        grouped_bookings = []
        for name, booking in booking_dict.items():
            grouped_bookings.append({
                'name': name,
                **booking
            })

        return jsonify({'bookings': grouped_bookings}), 200
    else:
        return jsonify({'message': 'No booking found for this mobile number'}), 404

def is_valid_mobile_number(mobile_number):
    # Add your mobile number validation logic here
    # Example: check length and numeric value
    return mobile_number.isdigit() and len(mobile_number) in [10]  # Adjust length as necessary

# Register blueprint
def register_routes(app):
    app.register_blueprint(appointment_bp, url_prefix='/api')

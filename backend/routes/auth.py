from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from models import Patient, Hospital, db
import re

auth_bp = Blueprint('auth', __name__)

def validate_aadhaar(aadhaar_id):
    """Simple Aadhaar validation (12 digits)"""
    return bool(re.match(r'^\d{12}$', aadhaar_id))

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or 'aadhaar_id' not in data:
            return jsonify({'error': 'Aadhaar ID is required'}), 400
        
        aadhaar_id = data['aadhaar_id']
        
        if not validate_aadhaar(aadhaar_id):
            return jsonify({'error': 'Invalid Aadhaar ID format'}), 400
        
        # For prototype, we'll create a simple authentication
        # In real implementation, this would involve proper password verification
        patient = Patient.query.filter_by(aadhaar_id=aadhaar_id).first()
        
        if not patient:
            return jsonify({'error': 'Patient not found. Please register first.'}), 404
        
        # Create access token
        access_token = create_access_token(
            identity=patient.id,
            additional_claims={'type': 'patient', 'aadhaar_id': aadhaar_id}
        )
        
        return jsonify({
            'access_token': access_token,
            'patient': patient.to_dict(),
            'message': 'Login successful'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['aadhaar_id', 'name', 'age', 'gender', 'phone', 'address', 'emergency_contact_name', 'emergency_contact_phone']
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
        
        # Validate Aadhaar ID
        if not validate_aadhaar(data['aadhaar_id']):
            return jsonify({'error': 'Invalid Aadhaar ID format'}), 400
        
        # Check if patient already exists
        existing_patient = Patient.query.filter_by(aadhaar_id=data['aadhaar_id']).first()
        if existing_patient:
            return jsonify({'error': 'Patient with this Aadhaar ID already exists'}), 409
        
        # Create new patient
        patient = Patient(
            aadhaar_id=data['aadhaar_id'],
            name=data['name'],
            age=int(data['age']),
            gender=data['gender'],
            phone=data['phone'],
            email=data.get('email'),
            address=data['address'],
            blood_group=data.get('blood_group'),
            emergency_contact_name=data['emergency_contact_name'],
            emergency_contact_phone=data['emergency_contact_phone']
        )
        
        db.session.add(patient)
        db.session.commit()
        
        # Create access token
        access_token = create_access_token(
            identity=patient.id,
            additional_claims={'type': 'patient', 'aadhaar_id': data['aadhaar_id']}
        )
        
        return jsonify({
            'access_token': access_token,
            'patient': patient.to_dict(),
            'message': 'Registration successful'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/hospital-login', methods=['POST'])
def hospital_login():
    try:
        data = request.get_json()
        
        if not data or 'registration_number' not in data:
            return jsonify({'error': 'Hospital registration number is required'}), 400
        
        registration_number = data['registration_number']
        
        hospital = Hospital.query.filter_by(registration_number=registration_number).first()
        
        if not hospital:
            return jsonify({'error': 'Hospital not found. Please register first.'}), 404
        
        # Create access token for hospital
        access_token = create_access_token(
            identity=hospital.id,
            additional_claims={'type': 'hospital', 'registration_number': registration_number}
        )
        
        return jsonify({
            'access_token': access_token,
            'hospital': hospital.to_dict(),
            'message': 'Hospital login successful'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/verify-token', methods=['GET'])
@jwt_required()
def verify_token():
    try:
        current_user_id = get_jwt_identity()
        # Return user info based on token
        return jsonify({
            'valid': True,
            'user_id': current_user_id
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
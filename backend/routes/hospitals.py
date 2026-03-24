from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Hospital, db
import json

hospitals_bp = Blueprint('hospitals', __name__)

@hospitals_bp.route('/', methods=['GET'])
def get_hospitals():
    try:
        hospitals = Hospital.query.all()
        return jsonify([hospital.to_dict() for hospital in hospitals]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@hospitals_bp.route('/register', methods=['POST'])
def register_hospital():
    try:
        data = request.get_json()
        
        required_fields = ['name', 'registration_number', 'address', 'phone', 'email', 'hospital_type']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
        
        # Check if hospital already exists
        existing_hospital = Hospital.query.filter_by(registration_number=data['registration_number']).first()
        if existing_hospital:
            return jsonify({'error': 'Hospital with this registration number already exists'}), 409
        
        hospital = Hospital(
            name=data['name'],
            registration_number=data['registration_number'],
            address=data['address'],
            phone=data['phone'],
            email=data['email'],
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            hospital_type=data['hospital_type'],
            specialties=json.dumps(data.get('specialties', [])),
            is_emergency_capable=data.get('is_emergency_capable', False)
        )
        
        db.session.add(hospital)
        db.session.commit()
        
        return jsonify({
            'message': 'Hospital registered successfully',
            'hospital': hospital.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
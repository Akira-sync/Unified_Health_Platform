from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Patient, db

patients_bp = Blueprint('patients', __name__)

@patients_bp.route('/', methods=['GET'])
@jwt_required()
def get_patients():
    try:
        patients = Patient.query.all()
        return jsonify([patient.to_dict() for patient in patients]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@patients_bp.route('/<patient_id>', methods=['GET'])
@jwt_required()
def get_patient(patient_id):
    try:
        patient = Patient.query.get(patient_id)
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        return jsonify(patient.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@patients_bp.route('/aadhaar/<aadhaar_id>', methods=['GET'])
@jwt_required()
def get_patient_by_aadhaar(aadhaar_id):
    try:
        patient = Patient.query.filter_by(aadhaar_id=aadhaar_id).first()
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        return jsonify(patient.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
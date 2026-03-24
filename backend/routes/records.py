from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import MedicalRecord, Patient, Hospital, db
from datetime import datetime

records_bp = Blueprint('records', __name__)

@records_bp.route('/patient/<patient_id>', methods=['GET'])
@jwt_required()
def get_patient_records(patient_id):
    try:
        records = MedicalRecord.query.filter_by(patient_id=patient_id).order_by(MedicalRecord.visit_date.desc()).all()
        return jsonify([record.to_dict() for record in records]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@records_bp.route('/create', methods=['POST'])
@jwt_required()
def create_medical_record():
    try:
        data = request.get_json()
        
        required_fields = ['patient_id', 'hospital_id', 'diagnosis', 'doctor_name', 'visit_type']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
        
        record = MedicalRecord(
            patient_id=data['patient_id'],
            hospital_id=data['hospital_id'],
            visit_date=datetime.fromisoformat(data.get('visit_date', datetime.utcnow().isoformat())),
            diagnosis=data['diagnosis'],
            symptoms=data.get('symptoms'),
            treatment=data.get('treatment'),
            prescriptions=data.get('prescriptions'),
            doctor_name=data['doctor_name'],
            doctor_specialization=data.get('doctor_specialization'),
            visit_type=data['visit_type'],
            discharge_summary=data.get('discharge_summary'),
            lab_reports=data.get('lab_reports')
        )
        
        db.session.add(record)
        db.session.commit()
        
        return jsonify({
            'message': 'Medical record created successfully',
            'record': record.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
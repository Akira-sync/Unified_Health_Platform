from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Bed, Hospital, Patient, db
from datetime import datetime

emergency_bp = Blueprint('emergency', __name__)

@emergency_bp.route('/find-beds', methods=['POST'])
def find_emergency_beds():
    try:
        data = request.get_json()
        bed_type = data.get('bed_type', 'ICU')  # Default to ICU for emergencies
        patient_location = data.get('location')  # For future geographic sorting
        
        # Find available beds in emergency-capable hospitals
        available_beds = db.session.query(Bed, Hospital).join(Hospital).filter(
            Bed.is_occupied == False,
            Bed.bed_type == bed_type,
            Hospital.is_emergency_capable == True
        ).all()
        
        emergency_beds = []
        for bed, hospital in available_beds:
            emergency_beds.append({
                'bed': bed.to_dict(),
                'hospital': hospital.to_dict(),
                'priority_score': 100  # Can be calculated based on distance, specialization, etc.
            })
        
        # Sort by priority (in a real system, this would consider distance, specialization, etc.)
        emergency_beds.sort(key=lambda x: x['priority_score'], reverse=True)
        
        return jsonify({
            'total_available': len(emergency_beds),
            'emergency_beds': emergency_beds,
            'search_timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@emergency_bp.route('/book-emergency-bed', methods=['POST'])
@jwt_required()
def book_emergency_bed():
    try:
        data = request.get_json()
        
        required_fields = ['bed_id', 'patient_id', 'emergency_type']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
        
        bed = Bed.query.get(data['bed_id'])
        if not bed:
            return jsonify({'error': 'Bed not found'}), 404
        
        if bed.is_occupied:
            return jsonify({'error': 'Bed is no longer available'}), 409
        
        patient = Patient.query.get(data['patient_id'])
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        # Book the bed
        bed.is_occupied = True
        bed.current_patient_id = data['patient_id']
        bed.last_updated = datetime.utcnow()
        
        db.session.commit()
        
        # Broadcast emergency booking
        from app import socketio
        socketio.emit('emergency_booking', {
            'type': 'emergency_bed_booked',
            'bed': bed.to_dict(),
            'patient': patient.to_dict(),
            'emergency_type': data['emergency_type'],
            'timestamp': datetime.utcnow().isoformat()
        })
        
        return jsonify({
            'message': 'Emergency bed booked successfully',
            'bed': bed.to_dict(),
            'patient': patient.to_dict(),
            'booking_reference': f"EMR-{datetime.utcnow().strftime('%Y%m%d')}-{bed.id[:8]}"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
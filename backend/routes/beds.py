from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Bed, Hospital, db
from datetime import datetime
import json

beds_bp = Blueprint('beds', __name__)

@beds_bp.route('/search', methods=['GET'])
def search_available_beds():
    try:
        # Get query parameters
        bed_type = request.args.get('type', 'General')
        hospital_id = request.args.get('hospital_id')
        location = request.args.get('location')  # City/area for filtering
        emergency_only = request.args.get('emergency_only', 'false').lower() == 'true'
        
        query = Bed.query.filter_by(is_occupied=False, bed_type=bed_type)
        
        if hospital_id:
            query = query.filter_by(hospital_id=hospital_id)
        
        if emergency_only:
            # Join with hospitals to filter emergency-capable ones
            query = query.join(Hospital).filter(Hospital.is_emergency_capable == True)
        
        available_beds = query.all()
        
        # Group by hospital for better presentation
        beds_by_hospital = {}
        for bed in available_beds:
            hospital = Hospital.query.get(bed.hospital_id)
            if hospital:
                if hospital.id not in beds_by_hospital:
                    beds_by_hospital[hospital.id] = {
                        'hospital': hospital.to_dict(),
                        'available_beds': []
                    }
                beds_by_hospital[hospital.id]['available_beds'].append(bed.to_dict())
        
        return jsonify({
            'total_hospitals': len(beds_by_hospital),
            'total_beds': len(available_beds),
            'hospitals_with_beds': list(beds_by_hospital.values())
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@beds_bp.route('/hospital/<hospital_id>', methods=['GET'])
def get_hospital_beds(hospital_id):
    try:
        hospital = Hospital.query.get(hospital_id)
        if not hospital:
            return jsonify({'error': 'Hospital not found'}), 404
        
        beds = Bed.query.filter_by(hospital_id=hospital_id).all()
        
        # Group beds by type and status
        bed_summary = {}
        for bed in beds:
            bed_type = bed.bed_type
            if bed_type not in bed_summary:
                bed_summary[bed_type] = {
                    'total': 0,
                    'occupied': 0,
                    'available': 0,
                    'beds': []
                }
            
            bed_summary[bed_type]['total'] += 1
            bed_summary[bed_type]['beds'].append(bed.to_dict())
            
            if bed.is_occupied:
                bed_summary[bed_type]['occupied'] += 1
            else:
                bed_summary[bed_type]['available'] += 1
        
        return jsonify({
            'hospital': hospital.to_dict(),
            'bed_summary': bed_summary
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@beds_bp.route('/occupy/<bed_id>', methods=['POST'])
@jwt_required()
def occupy_bed(bed_id):
    try:
        data = request.get_json()
        patient_id = data.get('patient_id')
        
        if not patient_id:
            return jsonify({'error': 'Patient ID is required'}), 400
        
        bed = Bed.query.get(bed_id)
        if not bed:
            return jsonify({'error': 'Bed not found'}), 404
        
        if bed.is_occupied:
            return jsonify({'error': 'Bed is already occupied'}), 409
        
        # Update bed status
        bed.is_occupied = True
        bed.current_patient_id = patient_id
        bed.last_updated = datetime.utcnow()
        
        db.session.commit()
        
        # Broadcast update to hospital room
        from app import socketio
        socketio.emit('bed_update', {
            'type': 'occupied',
            'bed': bed.to_dict(),
            'hospital_id': bed.hospital_id
        }, room=f'hospital_{bed.hospital_id}')
        
        return jsonify({
            'message': 'Bed successfully occupied',
            'bed': bed.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@beds_bp.route('/release/<bed_id>', methods=['POST'])
@jwt_required()
def release_bed(bed_id):
    try:
        bed = Bed.query.get(bed_id)
        if not bed:
            return jsonify({'error': 'Bed not found'}), 404
        
        if not bed.is_occupied:
            return jsonify({'error': 'Bed is not currently occupied'}), 409
        
        # Update bed status
        bed.is_occupied = False
        bed.current_patient_id = None
        bed.last_updated = datetime.utcnow()
        
        db.session.commit()
        
        # Broadcast update to hospital room
        from app import socketio
        socketio.emit('bed_update', {
            'type': 'released',
            'bed': bed.to_dict(),
            'hospital_id': bed.hospital_id
        }, room=f'hospital_{bed.hospital_id}')
        
        return jsonify({
            'message': 'Bed successfully released',
            'bed': bed.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@beds_bp.route('/create', methods=['POST'])
@jwt_required()
def create_bed():
    try:
        data = request.get_json()
        
        required_fields = ['hospital_id', 'bed_number', 'bed_type']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
        
        # Verify hospital exists
        hospital = Hospital.query.get(data['hospital_id'])
        if not hospital:
            return jsonify({'error': 'Hospital not found'}), 404
        
        # Check if bed number already exists in the hospital
        existing_bed = Bed.query.filter_by(
            hospital_id=data['hospital_id'],
            bed_number=data['bed_number']
        ).first()
        
        if existing_bed:
            return jsonify({'error': 'Bed number already exists in this hospital'}), 409
        
        # Create new bed
        bed = Bed(
            hospital_id=data['hospital_id'],
            bed_number=data['bed_number'],
            bed_type=data['bed_type'],
            ward_name=data.get('ward_name'),
            floor_number=data.get('floor_number'),
            equipment_available=json.dumps(data.get('equipment_available', [])),
            cost_per_day=data.get('cost_per_day')
        )
        
        db.session.add(bed)
        db.session.commit()
        
        return jsonify({
            'message': 'Bed created successfully',
            'bed': bed.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@beds_bp.route('/update/<bed_id>', methods=['PUT'])
@jwt_required()
def update_bed(bed_id):
    try:
        data = request.get_json()
        
        bed = Bed.query.get(bed_id)
        if not bed:
            return jsonify({'error': 'Bed not found'}), 404
        
        # Update allowed fields
        updateable_fields = ['bed_type', 'ward_name', 'floor_number', 'equipment_available', 'cost_per_day']
        
        for field in updateable_fields:
            if field in data:
                if field == 'equipment_available':
                    setattr(bed, field, json.dumps(data[field]))
                else:
                    setattr(bed, field, data[field])
        
        bed.last_updated = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Bed updated successfully',
            'bed': bed.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@beds_bp.route('/stats', methods=['GET'])
def get_bed_statistics():
    try:
        # Overall statistics
        total_beds = Bed.query.count()
        occupied_beds = Bed.query.filter_by(is_occupied=True).count()
        available_beds = total_beds - occupied_beds
        
        # Statistics by bed type
        bed_types = db.session.query(Bed.bed_type, 
                                   db.func.count(Bed.id).label('total'),
                                   db.func.sum(db.case([(Bed.is_occupied == True, 1)], else_=0)).label('occupied')
                                   ).group_by(Bed.bed_type).all()
        
        type_stats = {}
        for bed_type, total, occupied in bed_types:
            type_stats[bed_type] = {
                'total': total,
                'occupied': occupied or 0,
                'available': total - (occupied or 0)
            }
        
        # Statistics by hospital
        hospital_stats = db.session.query(Hospital.name, Hospital.id,
                                        db.func.count(Bed.id).label('total_beds'),
                                        db.func.sum(db.case([(Bed.is_occupied == True, 1)], else_=0)).label('occupied_beds')
                                        ).join(Bed).group_by(Hospital.id, Hospital.name).all()
        
        hospitals = []
        for name, hospital_id, total, occupied in hospital_stats:
            hospitals.append({
                'hospital_id': hospital_id,
                'hospital_name': name,
                'total_beds': total,
                'occupied_beds': occupied or 0,
                'available_beds': total - (occupied or 0),
                'occupancy_rate': round((occupied or 0) / total * 100, 2) if total > 0 else 0
            })
        
        return jsonify({
            'overall': {
                'total_beds': total_beds,
                'occupied_beds': occupied_beds,
                'available_beds': available_beds,
                'occupancy_rate': round(occupied_beds / total_beds * 100, 2) if total_beds > 0 else 0
            },
            'by_type': type_stats,
            'by_hospital': hospitals
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
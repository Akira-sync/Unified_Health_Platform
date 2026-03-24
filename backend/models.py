from flask_sqlalchemy import SQLAlchemy
from extensions import db
import uuid
from datetime import datetime

#db = SQLAlchemy()

class Patient(db.Model):
    __tablename__ = 'patients'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    aadhaar_id = db.Column(db.String(12), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    address = db.Column(db.Text, nullable=False)
    blood_group = db.Column(db.String(5), nullable=True)
    emergency_contact_name = db.Column(db.String(100), nullable=False)
    emergency_contact_phone = db.Column(db.String(15), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    medical_records = db.relationship('MedicalRecord', backref='patient', lazy=True)
    appointments = db.relationship('Appointment', backref='patient', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'aadhaar_id': self.aadhaar_id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'blood_group': self.blood_group,
            'emergency_contact_name': self.emergency_contact_name,
            'emergency_contact_phone': self.emergency_contact_phone,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Hospital(db.Model):
    __tablename__ = 'hospitals'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(200), nullable=False)
    registration_number = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    hospital_type = db.Column(db.String(50), nullable=False)  # Government, Private, Specialty
    specialties = db.Column(db.Text, nullable=True)  # JSON array of specialties
    is_emergency_capable = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    beds = db.relationship('Bed', backref='hospital', lazy=True)
    medical_records = db.relationship('MedicalRecord', backref='hospital', lazy=True)
    appointments = db.relationship('Appointment', backref='hospital', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'registration_number': self.registration_number,
            'address': self.address,
            'phone': self.phone,
            'email': self.email,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'hospital_type': self.hospital_type,
            'specialties': self.specialties,
            'is_emergency_capable': self.is_emergency_capable,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Bed(db.Model):
    __tablename__ = 'beds'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    hospital_id = db.Column(db.String(36), db.ForeignKey('hospitals.id'), nullable=False)
    bed_number = db.Column(db.String(20), nullable=False)
    bed_type = db.Column(db.String(50), nullable=False)  # General, ICU, Emergency, Maternity
    is_occupied = db.Column(db.Boolean, default=False)
    current_patient_id = db.Column(db.String(36), nullable=True)
    ward_name = db.Column(db.String(100), nullable=True)
    floor_number = db.Column(db.Integer, nullable=True)
    equipment_available = db.Column(db.Text, nullable=True)  # JSON array
    cost_per_day = db.Column(db.Float, nullable=True)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'hospital_id': self.hospital_id,
            'bed_number': self.bed_number,
            'bed_type': self.bed_type,
            'is_occupied': self.is_occupied,
            'current_patient_id': self.current_patient_id,
            'ward_name': self.ward_name,
            'floor_number': self.floor_number,
            'equipment_available': self.equipment_available,
            'cost_per_day': self.cost_per_day,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }

class MedicalRecord(db.Model):
    __tablename__ = 'medical_records'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = db.Column(db.String(36), db.ForeignKey('patients.id'), nullable=False)
    hospital_id = db.Column(db.String(36), db.ForeignKey('hospitals.id'), nullable=False)
    visit_date = db.Column(db.DateTime, nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    symptoms = db.Column(db.Text, nullable=True)
    treatment = db.Column(db.Text, nullable=True)
    prescriptions = db.Column(db.Text, nullable=True)  # JSON array
    doctor_name = db.Column(db.String(100), nullable=False)
    doctor_specialization = db.Column(db.String(100), nullable=True)
    visit_type = db.Column(db.String(50), nullable=False)  # Emergency, Regular, Follow-up
    discharge_summary = db.Column(db.Text, nullable=True)
    lab_reports = db.Column(db.Text, nullable=True)  # JSON array of file paths
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'hospital_id': self.hospital_id,
            'visit_date': self.visit_date.isoformat() if self.visit_date else None,
            'diagnosis': self.diagnosis,
            'symptoms': self.symptoms,
            'treatment': self.treatment,
            'prescriptions': self.prescriptions,
            'doctor_name': self.doctor_name,
            'doctor_specialization': self.doctor_specialization,
            'visit_type': self.visit_type,
            'discharge_summary': self.discharge_summary,
            'lab_reports': self.lab_reports,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = db.Column(db.String(36), db.ForeignKey('patients.id'), nullable=False)
    hospital_id = db.Column(db.String(36), db.ForeignKey('hospitals.id'), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    doctor_name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    appointment_type = db.Column(db.String(50), nullable=False)  # Regular, Emergency, Follow-up
    status = db.Column(db.String(20), default='Scheduled')  # Scheduled, Completed, Cancelled, No-show
    notes = db.Column(db.Text, nullable=True)
    queue_number = db.Column(db.Integer, nullable=True)
    estimated_wait_time = db.Column(db.Integer, nullable=True)  # in minutes
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'hospital_id': self.hospital_id,
            'appointment_date': self.appointment_date.isoformat() if self.appointment_date else None,
            'doctor_name': self.doctor_name,
            'department': self.department,
            'appointment_type': self.appointment_type,
            'status': self.status,
            'notes': self.notes,
            'queue_number': self.queue_number,
            'estimated_wait_time': self.estimated_wait_time,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
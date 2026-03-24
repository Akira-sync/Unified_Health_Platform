#!/usr/bin/env python3
"""
Demo data seeding script for Unified Health Platform
Populates the database with sample hospitals, patients, beds, and medical records
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app # still the Flask app
from extensions import db # import the db instance
from models import Patient, Hospital, Bed, MedicalRecord, Appointment
from datetime import datetime, timedelta
import json

def seed_demo_data():
    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        db.drop_all()
        db.create_all()
        
        # Create sample hospitals
        print("Creating sample hospitals...")
        hospitals = [
            Hospital(
                name="AIIMS New Delhi",
                registration_number="AIIMS-DEL-001",
                address="Ansari Nagar, New Delhi, Delhi 110029",
                phone="011-26588500",
                email="info@aiims.edu",
                latitude=28.5672,
                longitude=77.2100,
                hospital_type="Government",
                specialties=json.dumps(["Cardiology", "Neurology", "Oncology", "Emergency Medicine", "ICU"]),
                is_emergency_capable=True
            ),
            Hospital(
                name="Apollo Hospital Delhi",
                registration_number="APOLLO-DEL-002",
                address="Mathura Road, Sarita Vihar, New Delhi, Delhi 110076",
                phone="011-71791000",
                email="info@apollohospitals.com",
                latitude=28.5355,
                longitude=77.2954,
                hospital_type="Private",
                specialties=json.dumps(["Cardiology", "Orthopedics", "Gastroenterology", "ICU"]),
                is_emergency_capable=True
            ),
            Hospital(
                name="Fortis Hospital Gurgaon",
                registration_number="FORTIS-GUR-003",
                address="Sector 44, Gurugram, Haryana 122002",
                phone="0124-4962200",
                email="info@fortishealthcare.com",
                latitude=28.4508,
                longitude=77.0677,
                hospital_type="Private",
                specialties=json.dumps(["Cardiology", "Neurosurgery", "Oncology", "Emergency"]),
                is_emergency_capable=True
            ),
            Hospital(
                name="Max Super Speciality Hospital",
                registration_number="MAX-SAK-004",
                address="2, Press Enclave Road, Saket, New Delhi, Delhi 110017",
                phone="011-26515050",
                email="info@maxhealthcare.com",
                latitude=28.5244,
                longitude=77.2066,
                hospital_type="Private",
                specialties=json.dumps(["Cardiac Surgery", "Neurology", "Orthopedics"]),
                is_emergency_capable=True
            ),
            Hospital(
                name="Safdarjung Hospital",
                registration_number="SAFDAR-DEL-005",
                address="Ansari Nagar West, New Delhi, Delhi 110029",
                phone="011-26165060",
                email="info@safdarjung.nic.in",
                latitude=28.5689,
                longitude=77.2089,
                hospital_type="Government",
                specialties=json.dumps(["General Medicine", "Surgery", "Emergency", "Maternity"]),
                is_emergency_capable=True
            )
        ]
        
        for hospital in hospitals:
            db.session.add(hospital)
        db.session.commit()
        print(f"Created {len(hospitals)} hospitals")
        
        # Create beds for each hospital
        print("Creating hospital beds...")
        bed_types = ["General", "ICU", "Emergency", "Maternity"]
        total_beds = 0
        
        for hospital in hospitals:
            # Create different types of beds for each hospital
            for bed_type in bed_types:
                bed_count = 10 if bed_type == "General" else 5
                for i in range(1, bed_count + 1):
                    bed = Bed(
                        hospital_id=hospital.id,
                        bed_number=f"{bed_type[0]}{i:03d}",
                        bed_type=bed_type,
                        is_occupied=(i % 3 == 0),  # Make every 3rd bed occupied
                        ward_name=f"{bed_type} Ward",
                        floor_number=2 if bed_type == "ICU" else 1,
                        equipment_available=json.dumps([
                            "Oxygen", "Monitor", "IV Stand"
                        ] + (["Ventilator"] if bed_type == "ICU" else [])),
                        cost_per_day=5000.0 if bed_type == "ICU" else 2000.0
                    )
                    db.session.add(bed)
                    total_beds += 1
        
        db.session.commit()
        print(f"Created {total_beds} beds")
        
        # Create sample patients
        print("Creating sample patients...")
        patients = [
            Patient(
                aadhaar_id="123456789012",
                name="Rajesh Kumar",
                age=45,
                gender="Male",
                phone="9876543210",
                email="rajesh.kumar@email.com",
                address="123 Main Street, New Delhi, Delhi 110001",
                blood_group="B+",
                emergency_contact_name="Sunita Kumar",
                emergency_contact_phone="9876543211"
            ),
            Patient(
                aadhaar_id="234567890123",
                name="Priya Sharma",
                age=32,
                gender="Female",
                phone="9876543212",
                email="priya.sharma@email.com",
                address="456 Park Avenue, Gurgaon, Haryana 122001",
                blood_group="A+",
                emergency_contact_name="Vikram Sharma",
                emergency_contact_phone="9876543213"
            ),
            Patient(
                aadhaar_id="345678901234",
                name="Mohammad Ali",
                age=28,
                gender="Male",
                phone="9876543214",
                email="mohammad.ali@email.com",
                address="789 Old City Road, New Delhi, Delhi 110002",
                blood_group="O-",
                emergency_contact_name="Fatima Ali",
                emergency_contact_phone="9876543215"
            ),
            Patient(
                aadhaar_id="456789012345",
                name="Anita Patel",
                age=55,
                gender="Female",
                phone="9876543216",
                email="anita.patel@email.com",
                address="321 Business District, New Delhi, Delhi 110003",
                blood_group="AB+",
                emergency_contact_name="Ravi Patel",
                emergency_contact_phone="9876543217"
            ),
            Patient(
                aadhaar_id="567890123456",
                name="Suresh Gupta",
                age=38,
                gender="Male",
                phone="9876543218",
                email="suresh.gupta@email.com",
                address="654 Green Park, New Delhi, Delhi 110016",
                blood_group="O+",
                emergency_contact_name="Meera Gupta",
                emergency_contact_phone="9876543219"
            )
        ]
        
        for patient in patients:
            db.session.add(patient)
        db.session.commit()
        print(f"Created {len(patients)} patients")
        
        # Create sample medical records
        print("Creating medical records...")
        medical_records = [
            MedicalRecord(
                patient_id=patients[0].id,
                hospital_id=hospitals[0].id,
                visit_date=datetime.now() - timedelta(days=30),
                diagnosis="Hypertension",
                symptoms="High blood pressure, headaches",
                treatment="Prescribed antihypertensive medication",
                prescriptions=json.dumps([
                    {"medicine": "Amlodipine", "dosage": "5mg", "frequency": "Once daily"},
                    {"medicine": "Lisinopril", "dosage": "10mg", "frequency": "Once daily"}
                ]),
                doctor_name="Dr. Ramesh Verma",
                doctor_specialization="Cardiology",
                visit_type="Regular"
            ),
            MedicalRecord(
                patient_id=patients[1].id,
                hospital_id=hospitals[1].id,
                visit_date=datetime.now() - timedelta(days=15),
                diagnosis="Diabetes Type 2",
                symptoms="Increased thirst, frequent urination",
                treatment="Dietary changes and medication",
                prescriptions=json.dumps([
                    {"medicine": "Metformin", "dosage": "500mg", "frequency": "Twice daily"}
                ]),
                doctor_name="Dr. Sita Rani",
                doctor_specialization="Endocrinology",
                visit_type="Regular"
            ),
            MedicalRecord(
                patient_id=patients[2].id,
                hospital_id=hospitals[0].id,
                visit_date=datetime.now() - timedelta(days=7),
                diagnosis="Acute Myocardial Infarction",
                symptoms="Chest pain, shortness of breath",
                treatment="Emergency cardiac intervention, ICU monitoring",
                prescriptions=json.dumps([
                    {"medicine": "Aspirin", "dosage": "75mg", "frequency": "Once daily"},
                    {"medicine": "Atorvastatin", "dosage": "20mg", "frequency": "Once daily"}
                ]),
                doctor_name="Dr. Ashok Kumar",
                doctor_specialization="Emergency Medicine",
                visit_type="Emergency"
            )
        ]
        
        for record in medical_records:
            db.session.add(record)
        db.session.commit()
        print(f"Created {len(medical_records)} medical records")
        
        # Create some appointments
        print("Creating sample appointments...")
        appointments = [
            Appointment(
                patient_id=patients[0].id,
                hospital_id=hospitals[0].id,
                appointment_date=datetime.now() + timedelta(days=7),
                doctor_name="Dr. Ramesh Verma",
                department="Cardiology",
                appointment_type="Follow-up",
                status="Scheduled",
                queue_number=5,
                estimated_wait_time=25
            ),
            Appointment(
                patient_id=patients[1].id,
                hospital_id=hospitals[1].id,
                appointment_date=datetime.now() + timedelta(days=3),
                doctor_name="Dr. Sita Rani",
                department="Endocrinology",
                appointment_type="Regular",
                status="Scheduled",
                queue_number=2,
                estimated_wait_time=10
            )
        ]
        
        for appointment in appointments:
            db.session.add(appointment)
        db.session.commit()
        print(f"Created {len(appointments)} appointments")
        
        print("\n✅ Demo data seeded successfully!")
        print(f"Created:")
        print(f"  - {len(hospitals)} hospitals")
        print(f"  - {total_beds} beds")
        print(f"  - {len(patients)} patients") 
        print(f"  - {len(medical_records)} medical records")
        print(f"  - {len(appointments)} appointments")
        
        print(f"\n📋 Demo login credentials:")
        print(f"Patient Aadhaar IDs for testing:")
        for patient in patients:
            print(f"  - {patient.aadhaar_id} ({patient.name})")

if __name__ == "__main__":
    seed_demo_data()
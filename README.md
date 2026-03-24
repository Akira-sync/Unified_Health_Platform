
# Unified Health Platform

This project is a prototype built during a hackathon to explore solutions for common healthcare challenges in India

## Problem Statement

India's healthcare system suffers from:
- Long wait times and inefficient queue management
- No real-time visibility of hospital bed availability (especially ICU)
- Fragmented patient records across hospitals
- Emergency delays in finding ICU beds
- Difficulty accessing medical history in critical situations
- Lack of unified Aadhaar-linked health platform
- Absence of digital prescriptions and secure data sharing

## What This Project Does

It provides a unified platform where:
- Patients can view available hospital beds in real time
- Hospitals can manage bed availability and patent intake
- Medical records are securely accessible across institutions



## Solution Features

- **Real-time Bed Tracking**: Live availability of hospital beds across facilities
- **Aadhaar-Linked Patient Records**: Unified patient identity and medical history
- **Digital Prescriptions**: Electronic prescription management
- **Emergency Services Integration**: Quick ICU bed discovery for emergencies
- **Secure Data Sharing**: Secure patient data sharing between authorized healthcare providers
- **Queue Management**: Reduce wait times through digital appointment booking

## Tech Stack

- **Backend**: Flask (Python), SQLAlchemy
- **Frontend**: React.js (Material-UI)
- **Database**: SQLite (prototype)
- **Real-time**: WebSocket for live updates
- **Authentication**: JWT tokens

## Project Structure (Simplified)

unified-health-platform/
├── backend/           # Flask API server
├── frontend/          # React web application  
├── database/          # Database schema and migrations
├── docs/             # Documentation
└── README.md

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn
- Git (optional, for version control)

Follow these steps to run the project locally:

### Step 1: Backend Setup
```bash
cd backend

# Install required python packages
pip install -r requirements.txt

# Add demo data to the database
python seed_demo_data.py

# Start the Flask server
python app.py
```
Backend runs at http://localhost:5000

### Step 2: Frontend Setup
```bash
cd frontend

# Install Node.js dependencies
npm install

# Start the React development server
npm start
```
Frontend runs at http://localhost:3000

## Demo Scenarios

### Patient Workflows
1. **Patient Registration**: Register with Aadhaar and create medical profile
   - Register a new patient using the web interface

2. **Patient Login & Dashboard**: Access patient dashboard
   - Use demo Aadhaar IDs: `123456789012`, `234567890123`, `345678901234`
   - View patient profile and quick actions

> Note: Aadhaar numbers used here are dummy data for demonstration purposes only

3. **Bed Search**: Real-time search for available beds in nearby hospitals
   - Browse available beds across multiple hospitals
   - Filter by bed type (General, ICU, Emergency, Maternity)

4. **Medical Records**: View comprehensive health history across hospitals
   - Access patient profile and quick actions
   - Check prescriptions, diagnoses and treatment history

### Hospital Workflows
5. **Hospital Dashboard**: Manage bed availability and patient intake
   - Login as hospital administrator
   - Update bed status and manage hospital information

### Emergency Services
6. **Emergency Mode**: Critical patient bed allocation with priority routing
   - Quickly find available beds for critical patients
   - Priority booking during emergencies

## Demo Data

The project includes sample data such as:

- **5 Hospitals**: AIIMS Delhi, Apollo Hospital, Fortis Gurgaon, Max Hospital, Safdarjung Hospital
- **150+ Beds**: 150+ beds including General, ICU, Emergency and Maternity types
- **5 Demo Patients**: With complete profiles and medical histories
- **Medical Records**: Sample diagnoses, prescriptions, and treatment records
- **Appointments**: Scheduled appointments with queue management

### Demo Login Credentials

**Patient Aadhaar IDs for testing:**
- `123456789012` - Rajesh Kumar (Male, 45, B+)
- `234567890123` - Priya Sharma (Female, 32, A+)
- `345678901234` - Mohammad Ali (Male, 28, O-)
- `456789012345` - Anita Patel (Female, 55, AB+)
- `567890123456` - Suresh Gupta (Male, 38, O+)

**Sample Hospital Registration Numbers:**
- AIIMS New Delhi (`AIIMS-DEL-001`)
- Apollo Hospital Delhi (`APOLLO-DEL-002`)
- Fortis Hospital Gurgaon (`FORTIS-GUR-003`)

## API Endpoints

- `/api/auth/login` - Patient authentication
- `/api/auth/register` - Patient registration
- `/api/patients` - Patient management
- `/api/hospitals` - Hospital registration and management
- `/api/beds` - Check real-time bed availability
- `/api/records` - Access medical records
- `/api/emergency` - Emergency services integration

## Contributing

This project prototype was built as part of a hackathon. Contibutions and improvements are welcome, especially around core functionality and user experience.

## License

MIT License - Developed as a part of a healthcare innovation hackathon.

# Unified Health Platform

A hackathon prototype addressing India's healthcare system challenges including long queues, lack of real-time bed availability, and fragmented patient records.

## Problem Statement

India's healthcare system suffers from:
- Long queues and wait times
- Lack of real-time bed availability information
- Fragmented patient records across different hospitals
- Emergency delays in finding ICU beds
- Difficulty accessing medical history in critical situations
- Lack of unified Aadhaar-linked health platform
- Absence of digital prescriptions and secure data sharing

## Solution Features

- **Real-time Bed Tracking**: Live availability of hospital beds across facilities
- **Aadhaar-Linked Patient Records**: Unified patient identity and medical history
- **Digital Prescriptions**: Electronic prescription management
- **Emergency Services Integration**: Quick ICU bed discovery for emergencies
- **Secure Data Sharing**: HIPAA-compliant patient data sharing between authorized healthcare providers
- **Queue Management**: Reduce wait times through digital appointment booking

## Tech Stack

- **Backend**: Python Flask with SQLAlchemy
- **Frontend**: React.js with Material-UI
- **Database**: SQLite (for prototype)
- **Real-time**: WebSocket for live updates
- **Authentication**: JWT tokens

## Project Structure

```
unified-health-platform/
├── backend/           # Flask API server
├── frontend/          # React web application  
├── database/          # Database schema and migrations
├── docs/             # Documentation
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn
- Git (optional, for version control)

### Step 1: Backend Setup
```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Seed the database with demo data
python seed_demo_data.py

# Start the Flask server
python app.py
```
Backend will run on http://localhost:5000

### Step 2: Frontend Setup
```bash
cd frontend

# Install Node.js dependencies
npm install

# Start the React development server
npm start
```
Frontend will run on http://localhost:3000

## Demo Scenarios

### Patient Workflows
1. **Patient Registration**: Register with Aadhaar and create medical profile
   - Visit http://localhost:3000/patient/register
   - Fill in demo details (any 12-digit Aadhaar number)

2. **Patient Login & Dashboard**: Access patient dashboard
   - Use demo Aadhaar IDs: `123456789012`, `234567890123`, `345678901234`
   - View patient profile and quick actions

3. **Bed Search**: Real-time search for available beds in nearby hospitals
   - Browse available beds across 5+ hospitals
   - Filter by bed type (General, ICU, Emergency, Maternity)

4. **Medical Records**: View comprehensive health history across hospitals
   - Access unified medical records from multiple hospitals
   - View prescriptions, diagnoses, and treatment history

### Hospital Workflows
5. **Hospital Dashboard**: Manage bed availability and patient intake
   - Login as hospital administrator
   - Update bed status and manage hospital information

### Emergency Services
6. **Emergency Mode**: Critical patient bed allocation with priority routing
   - Quick emergency bed search
   - Priority booking for critical patients

## Demo Data

The project includes comprehensive demo data:

- **5 Hospitals**: AIIMS Delhi, Apollo Hospital, Fortis Gurgaon, Max Hospital, Safdarjung Hospital
- **150+ Beds**: Mix of General, ICU, Emergency, and Maternity beds across all hospitals
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

**Hospital Registration Numbers:**
- `AIIMS-DEL-001` - AIIMS New Delhi
- `APOLLO-DEL-002` - Apollo Hospital Delhi
- `FORTIS-GUR-003` - Fortis Hospital Gurgaon

## API Endpoints

- `/api/auth/login` - Patient authentication
- `/api/auth/register` - Patient registration
- `/api/patients` - Patient management
- `/api/hospitals` - Hospital registration and management
- `/api/beds` - Real-time bed availability
- `/api/records` - Medical records access
- `/api/emergency` - Emergency services integration

## Contributing

This is a hackathon prototype. Focus on core functionality and user experience.

## License

MIT License - Built for healthcare innovation hackathon.
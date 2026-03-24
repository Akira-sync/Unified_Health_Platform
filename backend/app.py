from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_socketio import SocketIO, emit, join_room, leave_room
import os
from datetime import datetime, timedelta
import uuid

from extensions import db # import db from extensions

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'healthcare-hackathon-secret-key'
app.config['JWT_SECRET_KEY'] = 'jwt-healthcare-secret'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///healthcare_platform.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
#db = SQLAlchemy(app)
cors = CORS(app)
jwt = JWTManager(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Import models
from models import Patient, Hospital, Bed, MedicalRecord, Appointment

# Import routes
from routes.patients import patients_bp
from routes.hospitals import hospitals_bp
from routes.beds import beds_bp
from routes.records import records_bp
from routes.emergency import emergency_bp
from routes.auth import auth_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(patients_bp, url_prefix='/api/patients')
app.register_blueprint(hospitals_bp, url_prefix='/api/hospitals')
app.register_blueprint(beds_bp, url_prefix='/api/beds')
app.register_blueprint(records_bp, url_prefix='/api/records')
app.register_blueprint(emergency_bp, url_prefix='/api/emergency')

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })

# WebSocket events for real-time updates
@socketio.on('connect')
def on_connect():
    print(f'Client connected: {request.sid}')
    emit('status', {'msg': 'Connected to Unified Health Platform'})

@socketio.on('disconnect')
def on_disconnect():
    print(f'Client disconnected: {request.sid}')

@socketio.on('join_hospital')
def on_join_hospital(data):
    hospital_id = data['hospital_id']
    join_room(f'hospital_{hospital_id}')
    emit('status', {'msg': f'Joined hospital {hospital_id} room'})

@socketio.on('leave_hospital')
def on_leave_hospital(data):
    hospital_id = data['hospital_id']
    leave_room(f'hospital_{hospital_id}')
    emit('status', {'msg': f'Left hospital {hospital_id} room'})

def broadcast_bed_update(hospital_id, bed_data):
    socketio.emit('bed_update', {
        'hospital_id': hospital_id,
        'bed_data': bed_data
    }, room=f'hospital_{hospital_id}')

# Create tables on startup
def create_tables():
    with app.app_context():
        db.create_all()
        print("Database tables created successfully")
        print("Tables available:", db.metadata.tables.keys()) # Debug Line

if __name__ == '__main__':
    create_tables() #call it once at startup
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
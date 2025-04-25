from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for external systems

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models import Client, Program, Enrollment

@app.route('/')
def home():
    return "Welcome to the Health Information System!"

# === Create Health Program ===
@app.route('/api/programs', methods=['POST'])
def create_program():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    if not name:
        return jsonify({'error': 'Program name is required'}), 400

    existing = Program.query.filter_by(name=name).first()
    if existing:
        return jsonify({'error': 'Program already exists'}), 409

    program = Program(name=name, description=description)
    db.session.add(program)
    db.session.commit()

    return jsonify({
        'message': 'Program created successfully',
        'program': {
            'id': program.id,
            'name': program.name,
            'description': program.description
        }
    }), 201

# === Register New Client ===
@app.route('/api/clients', methods=['POST'])
def register_client():
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')
    gender = data.get('gender')

    if not name or not age or not gender:
        return jsonify({'error': 'Name, age, and gender are required'}), 400

    client = Client(name=name, age=age, gender=gender)
    db.session.add(client)
    db.session.commit()

    return jsonify({
        'message': 'Client registered successfully',
        'client': {
            'id': client.id,
            'name': client.name,
            'age': client.age,
            'gender': client.gender
        }
    }), 201

# === Enroll Client in Programs ===
@app.route('/api/enroll', methods=['POST'])
def enroll_client():
    data = request.get_json()
    client_id = data.get('client_id')
    program_ids = data.get('program_ids')  # expects list

    if not client_id or not program_ids:
        return jsonify({'error': 'client_id and program_ids are required'}), 400

    client = Client.query.get(client_id)
    if not client:
        return jsonify({'error': 'Client not found'}), 404

    for pid in program_ids:
        program = Program.query.get(pid)
        if program and program not in client.programs:
            client.programs.append(program)

    db.session.commit()
    return jsonify({'message': 'Client enrolled in selected programs successfully'}), 200

# === Search Clients ===
@app.route('/api/clients/search', methods=['GET'])
def search_clients():
    query = request.args.get('q', '')
    results = Client.query.filter(Client.name.ilike(f'%{query}%')).all()

    clients = [{
        'id': client.id,
        'name': client.name,
        'age': client.age,
        'gender': client.gender
    } for client in results]

    return jsonify({'results': clients}), 200

# === View Client Profile (API) ===
@app.route('/api/clients/<int:client_id>', methods=['GET'])
def get_client_profile(client_id):
    client = Client.query.get(client_id)
    if not client:
        return jsonify({'error': 'Client not found'}), 404

    enrolled_programs = [{'id': p.id, 'name': p.name} for p in client.programs]

    return jsonify({
        'id': client.id,
        'name': client.name,
        'age': client.age,
        'gender': client.gender,
        'programs': enrolled_programs
    }), 200

if __name__ == '__main__':
    app.run(debug=True)

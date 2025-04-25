from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity
from models import User, db, TokenBlocklist
from flask import Flask, request, jsonify
from flask_restful import Resource
from datetime import datetime, timezone
from models import Program


# === Create Health Program ===
class CreateProgram(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        doctor_id = data.get('doctor_id')

        if not name or not doctor_id:
            return jsonify({'error': 'Program name and doctor_id are required'}), 400

        existing = Program.query.filter_by(name=name).first()
        if existing:
            return jsonify({'error': 'Program already exists'}), 409

        doctor = User.query.get(doctor_id)
        if not doctor:
            return jsonify({'error': 'Doctor not found'}), 404

        program = Program(name=name, description=description, doctor_id=doctor_id)
        db.session.add(program)
        db.session.commit()

        return jsonify({'message': 'Program created successfully', 'program': {
            'id': program.id,
            'name': program.name,
            'description': program.description,
            'doctor_id': program.doctor_id
        }}), 201

# === Fetch Health Program by Doctor ===
class GetProgramsByDoctor(Resource):
    def get(self, doctor_id):
        doctor = User.query.get(doctor_id)
        if not doctor:
            return {'error': 'Doctor not found'}, 404

        programs = [{
            'id': program.id,
            'name': program.name,
            'description': program.description
        } for program in doctor.programs]

        return {'doctor': doctor.full_name, 'programs': programs}


class GetProgram(Resource):
    def get(self, program_id):
        program = Program.query.get(program_id)
        if not program:
            return {'error': 'Program not found'}, 404

        doctor = User.query.get(program.doctor_id)  # Adjusted to use the program's doctor
        if not doctor:
            return {'error': 'Doctor not found'}, 404

        return {
            'id': program.id,
            'name': program.name,
            'description': program.description,
            'doctor': {
                'username': doctor.username,
                'full_name': doctor.full_name
            }
        }


#=== Fetch all programs and their enrolled clients===
class GetAllPrograms(Resource):
    @jwt_required()
    def get(self):
        programs = Program.query.all()
        output = []

        for program in programs:
            clients = [{
                'id': e.client.id,
                'name': e.client.full_name,
                'age': e.client.age,
                'gender': e.client.gender
            } for e in program.enrollments]

            program_data = {
                'id': program.id,
                'name': program.name,
                'description': program.description,
                'clients': clients
            }
            output.append(program_data)

        return jsonify({'programs': output})

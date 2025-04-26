from flask_jwt_extended import  jwt_required
from models import User, db, Enrollment
from flask import Flask, request, jsonify
from flask_restful import Resource
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
            return {'error': 'Program name and doctor_id are required'}, 400

        name = data.get('name', '').strip().lower()
        existing = Program.query.filter(db.func.lower(Program.name) == name).first()
        if existing:
            return {'error': 'Program already exists'}, 409

        doctor = User.query.get(doctor_id)
        if not doctor:
            return {'error': 'Doctor not found'}, 404

        program = Program(name=name, description=description, doctor_id=doctor_id)
        db.session.add(program)
        db.session.commit()

        return {
            'message': 'Program created successfully',
            'program': {
                'id': program.id,
                'name': program.name,
                'description': program.description,
                'doctor_id': program.doctor_id
            }
        }, 201

#=== Update a program's details===
class UpdateProgram(Resource):
    @jwt_required()
    def put(self, program_id):
        program = Program.query.get(program_id)
        if not program:
            return {'error': 'Program not found'}, 404

        data = request.get_json()
        name = data.get('name')
        description = data.get('description')

        if name:
            # Check if a program with the new name already exists 
            existing = Program.query.filter(Program.name == name, Program.id != program_id).first()
            if existing:
                return {'error': 'Another program with this name already exists'}, 409
            program.name = name

        if description:
            program.description = description

        db.session.commit()

        return {
            'message': 'Program details updated successfully',
            'program': {
                'id': program.id,
                'name': program.name,
                'description': program.description,
                'doctor_id': program.doctor_id
            }
        }, 200


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

#===Fetch a single program===

class GetProgram(Resource):
    def get(self, program_id):
        program = Program.query.get(program_id)
        if not program:
            return {'error': 'Program not found'}, 404

        doctor = User.query.get(program.doctor_id) 
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

# Delete a program and enrollments linked to it
class DeleteProgram(Resource):
    @jwt_required()
    def delete(self, program_id):
        program = Program.query.get(program_id)
        
        if not program:
            return {'error': 'Program not found'}, 404
        
        # First, delete all enrollments linked to this program
        Enrollment.query.filter_by(program_id=program.id).delete()

        # Then, delete the program itself
        db.session.delete(program)
        db.session.commit()

        return {'message': 'Program and its enrollments deleted successfully'}, 200

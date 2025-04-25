from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity
from models import User, db, TokenBlocklist, Client, Enrollment, Program
from flask import Flask, request, jsonify
from flask_restful import Resource
from datetime import datetime, timezone


# === Register New Client ===
class RegisterClient(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        name = data.get('name')
        age = data.get('age')
        gender = data.get('gender')

        if not name or not age or not gender:
            return {'error': 'Name, age, and gender are required'}, 400

        client = Client(full_name=name, age=age, gender=gender)  # ✅ fix: full_name not name
        db.session.add(client)
        db.session.commit()

        return {
            'message': 'Client registered successfully',
            'client': {
                'id': client.id,
                'name': client.full_name,
                'age': client.age,
                'gender': client.gender
            }
        }, 201


# === Enroll Client in Programs ===
from flask import jsonify

class EnrollClient(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        client_id = data.get('client_id')
        program_ids = data.get('program_ids')

        # Validate input
        if not client_id or not program_ids:
            return jsonify({'error': 'client_id and program_ids are required'}), 400

        # Find the client by ID
        client = Client.query.get(client_id)
        if not client:
            return jsonify({'error': 'Client not found'}), 404

        enrolled_programs = []

        # Iterate over the program IDs and enroll the client
        for pid in program_ids:
            program = Program.query.get(pid)
            if not program:
                continue  # Skip if program doesn't exist

            existing_enrollment = Enrollment.query.filter_by(client_id=client.id, program_id=program.id).first()
            if not existing_enrollment:
                enrollment = Enrollment(client_id=client.id, program_id=program.id)
                db.session.add(enrollment)
                enrolled_programs.append(program.name)

        db.session.commit()

        # Return the response as JSON
        return jsonify({
            'message': 'Client enrolled in selected programs successfully',
            'client_id': client.id,
            'enrolled_programs': enrolled_programs
        }), 200



# === Search Clients ===
class SearchClients(Resource):
    @jwt_required()
    def get(self):
        query = request.args.get('q', '').strip()

        if not query:
            return jsonify({'error': 'Search query is required'}), 400

        results = Client.query.filter(Client.full_name.ilike(f'%{query}%')).all()

        clients = [{
            'id': client.id,
            'name': client.full_name,
            'age': client.age,
            'gender': client.gender
        } for client in results]

        return ({
            'count': len(clients),
            'results': clients
        }), 200


# === View Client Profile (API) ===
class GetClientProfile(Resource):
    @jwt_required()
    def get(self, client_id):
        client = Client.query.get(client_id)

        if not client:
            return jsonify({'error': 'Client not found'}), 404

        enrollments = Enrollment.query.filter_by(client_id=client.id).all()

        programs = [{
            'id': e.program.id,
            'name': e.program.name,
            'description': e.program.description
        } for e in enrollments]

        return jsonify({
            'id': client.id,
            'name': client.full_name,
            'age': client.age,
            'gender': client.gender,
            'programs': programs
        })

# ===Fetch all clients and their programs===
class GetAllClients(Resource):
    @jwt_required()
    def get(self):
        clients = Client.query.all()
        output = []

        for client in clients:
            programs = [{'id': p.id, 'name': p.name} for p in client.programs]
            client_data = {
                'id': client.id,
                'name': client.full_name,
                'age': client.age,
                'gender': client.gender,
                'programs': programs
            }
            output.append(client_data)

        return jsonify({'clients': output})

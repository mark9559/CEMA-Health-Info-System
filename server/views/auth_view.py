from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity
from models import User, db, TokenBlocklist
from flask import Flask, request, jsonify
from flask_restful import Resource
from datetime import datetime, timezone


# Login User
class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Validate user credentials
        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            return jsonify({'error': 'Invalid credentials'}), 401

        # Create JWT token
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token)

# Get authenticated user

class AuthenticatedUser(Resource):
    @jwt_required()  # Ensure the user is authenticated with JWT
    def get(self):
        # Get the identity (user ID) of the authenticated user from the JWT
        user_id = get_jwt_identity()
        
        # Fetch the user from the database
        user = User.query.get(user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Return the user's details
        return jsonify({
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name
        })

# Log Out
class Logout(Resource):
    @jwt_required()
    def delete(self):
        # Get the unique identifier (JTI) from the current JWT token
        jti = get_jwt()["jti"]
        now = datetime.now(timezone.utc)

        # Add the JTI to the blocklist table
        db.session.add(TokenBlocklist(jti=jti, created_at=now))
        db.session.commit()

        return jsonify(msg="Logged out successfully")

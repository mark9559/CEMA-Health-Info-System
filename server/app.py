from models import Client, Program, Enrollment, User, db
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager,jwt_required, get_jwt_identity
from views import *
from datetime import timedelta
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
CORS(app)  # Enable CORS for external systems

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

api = Api(app)
jwt = JWTManager(app)

db = SQLAlchemy(app)

# Custom token validation handler
@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    # Check if the JTI is in the blocklist table
    token = TokenBlocklist.query.filter_by(jti=jti).first()
    if token:
        return True  # Token is in the blocklist, so it's invalid
    return False


# Adding resources
api.add_resource(RegisterDoctor, '/register')
api.add_resource(CreateProgram, '/programs')
api.add_resource(GetProgram, '/programs/<int:program_id>')
api.add_resource(GetProgramsByDoctor, '/doctors/<int:doctor_id>/programs')
api.add_resource(RegisterClient, '/clients')
api.add_resource(EnrollClient, '/enroll')
api.add_resource(SearchClients, '/clients/search')
api.add_resource(GetClientProfile, '/clients/<int:client_id>')
api.add_resource(GetAllClients, '/clients')
api.add_resource(GetAllPrograms, '/programs')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(AuthenticatedUser, '/user')

@app.route('/')
def home():
    return "Welcome to the Health Information System!"


    






if __name__ == '__main__':
    app.run(debug=True)

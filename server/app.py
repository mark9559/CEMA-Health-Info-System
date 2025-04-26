import os
from flask_sqlalchemy import SQLAlchemy
from models import  db, TokenBlocklist
from flask import Flask
from flask_migrate import Migrate

from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_restful import Api
from dotenv import load_dotenv
from views import *

load_dotenv()

app = Flask(__name__)
api = Api(app)
CORS(app)  # Enable CORS for external systems

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)


jwt = JWTManager(app)
jwt.init_app(app)
db.init_app(app)
#db = SQLAlchemy(app)
migrate = Migrate(app, db)

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
api.add_resource(GetAllDoctors, '/doctors')
api.add_resource(UpdateDoctor, '/doctors/<int:doctor_id>')
api.add_resource(DeleteDoctor, '/doctors/<int:doctor_id>/delete')
api.add_resource(CreateProgram, '/programs')
api.add_resource(GetProgram, '/programs/<int:program_id>')
api.add_resource(UpdateProgram, '/programs/<int:program_id>')
api.add_resource(GetProgramsByDoctor, '/doctors/<int:doctor_id>/programs')
api.add_resource(DeleteProgram, '/programs/<int:program_id>')
api.add_resource(RegisterClient, '/clients')
api.add_resource(UpdateClient, '/clients/<int:client_id>')
api.add_resource(DeleteClient, '/clients/<int:client_id>')
api.add_resource(EnrollClient, '/enroll')
api.add_resource(UnenrollClient, '/clients/unenroll')
api.add_resource(SearchClients, '/api/clients/search')
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

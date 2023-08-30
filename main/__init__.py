from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from main.models import *
from main.config import LocalDevelopmentConfig
from flask import Flask
import os
from flask_restful import Api
from main.api import *
from flask import Flask, render_template_string
from flask_security import Security, current_user, auth_required, hash_password, \
     SQLAlchemySessionUserDatastore, permissions_accepted
from main.database import db_session, init_db
from flask_jwt_extended import create_access_token, JWTManager

app = Flask(__name__)
app.config.from_object(LocalDevelopmentConfig)
from main.controllers import *

user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
app.security = Security(app, user_datastore)


app.config["SECURITY_EMAIL_VALIDATOR_ARGS"] = {"check_deliverability": False}
api=Api(app)
# jwt=JWTManager(app)

with app.app_context():
    init_db()

class UserResource(Resource):
    def post(self):
        print("HERE")
        data = request.get_json()
        if not data:
            return {'Error': 'REQUEST001'}, 400

        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        roles = data.get('roles')
        attributes = data.get('attributes')

        if not email or not username or not password or not roles:
            return {'Error': 'REQUEST001'}, 400
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return {'message': 'User with this email already exists'}, 400

        try:
            app.security.datastore.create_user(email=email,username=username, password=hash_password(password), roles=[roles],attributes=attributes.split(", "))
            # db_session.add(User(username=username,email=email,password=hash_password(password),active=1,attributes=attributes.split(",")))
            # db_session.add(RolesUsers(user_id=User.query.filter_by(username=username).first().id,role_id=Role.query.filter_by(name=roles).first().id))
            db_session.commit()

            return {'message': 'User created successfully'}, 201
        except Exception as e:
            print(e)
            return {"Error":"USER001"},400


api.add_resource(ExperienceResource,"/user/experience","/user/experience/<int:exp_id>")
api.add_resource(UserResource,'/user' ,'/user-register')
api.add_resource(QuestionResource,"/question")
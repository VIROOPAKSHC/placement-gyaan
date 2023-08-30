from main.models import *
from main.database import db_session
from flask_restful import Resource,Api
from werkzeug.exceptions import HTTPException
from flask import request,make_response
import json
from flask_security import auth_required, login_required, roles_accepted, roles_required, auth_token_required,current_user
from flask_restful import Api, Resource, reqparse
from flask_security import SQLAlchemyUserDatastore, Security
from flask_sqlalchemy import SQLAlchemy
from main import app, api
from datetime import datetime
class UserResource(Resource):

    def post(self):
        data = request.get_json()
        if not data:
            return {'message': 'No input data provided'}, 400

        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        roles = data.get('roles')
        attributes = data.get('attributes')

        if not email or not username or not password or not roles:
            return {'message': 'Missing required fields'}, 400

        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return {'message': 'User with this email already exists'}, 400

        
        app.security.datastore.create_user(email=email,username=username, password=hash_password(password), roles=[role],attributes=attributes.split(", "))

        db_session.commit()

        return {'message': 'User created successfully'}, 201

class ExperienceResource(Resource):
    def get(self, user_id):        
        rows = db_session.query(Experience).all()

        if not experiences:
            return {'message': 'No experiences found'}, 404

        exps = []
        for i in rows:
            user=User.query.filter_by(id=i.auth_id).first()
            temp = {}
            temp["title"] = i.title
            temp["description"] = i.description
            temp["author"] = user.username
            temp["anonymous"] = i.anonymous
            temp["timestamp"] = i.timestamp

            exps.append(temp)

        return {'experiences': exps}

    def post(self):
        data = request.get_json()
        if not data:
            return {'message': 'No input data provided'}, 400

        title = data.get('title')
        description = data.get('description')
        anonymous = data.get('anonymous')
        user_id = data.get('user_id')

        if not title or description or anonymous:
            return {'message': 'Missing required fields'}, 400

        experience = Experience(title=title, description=description, anonymous=anonymous, auth_id=user_id, timestamp = datetime.utcfromtimestamp(datetime.now().timestamp()).strftime("%H:%M %d/%m/%y"))
        db_session.add(experience)
        db_session.commit()
        
        return {'message': 'Experience created successfully'}, 201

api.add_resource(UserResource, '/user')
api.add_resource(ExperienceResource, '/experience')
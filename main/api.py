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
# from main import app, api
import datetime as dt


class UserResource(Resource):
    def post(self):
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
            app.security.datastore.create_user(email=email,username=username, password=hash_password(password), roles=[role],attributes=attributes.split(", "))

            db_session.commit()

            return {'message': 'User created successfully'}, 201
        except:
            return {"Error":"USER001"}

class ExperienceResource(Resource):
    @auth_required("token")
    def get(self):        
        rows = db_session.query(Experience).all()

        if not rows:
            return {'message': 'No experiences found'}, 404

        exps = []
        for i in rows:
            user=User.query.filter_by(id=i.auth_id).first()
            temp = {}
            temp["id"]=i.id
            temp["title"] = i.title
            temp["description"] = i.description
            temp["anonymous"] = i.anonymous
            if temp["anonymous"]:
                temp["author"]="anonymous"
            else:
                temp["author"] = user.username
            
            temp["timestamp"] = i.timestamp

            exps.append(temp)

        return {'experiences': exps}

    @auth_required("token")
    def post(self):
        data = request.get_json()
        if not data:
            return {'Error': 'REQUEST001'}, 400

        title = data.get('title')
        description = data.get('description')
        anonymous = int(data.get('anonymous'))
        user_id=current_user.id

        if not( title or description or anonymous):
            return {'Error': 'REQUEST001'}, 400
        try:

            experience = Experience(title=title, description=description, anonymous=anonymous, auth_id=user_id, timestamp = dt.datetime.now())
            db_session.add(experience)
            db_session.commit()
            return {'message': 'Experience created successfully'}, 200
        except:
            db_session.rollback()
            if Experience.query.filter_by(title=title).first():
                return {"Error":"EXPE001"}
            
            return {"Error" : "Unknown Error"},403

    @auth_required("token")
    def put(self,exp_id):
        data = request.get_json()
        if not Experience.query.filter_by(id=exp_id).first():
            return {"Error":"EXPE001"},403
        if not data:
            return {'Error': 'No input data provided'}, 400

        title = data.get('title')
        description = data.get('description')
        try:
            exp=Experience.query.filter_by(id=exp_id).first()
            if exp.auth_id==current_user.id:
                if Experience.query.filter_by(title=title).first():
                    return {"Error":"EXPE003"},403
                exp.title=title
                exp.description=description
                db_session.commit()
                return {'message': 'Experience edited successfully'}, 200
            else:
                return {"Error": "USER002"},403
        except:
            db_session.rollback()
            return {"message" : "Failed to edit experience"},403

    @auth_required("token")
    def delete(self,exp_id):
        try:
            exp=Experience.query.filter_by(id=exp_id).first()
            if exp.auth_id==current_user.id:
                db_session.delete(exp)
                db_session.commit()
                return {"Message":"Experience successfully deleted"},200
            else:
                return {"Error":"EXPE002"}, 400
        except:
            return {"Error" : "EXPE001"}, 400

class QuestionResource(Resource):
    @auth_required("token")
    def get(self):
        try:
            ques=Question.query.all()
            l=[]
            for que in ques:
                d={}
                d['id']=(que.id)
                d['question']=(que.question)
                d['choices']=(que.choices.split(","))
                d["correct-choice"]=que.correct_choice
                d['answer']=(que.answer)
                d["type"]=que.type
                d["author"]=User.query.filter_by(id=que.auth_id).first().username
                d["timestamp"]=que.timestamp
                l.append(d)
            return {"questions":l},200
        except Exception as e:
            print(e)
            return {"Error":"No Questions in the database"},400

    @auth_required("token")
    def post(self):
        data=request.get_json()
        if not data:
            return {'Error': 'REQUEST001'}, 400

        question = data.get('question')
        if Question.query.filter_by(question=question).first():
            return {"Error":"Question name already exists"},403
        answer = data.get('answer')
        choices = data.get('choices')
        type=data.get("type")
        timestamp=dt.datetime.now()
        correct_choice=data.get("correct_choice",-1)
        user_id=current_user.id
        if type not in ["aptitude","technical"]:
            return {"Error":"type should be either aptitude or technical"},400
        if not( question or answer or choices or type):
            return {'Error': 'REQUEST001'}, 400
        try:

            question = Question(question=question,answer=answer,choices=choices,type=type,timestamp=timestamp,auth_id=user_id,correct_choice=correct_choice)
            db_session.add(question)
            db_session.commit()
            return {'message': 'Question added successfully'}, 200
        except:
            db_session.rollback()
            
            
            return {"Error" : "Unknown Error"},403
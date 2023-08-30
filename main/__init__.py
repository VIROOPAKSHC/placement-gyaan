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
from flask_socketio import SocketIO,emit
import datetime as dt

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

socketio=SocketIO(app)

@app.route("/chat/<username>")
@auth_required()
def chatting(username):
  if not User.query.filter_by(username=username).first():
    return "No such username, provide valid username"
  user=User.query.filter_by(username=username).first()
  messages=[]
  for msg in Message.query.all():
    d={}
    if (msg.sender==user.id and msg.recipient==current_user.id):
      d["sender"]=user.username
      d["recipient"]=current_user.username
      d["content"]=msg.message
    elif (msg.sender==current_user.id and msg.recipient==user.id):
      d["sender"]=current_user.username
      d["recipient"]=user.username
      d["content"]=msg.message

    messages.append(d)
  return render_template("chat.html",messages=messages,sender=current_user,recipient=user)


@socketio.on('message')
def handle_message(data):
    print("Hi")
    sender = data['sender']
    recipient = data['recipient']
    content = data['content']
    message = Message(sender=User.query.filter_by(username=sender).first().id, recipient=User.query.filter_by(username=recipient).first().id, message=content)
    db_session.add(message)
    db_session.commit()
    emit('message', {'sender': sender, 'content': content}, broadcast=True)


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
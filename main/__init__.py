from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from main.models import *
from main.config import LocalDevelopmentConfig
from flask import Flask
import os

from flask import Flask, render_template_string
from flask_security import Security, current_user, auth_required, hash_password, \
     SQLAlchemySessionUserDatastore, permissions_accepted
from main.database import db_session, init_db

app = Flask(__name__)
app.config.from_object(LocalDevelopmentConfig)
from main.controllers import *

user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
app.security = Security(app, user_datastore)


app.config["SECURITY_EMAIL_VALIDATOR_ARGS"] = {"check_deliverability": False}


with app.app_context():
    init_db()
    # Create a user and role to test with
    app.security.datastore.find_or_create_role(
        name="user",permissions={"user-read","user-write"}
    )
    db_session.commit()
    if not app.security.datastore.find_user(email="test@me.com"):
        app.security.datastore.create_user(email="test@me.com",username="testuser",
        password=hash_password("password"), roles=["user"])
    db_session.commit()


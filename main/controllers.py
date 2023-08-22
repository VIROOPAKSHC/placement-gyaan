from main import app
from main.database import db_session
from main.models import *
from flask_security import Security, current_user, auth_required, hash_password, \
     SQLAlchemySessionUserDatastore, permissions_accepted,login_required
from flask import render_template,render_template_string,redirect
@app.route('/')
def index():
  return redirect("/home")

@app.route('/hi')
@login_required
def hi():
  return " ".format(dir(current_user))

# @app.route('/favicon.ico') 
# def favicon(): 
#   return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/home")
@auth_required()
def user_home():
    # print(dir(current_user))
    # print("Current user : ")
    # print(current_user.attributes)
    # print(db_session.query())
    # print(current_user)
    # role=Role.query.filter_by(id=(RolesUsers.query.filter_by(user_id=current_user.id).first().role_id)).first()
    # print(role.id,role.name,role.description,role.permissions)
    return render_template("home.html")

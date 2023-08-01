from main import app
from flask_security import Security, current_user, auth_required, hash_password, \
     SQLAlchemySessionUserDatastore, permissions_accepted,login_required
from flask import render_template,render_template_string

@app.route('/')
def index():
  if current_user.is_active:
    return "IS ACTIVE"+"{}".format(current_user.get_id())
  else:
    return "NOT ACTIVE"

@app.route('/hi')
@login_required
def hi():
  return " ".format(dir(current_user))

@app.route('/favicon.ico') 
def favicon(): 
  return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/home")
@auth_required()
def user_home():
    return render_template_string("Hello {{ current_user.email }} you are a user!")

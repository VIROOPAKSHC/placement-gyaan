from main import app
from main.database import db_session
from main.models import *
from flask_security import Security, current_user, auth_required, hash_password, \
     SQLAlchemySessionUserDatastore, permissions_accepted,login_required
from flask import render_template,render_template_string,redirect, request, url_for
from main.forms import RegistrationForm

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

@app.route('/register', methods=['GET', 'POST'])
def register():
  form = RegistrationForm(request.form)
  if form.validate_on_submit():
    email = form.email.data
    username = form.username.data
    password = form.password.data
    role = form.role.data

    attributes = []
    if role == 'student':
      year_of_study = form.year_of_study.data
      department = form.department.data
      attributes = [year_of_study, department]

    elif role == 'senior':
      years_of_experience = form.years_of_experience.data
      company = form.company.data
      attributes = [years_of_experience, company]

    elif role == 'aspiring':
      skills = form.skills.data
      desired_role = form.desired_role.data
      attributes = [skills, desired_role]

    app.security.datastore.create_user(email=email,username=username, password=hash_password(password), roles=[role],attributes=[str(item) for item in attributes])

    db_session.commit()
      
    return redirect('/home')

    # Render the registration form template
  return render_template('register.html', form=form)


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

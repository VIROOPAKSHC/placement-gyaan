from main import app
from main.database import db_session
from main.models import *
from flask_security import Security, current_user, auth_required, hash_password, \
     SQLAlchemySessionUserDatastore, permissions_accepted,login_required
from flask import render_template,render_template_string,redirect, request, url_for
from main.forms import RegistrationForm
import datetime as dt

def extract_time(timestamp):
  time_and_date=dt.datetime.strptime(str(timestamp).split(".")[0],"%Y-%m-%d %H:%M:%S")
  return dt.datetime.strftime(time_and_date,"%d %b,%Y %I:%M %p")

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
    return render_template("home.html",user=current_user)

@app.route("/assessment")
@auth_required()
def user_assessment():
  return render_template("assessment.html")

@app.route("/connect")
@auth_required()
def user_connect():
  return render_template("connect.html")

def extract(type):
  questions=[]
  for question in Question.query.filter_by(type=type).all():
    l=[]
    l.append(-1)
    l.append(question.question)
    l.append(User.query.filter_by(id=question.auth_id).first().username)
    l.append(extract_time(question.timestamp))
    l.append(question.id)
    questions.append(l)
  questions.sort(key=lambda x:x[3],reverse=True)
  c=1
  for que in questions:
    que[0]=c
    c+=1
  return questions


@app.route("/aptitude")
@auth_required()
def aptitude_question():
  # print(extract("aptitude"))
  return render_template("questions.html",type="Aptitude",questions=extract("Aptitude"))

@app.route("/technical")
@auth_required()
def technical_question():
  
  return render_template("questions.html",type="Technical",questions=extract("Technical"))

@app.route('/view_question/<int:question_id>')
@auth_required()
def view_question(question_id):
    question = Question.query.get(question_id)
    user=User.query.filter_by(id=question.auth_id).first()
    return render_template('view_question.html', question=question,username=user.username)


@app.route("/add-question",methods=["GET","POST"])
@auth_required()
def add_question():
  if request.method=="GET":
    return render_template("add-question.html")
  else:
    question = request.form['question']
    answer = request.form['answer']
    choices = request.form['choices']
    type = request.form['category']
    correct_choice = request.form.get('correct_choice')

    new_question = Question(
        question=question,
        answer=answer,
        choices=choices,
        type=type,
        auth_id=current_user.id,
        timestamp=dt.datetime.now(),
        correct_choice=correct_choice
    )

    try:
        db_session.add(new_question)
        db_session.commit()
        message = "Question added successfully!"
    except Exception as e:
        db_session.rollback()
        message = f"Error: {str(e)}"
        if Question.query.filter_by(question=question).first():
          message="Question already exists, add a different question or change the question name"
        

    return render_template('add-question.html', message=message)

@app.route("/experience")
@auth_required()
def experiences():
  exps=[]

  for exp in Experience.query.all():
    l=[]
    l.append(-1)
    l.append(exp.title)
    l.append(User.query.filter_by(id=exp.auth_id).first().username)
    l.append(extract_time(exp.timestamp))
    l.append(str(exp.id))
    l.append(exp.anonymous)
    exps.append(l)
  exps.sort(key=lambda x:x[3],reverse=True)
  c=1
  for exp in exps:
    exp[0]=c
    c+=1
  return render_template("experiences.html",experiences=exps)

@app.route("/add-experience",methods=["GET","POST"])
@auth_required()
def add_experience():
  if request.method=="GET":
    return render_template("add-experience.html")
  else:
    title = request.form['title']
    description = request.form['description']
    anonymous = request.form['anonymous']

    new_experience = Experience(
        title=title,
        description=description,
        anonymous=1 if anonymous=="yes" else 0,
        auth_id=current_user.id,
        timestamp=dt.datetime.now()
    )

    try:
        db_session.add(new_experience)
        db_session.commit()
        message = "Experience added successfully!"
    except Exception as e:
        db_session.rollback()
        message = f"Error: {str(e)}"
        if Experience.query.filter_by(title=title).first():
          message="Title already exists for another experience, add a different experience or change the title"
        

    return render_template('add-experience.html', message=message)

@app.route('/view_experience/<int:exp_id>')
@auth_required()
def view_experience(exp_id):
    experience = Experience.query.get(exp_id)
    user=User.query.filter_by(id=experience.auth_id).first()
    return render_template('view_experience.html', experience=experience,username=user.username,timestamp=extract_time(experience.timestamp))

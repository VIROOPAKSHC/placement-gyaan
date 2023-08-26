from wtforms import Form, StringField, PasswordField, SelectField, IntegerField, validators, TextAreaField
from flask_wtf import FlaskForm

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email()], render_kw={"placeholder": "Enter your email"})
    username = StringField('Username', validators=[validators.DataRequired()], render_kw={"placeholder": "Choose a username"})
    password = PasswordField('Password', validators=[validators.DataRequired()], render_kw={"placeholder": "Enter a password"})
    confirm_password = PasswordField('Confirm Password', validators=[validators.DataRequired(), validators.EqualTo('password', message='Passwords must match')], render_kw={"placeholder": "Confirm your password"})

    role = SelectField('Role', choices=[
        ('student', 'Student'),
        ('senior', 'Senior'),
        ('aspiring', 'Aspiring Candidate')
    ], render_kw={"placeholder": "Select your role"})

    # Fields for Student
    year_of_study = IntegerField('Year of Study', [validators.Optional()], render_kw={"placeholder": "Year of Study"})
    department = StringField('Department', [validators.Optional()], render_kw={"placeholder": "Department"})

    # Fields for Senior
    years_of_experience = IntegerField('Years of Experience', [validators.Optional()], render_kw={"placeholder": "Years of Experience"})
    company = StringField('Company', [validators.Optional()], render_kw={"placeholder": "Company"})

    # Fields for Aspiring Candidate
    skills = TextAreaField('Skills', [validators.Optional()], render_kw={"placeholder": "Skills"})
    desired_role = StringField('Desired Role', [validators.Optional()], render_kw={"placeholder": "Desired Role"})

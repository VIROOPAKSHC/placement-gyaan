from main.database import Base
from flask_security import UserMixin, RoleMixin,AsaList
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import Boolean, DateTime, Column, Integer, \
                    String, ForeignKey

class RolesUsers(Base):
    __tablename__ = 'RolesUsers'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))

class Role(Base, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))
    permissions = Column(MutableList.as_mutable(AsaList()),nullable=False)

class User(Base, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255), unique=True, nullable=True)
    password = Column(String(255), nullable=False)
    # last_login_at = Column(DateTime())
    # current_login_at = Column(DateTime())
    # last_login_ip = Column(String(100))
    # current_login_ip = Column(String(100))
    # login_count = Column(Integer)
    active = Column(Boolean())
    fs_uniquifier = Column(String(64), unique=True, nullable=False)
    # confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary='RolesUsers',
                         backref=backref('users', lazy='dynamic'))


# Question Model
class Question(Base):
	__tablename__='Question'
	id = Column(Integer, primary_key=True)
	question = Column(String(255), unique=True, nullable=False)
	answer = Column(Integer, nullable=False)
	choices = Column(String(255), nullable=False)
	type = Column(String(80), nullable=False)
	auth_id = Column(Integer, ForeignKey('User.id'), nullable=False)
	timestamp = Column(String(80), nullable=False)
	correct_choice = Column(String(80))

	# Relationships
	# author = relationship('User', backref='Question')

# Experience Model
class Experience(Base):
	__tablename__="Experience"
	id = Column(Integer, primary_key=True)
	title = Column(String(255), unique=True, nullable=False)
	description = Column(String(255), nullable=False)
	auth_id = Column(Integer, ForeignKey('User.id'), nullable=False)
	anonymous = Column(Boolean, default=False)
	timestamp = Column(String(80), default=0)

	# Relationships
	# author = relationship('User', backref='experiences')

# Student Model
class Student(Base):
	__tablename__="Student"
	id = Column(Integer, primary_key=True)
	yearOfStudy = Column(Integer, nullable=False)
	department = Column(String(120), nullable=False)

# Senior Model
class Senior(Base):
	__tablename__="Senior"
	id = Column(Integer, primary_key=True)
	yearsOfExperience = Column(Integer, nullable=False)
	Company = Column(String(120))

# AspCandidate Model
class AspCandidate(Base):
	__tablename__='AspCandidate'
	id = Column(Integer, primary_key=True)
	skills = Column(String(), nullable=False)
	desiredRoles = Column(String())

# UserCandidate Model (Association table for User and AspCandidate)
class UserCandidate(Base):
	__tablename__="UserCandidate"
	user_id = Column(Integer, ForeignKey('User.id'), primary_key=True)
	cand_id = Column(Integer, ForeignKey('AspCandidate.id'), primary_key=True)

# UserSenior Model (Association table for User and Senior)
class UserSenior(Base):
	__tablename__="UserSenior"
	user_id = Column(Integer, ForeignKey('User.id'), primary_key=True)
	senior_id = Column(Integer, ForeignKey('Senior.id'), primary_key=True)

# UserStudent Model (Association table for User and Student)
class UserStudent(Base):
	__tablename__="UserStudent"
	user_id = Column(Integer, ForeignKey('User.id'), primary_key=True)
	student_id = Column(Integer, ForeignKey('Student.id'), primary_key=True)

# Admin Model
class Admin(Base):
	__tablename__='Admin'
	id = Column(Integer, primary_key=True)
	position = Column(String(120))

# UserAdmin Model (Association table for User and Admin)
class UserAdmin(Base):
	__tablename__="UserAdmin"
	user_id = Column(Integer, ForeignKey('User.id'), primary_key=True)
	admin_id = Column(Integer, ForeignKey('Admin.id'), primary_key=True)


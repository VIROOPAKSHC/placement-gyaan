from main.database import Base
from flask_security import UserMixin, RoleMixin,AsaList
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import Boolean, DateTime, Column, Integer, \
                    String, ForeignKey

class RolesUsers(Base):
    __tablename__ = 'RolesUsers'
    id = Column(Integer(), primary_key=True,autoincrement=True)
    user_id = Column('user_id', Integer(), ForeignKey('User.id'))
    role_id = Column('role_id', Integer(), ForeignKey('Role.id'))

class Role(Base, RoleMixin):
    __tablename__ = 'Role'
    id = Column(Integer(), primary_key=True,autoincrement=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))
    permissions = Column(MutableList.as_mutable(AsaList()),nullable=False)

class User(Base, UserMixin):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True,autoincrement=True)
    email = Column(String(255), unique=True)
    username = Column(String(255), unique=False, nullable=True)
    password = Column(String(255), nullable=False)
    active = Column(Boolean())
    fs_uniquifier = Column(String(64), unique=True, nullable=False)
    attributes=Column(MutableList.as_mutable(AsaList()),nullable=False)
    roles = relationship('Role', secondary='RolesUsers',
                         backref=backref('Users', lazy='dynamic'))


# attributes should be:
# For the Admin:
# 	position
# For Senior:
# 	yearsOfExperience
# 	company
# For Student:
# 	yearOfStudy
# 	department
# For Aspiring Candidate:
# 	skills
# 	desiredRoles


# Question Model
class Question(Base):
	__tablename__='Question'
	id = Column(Integer, primary_key=True,autoincrement=True)
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
	id = Column(Integer, primary_key=True,autoincrement=True)
	title = Column(String(255), unique=True, nullable=False)
	description = Column(String(255), nullable=False)
	auth_id = Column(Integer, ForeignKey('User.id'), nullable=False)
	anonymous = Column(Boolean, default=False)
	timestamp = Column(String(80), default=0)

	# Relationships
	# author = relationship('User', backref='experiences')

# Chat Model
class Chat(Base):
	__tablename__="Chat"
	id=Column(Integer,primary_key=True,autoincrement=True)
	user1=Column(Integer,ForeignKey("User.id"),nullable=False)
	user2=Column(Integer,ForeignKey("User.id"),nullable=False)

class Message(Base):
	__tablename__="Message"
	id=Column(Integer,primary_key=True,autoincrement=True)
	message=Column(String(512),nullable=False)
	chat_id=Column(Integer,ForeignKey("Chat.id"))

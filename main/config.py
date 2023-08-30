import os
import secrets
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "auth_token"

# Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
# Generate a good salt using: secrets.SystemRandom().getrandbits(128)

class LocalDevelopmentConfig(Config):
    # SQLITE_DB_DIR = os.path.join(basedir)
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, 'database.db')
    DEBUG = True
    SECRET_KEY =  os.environ.get("SECRET_KEY", secrets.token_hex(16)) #Strong,random and can be in the env
    SECURITY_PASSWORD_HASH = "bcrypt"    
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634') # Read from ENV in your case
    SECURITY_LOGIN_USER_TEMPLATE='login.html'
    SECURITY_REGISTERABLE=True
    SECURITY_POST_LOGIN_VIEW = '/home'
    REMEMBER_COOKIE_SAMESITE = "strict"
    SESSION_COOKIE_SAMESITE = "strict" # have session and remember cookie be samesite (flask/flask_login)
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    WTF_CSRF_ENABLED = False




class StageConfig(Config):
    # SQLITE_DB_DIR = os.path.join(basedir)
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, 'database.db')
    DEBUG = True
    SECRET_KEY =  'Random Hashed Key' #Strong,random and should be in the evn
    SECURITY_PASSWORD_HASH = "bcrypt"    
    SECURITY_PASSWORD_SALT = 'Other Random Hashed KEY' # Read from ENV in your case
    SECURITY_REGISTERABLE = True
    SECURITY_CONFIRMABLE = False
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_DEFAULT_REMEMBER_ME=False
    SECURITY_UNAUTHORIZED_VIEW = None
    SECURITY_LOGIN_USER_TEMPLATE='login.html'
    # SECURITY_POST_LOGOUT_VIEW = '/login'
    # SECURITY_POST_LOGIN_VIEW = '/dashboard'
    # SECURITY_POST_REGISTER_VIEW = '/login'
    WTF_CSRF_ENABLED = False
    # REDIS_URL="redis://127.0.0.1:6379"
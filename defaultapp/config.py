import os, urllib
from dotenv import load_dotenv



class Config:

	#load dotenv in the base root
	
	APP_ROOT = os.path.join(os.path.dirname(__file__))   # refers to application_top
	dotenv_path = os.path.join(APP_ROOT, '.env')
	load_dotenv(dotenv_path)
	
	APP_NAME = os.getenv("APP_NAME")
	FLASK_ENV = os.getenv("FLASK_ENV")

	SECRET_KEY = os.getenv("SECRET_KEY")
	SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT")
	
	DB_CONNECTION_TYPE = os.getenv("DB_CONNECTION_TYPE")
	DB_HOST = os.getenv("DB_HOST")
	DB_PORT = os.getenv("DB_PORT")
	DB_DATABASE = os.getenv("DB_DATABASE")
	DB_USERNAME = os.getenv("DB_USERNAME")
	DB_PASSWORD = os.getenv("DB_PASSWORD")

	QUOTED_DATABASE_PASSWORD = urllib.parse.quote_plus(DB_PASSWORD)
	SQLALCHEMY_DATABASE_URI = DB_CONNECTION_TYPE+"://"+DB_USERNAME+":"+QUOTED_DATABASE_PASSWORD+"@"+DB_HOST+":"+DB_PORT+"/"+DB_DATABASE
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	
	MAIL_SERVER = os.getenv("MAIL_SERVER")
	MAIL_PORT = os.getenv("MAIL_PORT")
	MAIL_USE_TLS = os.getenv("MAIL_USE_TLS")
	MAIL_USERNAME = os.getenv("MAIL_USERNAME")
	MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
 
	BOKEH_URL = os.getenv("BOKEH_URL")
	BOKEH_PORT = os.getenv("BOKEH_PORT")
	BOKEH_SECRET_KEY = os.getenv("BOKEH_SECRET_KEY")
	BOKEH_SIGN_SESSIONS = os.getenv("BOKEH_SIGN_SESSIONS")
	BOKEH_DATA_PATH = os.path.join(APP_ROOT, os.getenv("BOKEH_DATA_PATH"))
	BOKEH_DEBUG_LEVEL = os.getenv("BOKEH_DEBUG_LEVEL")

	REDMINE_HOST = os.getenv("REDMINE_HOST")
	REDMINE_DATABASE = os.getenv("REDMINE_DATABASE")
	REDMINE_USER = os.getenv("REDMINE_USER")
	REDMINE_PASSWORD = os.getenv("REDMINE_PASSWORD")

	SSL_CERT_FILE = os.getenv("SSL_CERT_FILE")
	SSL_KEY_FILE = os.getenv("SSL_KEY_FILE")
 
	NEO4J_USR = os.getenv("NEO4J_USR")
	NEO4J_PWD = os.getenv("NEO4J_PWD")
	NEO4J_URI = os.getenv("NEO4J_URI")
    
	AUTH_ONLY_MAILS = os.getenv("AUTH_ONLY_MAILS").replace(' ','').lower().split(",")
	if '' in AUTH_ONLY_MAILS: AUTH_ONLY_MAILS.remove('')
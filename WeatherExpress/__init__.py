import os
from flask import Flask
from flask_login import LoginManager
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_pymongo import PyMongo
import certifi

secret_key = os.environ.get('SECRET_KEY')
mongo_uri = os.environ.get('MONGO_URI')

application = Flask(__name__)
application.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
application.config['MONGO_URI'] = 'mongodb+srv://lhiur001:0pemDaAuQTiqvR9L@profiles-db.jovxyhy.mongodb.net/profiles-db?retryWrites=true&w=majority'

mongo = PyMongo(application, tlsCAFile=certifi.where())

try:
    # Fetch data from a MongoDB collection
    data = mongo.db.collection_name.find_one()
    print('PyMongo connection test: Success')
except Exception as e:
    print('PyMongo connection test: Failed. Error: {}'.format(e))

bcrypt = Bcrypt(application)
login_manager = LoginManager(application)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
application.config['MAIL_SERVER'] = 'smtp.googlemail.com'
application.config['MAIL_PORT'] = 587
application.config['MAIL_USE_TLS'] = True
application.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
application.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(application)

from WeatherExpress import routes




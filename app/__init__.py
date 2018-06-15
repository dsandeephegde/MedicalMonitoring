from flask import Flask
from flask_mysqldb import MySQL

# Initialize the app
app = Flask(__name__, instance_relative_config=True)
mysql = MySQL()
mysql.init_app(app)

# Load the config file
app.config.from_object('config')

# Load the Apis
from app import api

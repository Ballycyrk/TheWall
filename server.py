from flask import Flask, flash, session, request, redirect, render_template
from flask.ext.bcrypt import Bcrypt
from mysqlconnection import MySQLConnector
import re
app = Flask(__name__)
# mysql = MySQLConnector('pinkfloydb')
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
app.secret_key = 'HeyKrisLeaveThemKidsAlone'

@app.route('/')
def index():
  return render_template('index.html')

app.run(debug=True)

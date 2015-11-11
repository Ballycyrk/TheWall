from flask import Flask, flash, session, request, redirect, render_template
from flask.ext.bcrypt import Bcrypt
from mysqlconnection import MySQLConnector
import re
app = Flask(__name__)
mysql = MySQLConnector('pinkfloydb')
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
NAME_REGEX = re.compile(r'^[a-zA-Z]{2,}$')
app.secret_key = 'HeyKrisLeaveThemKidsAlone'

# MODEL FUNCTIONS
def get_user(email):
  select = "SELECT * FROM users WHERE email = '{}'".format(email)
  user = mysql.fetch(select)
  print '*************************MODEL FUNCTIONS*****************************'
  print user
  return user

@app.route('/')
def index():
  if 'user_id' in session:
    return "still need a minute!"
  else:
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def create():
  bool = True
  if not NAME_REGEX.match(request.form['first_name']):
    flash('Your first name can only contain letters & must be at least \
          2 characters.')
    bool = False
  if not NAME_REGEX.match(request.form['last_name']):
    flash('Your last name can only contain letters & must be at least \
          2 characters.')
    bool = False
  if not EMAIL_REGEX.match(request.form['email']):
    flash('Not a valid email.')
    bool = False
  if request.form['password'] != request.form['confirm']:
    flash("Confirmation does not match Password, please re-enter.")
    bool = False
  elif len(request.form['password']) < 8:
    flash("Password must be at least 8 characters long")
    bool = False
  if bool:
    check = get_user(request.form['email'])
    if len(check) > 0:
      flash('That email is already in the database.  Please login.')
      return render_template('index.html')
    else:
      pw_digest = bcrypt.generate_password_hash(request.form['password'])
      insert = "INSERT INTO users \
                (first_name, last_name, email, pw_digest, created_at, updated_at) \
                VALUES ('{}','{}','{}','{}', NOW(), NOW())".format(request.form['first_name'], request.form['last_name'], request.form['email'], pw_digest)
      mysql.run_mysql_query(insert)
      user = get_user(request.form['email'])
      session['user_id']    = user[0]['id']
      session['first_name'] = user[0]['first_name']
      flash('Welcome to The Wall.')
      return 'Give us a minute.'
  return redirect('/')

app.run(debug=True)


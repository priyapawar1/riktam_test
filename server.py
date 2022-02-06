
from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
import string
import random


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.sqlite3'

db = SQLAlchemy(app)



class user(db.Model):
	id = db.Column('user_id', db.Integer, primary_key = True)
	name = db.Column(db.String(100))
	auth_token = db.Column(db.String(100))

	def __init__(self, name,auth_token):
		self.name = name
		self.auth_token = auth_token


class group(db.Model):
	group_id = db.Column('grp_id', db.Integer, primary_key = True)
	group_name = db.Column(db.String(100))
	created_by = db.Column('created_by', db.Integer)

	def __init__(self, g_name,created_by):
		self.group_name = g_name
		self.created_by = created_by


@app.route('/create_group',methods = ['GET', 'POST'])
def create_group():
	

	group_name = request.form["group_name"]
	created_by = request.form["created_by"]

	group_row = group(group_name, created_by)
	db.session.add(group_row)
	db.session.commit()

	return "group created"




@app.route('/')
def hello_world():
	return "hello_world"



@app.route('/login',methods = ['GET', 'POST'])
def login():
	req_auth_token = request.form["auth_token"]
	user_name = request.form["user_name"]

	record = user.query.filter_by(name = user_name,auth_token = req_auth_token).first()

	if record:
		return "Logged in succesfully"
	else:
		return "Invalid credentials"


@app.route('/logout',methods = ['GET', 'POST'])
def logout():
	
	user_name = request.form["user_name"]

	record = user.query.filter_by(name = user_name).first()

	if record:
		return "Logged Out succesfully"
	else:
		return "Invalid Login id"




@app.route('/edit_user',methods = ['GET', 'POST'])
def edit_user():

	req_auth_token = request.form["auth_token"]
	
	user_name = request.form["user_name"]
	user_id = request.form["user_id"]

	admin_record = user.query.filter_by(name = "admin_user").first()
	db_auth_token = admin_record.auth_token

	if req_auth_token == db_auth_token:

		
		user.query.filter_by(id = user_id).update({user.name:user_name})
		db.session.commit()


		return "Row Updated"

	else:
		return "Not Admin User"




@app.route('/create_user',methods = ['GET', 'POST'])
def create_user():
	print(request.form,"==")

	req_auth_token = request.form["auth_token"]
	

	admin_record = user.query.filter_by(name = "admin_user").first()
	db_auth_token = admin_record.auth_token

	if req_auth_token == db_auth_token:
		user_name = request.form["user_name"]

		random_token = ''.join(random.choices(string.ascii_uppercase+string.digits, k = 10))

		user_row = user(user_name,auth_token=random_token)
		db.session.add(user_row)
		db.session.commit()

		return "Row Inserted"


	else:
		return "Not Admin User"






if __name__ == '__main__':
	db.create_all()


	exists = user.query.filter_by(name = "admin_user").first()

	if not exists:

		admin_user = user("admin_user",auth_token="Priya@123")
		db.session.add(admin_user)
		db.session.commit()

	app.run(port=8181,debug=True)

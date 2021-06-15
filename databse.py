from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.secret_key = 'random key'

class Database_Soumee():

	gbl_email=''
	engine= create_engine(r'db2+ibm_db://lqd29580:w7db0p6rrq%5Ecg8g6@dashdb-txn-sbox-yp-dal09-10.services.dal.bluemix.net:50000/BLUDB')
	db = scoped_session(sessionmaker(bind=engine))

	def __init__(self):
		pass


	def write_user_table(self, user_info):
		print('inside databse')
		firstname = user_info['firstname']
		lastname = user_info['lastname']
		email = user_info['email']
		password = user_info['password']
		location_state = user_info['location']
		
		full_name=""
		full_name= full_name + firstname + lastname

	    # Pushing user data to database in the user table
	    # Checking if no other user exists with the same passwords and stuff
	    # And yet again displaying the entry.html file so that user can enter his credentials to login to his account
		#self.db.execute("SELECT password FROM user WHERE password= :password ",{"password":password}).fetchall())== 0 and
		if len(self.db.execute("SELECT passwords FROM users WHERE passwords= :password ",{"password":password}).fetchall())== 0 and len(self.db.execute("SELECT email FROM users WHERE email =:email ", {"email":email}).fetchall())== 0:
			print("there is no password")
			print("there is no email")
			self.db.execute("INSERT INTO users(uid, full_name, email, passwords, location_state) VALUES(seq_user.nextval,:full_name, :email, :password, :location_state)",
			               { "full_name":full_name, "email":email, "password":password, "location_state": location_state})
			print('commiting')
			self.db.commit()
			return "Registered"
		else:
			return "User Already registered"


	def check_user_table(self, user_info):
		
		email= user_info["email"]
		password= user_info["password"]

		if len(self.db.execute("SELECT email, passwords FROM users WHERE email= :email AND passwords= :password ",
						{"email":email, "password":password}).fetchall())== 0:
			print("User doesnt exist")
			return False

		print("User exist")
		return True



	def check_user_input_table(self, user_info):
		
		email= user_info["email"]
		password= user_info["password"]

		if self.check_user_table(user_info):
			sql_obj=self.db.execute("SELECT users.uid FROM users WHERE email=:email", {"email":email}).fetchone()
			#print(type(sql_obj))
			if len(self.db.execute("SELECT * FROM user_input WHERE uid = :id ", {"id":(sql_obj.items())[0][1]} ).fetchall())!=0:
				print("uid exist")
				return True
		
		print("uid doesnt exist")
		return False

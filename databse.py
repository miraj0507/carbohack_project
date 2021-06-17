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

	def write_user_input_table(self, user_info, user_data):
		
		email = user_info['email']
		uid = self.db.execute("SELECT users.uid FROM users WHERE email=:email", {"email":email}).fetchone().items()[0][1]
		self.db.execute("INSERT INTO user_input(ui_id, uid, travel, diet, electricity, no_of_flights, dates) VALUES(user_input_seq.nextval,:uid, :travel, :diet, :electricity, :no_of_flights, :dates)",
			               { "uid":uid, "travel":user_data['travel'], 'diet':user_data['diet'], 'electricity':user_data['elec'], 'no_of_flights':user_data['no_of_flights'], 'dates':user_data['dates']})
		print('commiting')
		self.db.commit()
		return "Registered"

	def write_travel_table(self, user_info, user_data):

		email = user_info['email']
		uid = self.db.execute("SELECT users.uid FROM users WHERE email=:email", {"email":email}).fetchone().items()[0][1]
		self.db.execute("INSERT INTO travel(travel_id, uid, bus, taxi, train, car, motorbike, cycling, walking, dates) VALUES(next value for travel_seq,:uid, :bus,:taxi, :train, :car, :motorbike, 0, 0, :dates)",
			            { "uid":uid, 'bus':user_data['bus'], 'taxi':user_data['taxi'], 'train':user_data['taxi'], 'car':user_data['car'], 'motorbike':user_data['bike'], 'dates':user_data['dates']})
		print('commiting')
		self.db.commit()
		print("Registered")


	def write_output_table(self, user_info, user_data):

		email = user_info['email']
		uid = self.db.execute("SELECT users.uid FROM users WHERE email=:email", {"email":email}).fetchone().items()[0][1]
		self.db.execute("INSERT INTO user_output(uoid, uid, carbon_footprint, monthly_average, dates) VALUES(next value for user_output_seq,:uid, :carbon_footprint, :monthly_average, :dates)",
			            { "uid":uid, 'carbon_footprint':user_data['carbon_footprint'],'monthly_average':user_data['monthly_average'] , 'dates': user_data['dates'] })
		print('commiting')
		self.db.commit()
		print("Registered")

	def update_state(self, user_info, state):
		email = user_info['email']
		uid = self.db.execute("SELECT users.uid FROM users WHERE email=:email", {'email':email}).fetchone().items()[0][1]
		self.db.execute(f"UPDATE users SET location_state='{state}' WHERE uid={uid}")
		self.db.commit()
		print('registered')

	def check_dates(self, user_info, today_date):
		email = user_info['email']
		uid = self.db.execute("SELECT users.uid FROM users WHERE email=:email", {"email":email}).fetchone().items()[0][1]
		
		if len(self.db.execute(f"SELECT * FROM USER_INPUT WHERE DATES='{today_date}' and uid={uid}").fetchall())==0:
			return False
		return True

	def fetch_data(self,user_info, table_name, item, today_date):
		email = user_info['email']
		uid = self.db.execute("SELECT users.uid FROM users WHERE email=:email", {"email":email}).fetchone().items()[0][1]
		data=self.db.execute(f"SELECT {item} FROM {table_name} WHERE dates='{today_date}' and uid={uid}").fetchone().items()[0][1]
		return data

	def update_travel_table(self, user_info, user_data, date):
		email = user_info['email']
		uid = self.db.execute("SELECT users.uid FROM users WHERE email=:email", {"email":email}).fetchone().items()[0][1]
		self.db.execute(f"UPDATE TRAVEL SET BUS={user_data['bus']}, TAXI={user_data['taxi']}, TRAIN={user_data['train']}, CAR={user_data['car']}, MOTORBIKE={user_data['bike']} WHERE uid={uid} and dates='{date}'")
		print('commiting')
		self.db.commit()
		print("Registered")

	def update_user_input_table(self, user_info, user_data, date):
		email = user_info['email']
		uid = self.db.execute("SELECT users.uid FROM users WHERE email=:email", {"email":email}).fetchone().items()[0][1]
		self.db.execute(f"UPDATE USER_INPUT SET  travel={user_data['travel']}, diet='{user_data['diet']}', electricity=0, no_of_flights={user_data['no_of_flights']} where uid={uid} and dates='{date}'")
		print('commiting')
		self.db.commit()
		return "Registered"

	def update_data(self, user_info, tablename, condition, value, date):
		email = user_info['email']
		uid = self.db.execute("SELECT users.uid FROM users WHERE email=:email", {"email":email}).fetchone().items()[0][1]
		self.db.execute(f"UPDATE {tablename} SET {condition}={value} where uid={uid} and dates='{date}'")
		print('commiting')
		self.db.commit()
		return "Registered"

	def latest_date(self, user_info, tablename):
		email = user_info['email']
		uid = self.db.execute("SELECT users.uid FROM users WHERE email=:email", {"email":email}).fetchone().items()[0][1]
		return self.db.execute(f"select max(dates) from {tablename} where uid={uid}").fetchone().items()[0][1]

	def oauth_login_signup(self, user_info):
		if len(self.db.execute(f"select * from users where email='{ user_info['email'] }'").fetchall())==0:
			self.db.execute("INSERT INTO users(uid, full_name, email, authenticate_id) VALUES(seq_user.nextval,:full_name, :email, :auth_id)",
			               { "full_name":user_info['full_name'], "email":user_info['email'], "auth_id":user_info['auth_id']})
			print('commiting')
			self.db.commit()
			return "MADE AN ACCOUNT"
		
		return "EXIST"
	
	
	'''
	def fetch_travel(self, user_info, need):

		email = user_info['email']
		uid=self,db.execute("SELECT users.uid FROM users WHERE email=:email",{'email':email}).fetchone().items()[0][1]
		data=self.db.execute(f"SELECT {need} from travel t inner join (select uid, max(dates) as MaxDate from travel group by uid) tm on t.uid = tm.uid and ").fetchall()
		print(data)
	'''
			

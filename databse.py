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
		if (password == '' or email == ''):
			return "Empty field"
		
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

	def oauth_login_signup(self, user_info):
		if len(self.db.execute(f"select * from users where email='{ user_info['email'] }'").fetchall())==0:
			self.db.execute("INSERT INTO users(uid, full_name, email, authenticate_id) VALUES(seq_user.nextval,:full_name, :email, :auth_id)",
			               { "full_name":user_info['name'], "email":user_info['email'], "auth_id":user_info['id']})
			print('commiting')
			self.db.commit()
		
		return True


	def check_user_table(self, user_info):
		
		email= user_info["email"]
		
		if user_info['password']:
			password= user_info["password"]
			if (email == '' or password == ''):
				return "Empty field"

			if len(self.db.execute("SELECT email, passwords FROM users WHERE email= :email AND passwords= :password ",
							{"email":email, "password":password}).fetchall())== 0:
				print("User doesnt exist")
				return False

			print("User exist")
			return True
		
		else:
			return self.oauth_login_signup(user_info)



	def check_user_input_table(self, user_info):
		
		email= user_info["email"]
		
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
		self.db.execute("INSERT INTO travel(travel_id, uid, bus, taxi, train, car, motorbike, cycling, walking, dates, fly) VALUES(next value for travel_seq,:uid, :bus,:taxi, :train, :car, :motorbike, 0, 0, :dates, :fly)",
			            { "uid":uid, 'bus':user_data['bus'], 'taxi':user_data['taxi'], 'train':user_data['taxi'], 'car':user_data['car'], 'motorbike':user_data['bike'], 'dates':user_data['dates'], 'fly':user_data['fly']})
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
		self.db.execute(f"UPDATE TRAVEL SET BUS={user_data['bus']}, TAXI={user_data['taxi']}, TRAIN={user_data['train']}, CAR={user_data['car']}, MOTORBIKE={user_data['bike']}, FLY={user_data['fly']} WHERE uid={uid} and dates='{date}'")
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

	
	def get_table_data(self, user_info, item, tablename, d):
		email = user_info['email']
		uid = self.db.execute("SELECT users.uid FROM users WHERE email=:email", {"email":email}).fetchone().items()[0][1]
		year_st = d.year
		month_st= d.month
		month_end = month_st+1
		year_end = year_st
		if month_st>12:
			month_end=1
			year_end+=1
		
		date_st=f"{year_st}-{month_st}-01"
		date_end=f"{year_end}-{month_end}-01"

		qqq = f"SELECT sum({item}) from {tablename} where uid={uid} and dates between '{date_st}' and '{date_end}'"
		print(qqq)

		values = self.db.execute(f"SELECT sum({item}) from {tablename} where uid={uid} and dates between '{date_st}' and '{date_end}'").fetchone().items()[0][1]
		if values==None:
			values=0

		print(values)
		return values

	def get_food_total(self, user_info, d):
		email = user_info['email']
		uid = self.db.execute("SELECT users.uid FROM users WHERE email=:email", {"email":email}).fetchone().items()[0][1]
		year_st = d.year
		month_st= d.month
		month_end = month_st+1
		year_end = year_st
		if month_st>12:
			month_end=1
			year_end+=1
		
		date_st=f"{year_st}-{month_st}-01"
		date_end=f"{year_end}-{month_end}-01"

		qqq = f"SELECT diet from user_input where uid={uid} and dates between '{date_st}' and '{date_end}'"
		values = self.db.execute(f"SELECT diet from user_input where uid={uid} and dates between '{date_st}' and '{date_end}'").fetchall()
		value_array = [i[0] for i in values]
		#print(value_array)
		#input()
		return value_array



	def fetch_user(self, user_info, tablename):
		email = user_info['email']
		uid = self.db.execute("SELECT users.uid FROM users WHERE email=:email", {"email":email}).fetchone().items()[0][1]
		value = self.db.execute(f"select {tablename} from users where uid={uid}")
		return value

	def get_monthly_avg(self, user_info, month, year):
		nxt_mnth = month+1
		nxt_year = year
		if nxt_mnth>12:
			nxt_mnth=1
			nxt_year=year+1
		st_date = f"{year}-{month}-1"
		end_date = f"{nxt_year}-{nxt_mnth}-1"

		d = self.db.execute(f"SELECT distinct monthly_average from user_output where dates between '{st_date}' and '{end_date}'").fetchone()
		if d == None:
			dd=str(0)
		else:
			dd=str(d.items()[0][1])
		
		return dd


	'''
	def fetch_travel(self, user_info, need):

		email = user_info['email']
		uid=self,db.execute("SELECT users.uid FROM users WHERE email=:email",{'email':email}).fetchone().items()[0][1]
		data=self.db.execute(f"SELECT {need} from travel t inner join (select uid, max(dates) as MaxDate from travel group by uid) tm on t.uid = tm.uid and ").fetchall()
		print(data)
	'''
			

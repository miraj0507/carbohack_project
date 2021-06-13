
import requests
import json

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from authlib.integrations.flask_client import OAuth


import os, sys
sys.path.append(".")
from oauth_user import Google, Facebook, Linkedin, Twitter


app = Flask(__name__)
app.secret_key = 'random key'

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
# engine = create_engine("ibm_db_sa+pyodbc400://lqd29580:w7db0p6rrq^5Ecg8g6@dashdb-txn-sbox-yp-dal09-10.services.dal.bluemix.net:50001/BLUDB;currentSchema=LQD29580")
engine= create_engine(r'db2+ibm_db://lqd29580:w7db0p6rrq%5Ecg8g6@dashdb-txn-sbox-yp-dal09-10.services.dal.bluemix.net:50000/BLUDB')
db = scoped_session(sessionmaker(bind=engine))

session={}
session["message_code"]=1

# Index page
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/entry')
def entry():
    if session["message_code"]==0:
        message_out= "Invalid username or password"
    else:
        message_out=""
    session["message_code"]=1
    return render_template('entry.html', message=message_out)

#*************************************************************************
#GOOGLE OAUTH /START

gg=Google()

@app.route('/signup_google')
def signup_google():
    google=gg.to_auth_page()
    redirect_url = url_for('auth_google', _external=True,_scheme='https')
    print(redirect_url)
    return google.authorize_redirect(redirect_url)


@app.route('/auth_google')
def auth_google():
    user_info = gg.send_user_info()
    print(user_info)
    #Use the user_info
    return redirect('/entry')

# /END
# *************************************************************************
#FACEBOOK OAUTH /START

ff=Facebook()

@app.route('/signup_facebook')
def signup_facebook():
    facebook=ff.to_auth_page()
    redirect_url = url_for('auth_facebook', _external=True,_scheme='https')
    print(redirect_url)
    return facebook.authorize_redirect(redirect_url)

@app.route('/auth_facebook/')
def auth_facebook():
    user_info = ff.send_user_info()
    print(user_info)
    #Use the user_info
    return redirect('/entry')

# /END
#***************************************************************************
# LINKEDIN OAUTH /START

ll=Linkedin()

@app.route('/signup_linkedin')
def signup_linkedin():
    linkedin=ll.to_auth_page()
    redirect_url = url_for('auth_linkedin', _external=True,_scheme='https')
    return linkedin.authorize_redirect(redirect_url)

@app.route('/auth_linkedin')
def auth_linkedin():
    user_info = ll.send_user_info()
    print(user_info)
    #use the user_info
    return redirect('/entry')

# /END
#***************************************************************************
# TWITTER OAUTH /START

tt=Twitter()

@app.route('/signup_twitter')
def signup_twitter():
    twitter=tt.to_auth_page()
    redirect_url= url_for('auth_twitter', _external=True, _scheme='https')
    return twitter.authorize_redirect(redirect_url)

@app.route('/auth_twitter')
def auth_twitter():
    user_info = tt.send_user_info()
    print(user_info)
    #use the user_info
    return redirect('/entry')


# /END
#***************************************************************************

# For processing user data
@app.route('/processing...', methods=['POST'])
def processing_user_info():

    # Parsing user data coming from frontend
    firstname = request.values.get('firstname')
    lastname = request.values.get('lastname')
    email = request.values.get('email-signup')
    password = request.values.get('password-signup')
    location_state = request.values.get('location')

    full_name=""
    full_name= full_name + firstname + lastname

    # Pushing user data to database in the user table
    # Checking if no other user exists with the same passwords and stuff
    # And yet again displaying the entry.html file so that user can enter his credentials to login to his account

    if len(db.execute("SELECT password FROM user WHERE password= :password ",{"password":password}).fetchall())== 0 and len(db.execute("SELECT email FROM user WHERE email =:email ", {"email":email}).fetchall())== 0:
                 print("there is no password")
                 print("there is no email")
                 db.execute("INSERT INTO user(User_id, full_name, email, password, location_state) VALUES(seq_user.nextval,:full_name, :email, :password, :location_state)",
                               { "full_name":full_name, "email":email, "password":password, "location_state": location_state})

                 db.commit()
                 return redirect(url_for('entry'))
    else:
        return render_template("entry.html", message= "The email/ password /username is already registered under an user")



# Logging in to get into the Questionaire page
@app.route('/questionare', methods=["POST"])
def login():
# Querying for relevant user details while logging an user in.
# if match is found:
# return render_template("questionaire.html")
# if request.method=="POST":
      print(session)
      email= request.values.get("email-signin")
      password= request.values.get("password-signin")

      if len(db.execute("SELECT email, password FROM user WHERE email= :email AND password= :password ",
                    {"email":email, "password":password}).fetchall())== 0:
           session["message_code"]=0
           print("failed")
           return redirect(url_for("entry"))

      else:
          print("success")
          session["email"]= email
          session["logged_in"]=True
          sql_obj=db.execute("SELECT user.user_id FROM user WHERE email=:email", {"email":email}).fetchone()
          if db.execute("SELECT * FROM user_input WHERE user_id = :id ", {"id":(sql_obj.items())[0][1]} ):
               return render_template("questionare.html")
          else:
              return redirect(url_for('My_Account'))

      return render_template("entry.html")


# User's account page. Left to be done
@app.route('/MyAccount')
def My_Account():
#    Details of the parameters taken in from the questionaire. Stored in the database. Graph is plotted. Things to be calculated according to formulae present here.
#    https://docs.google.com/document/d/1qZepM5Bbe13qaWUCraEf1Hmmb-otN7MImFnaBgSw44w/edit?ts=60bf9810
     return "hello world"


@app.route("/goback")
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route("/ret_home")
def rethome():
    return redirect(url_for('home'))
if __name__ == '__main__':
    app.run(debug=True)

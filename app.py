
import requests
import json

from flask import Flask, session, render_template, request, redirect, url_for
#from flask_session import Session
#from sqlalchemy import create_engine
#from sqlalchemy.orm import scoped_session, sessionmaker
from authlib.integrations.flask_client import OAuth


import os, sys
sys.path.append(".")
from oauth_user import Google, Facebook, Linkedin, Twitter


app = Flask(__name__)
app.secret_key = 'random key'

# Configure session to use filesystem
#app.config["SESSION_PERMANENT"] = False
#app.config["SESSION_TYPE"] = "filesystem"
#Session(app)

# Set up database
#engine = create_engine("URL for database")
#db = scoped_session(sessionmaker(bind=engine))



# Index page
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/entry_signin')
@app.route('/entry_signup')
def entry():
    return render_template('entry.html')

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

# MANUAL INPUT USER DATA /START
@app.route('/processing_signup', methods=['POST'])
def processing_signup():
    user_info = {}
    user_info['firstname'] = request.form['firstname']
    user_info['lastname'] = request.form['lastname']
    user_info['email'] = request.form['email']
    user_info['password'] = request.form['password']
    user_info['location'] = request.form['location']
    print(user_info)
    return "Correct"

@app.route('/processing_signin', methods=['POST'])
def processing_signin():
    user_info = {}
    user_info['email'] = request.form['email']
    user_info['password'] = request.form['password']
    print(user_info)
    return "Correct"

# /END
#**************************************************************************


# Logging in to get into the Questionaire page
@app.route('/questionare')
def login():
    # Querying for relevant user details while logging an user in.
    # if match is found:
    # return render_template("questionaire.html")
    # else:
    return render_template("entry.html")


# User's account page. Left to be done
@app.route('/MyAccount')
def My_Account():
#    Details of the parameters taken in from the questionaire. Stored in the database. Graph is plotted. Things to be calculated according to formulae present here.
#    https://docs.google.com/document/d/1qZepM5Bbe13qaWUCraEf1Hmmb-otN7MImFnaBgSw44w/edit?ts=60bf9810
    return render_template('dashboard.html') 

if __name__ == '__main__':
    app.run(debug=True)

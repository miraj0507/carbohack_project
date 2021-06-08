import requests
import json

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine("URL for database")
db = scoped_session(sessionmaker(bind=engine))


app = Flask(__name__)

# Index page
@app.route('/')
def index():
    return render_template('index.html')

# For registering the user/login
@app.route('/signup')
def signup():
    return render_template('entry.html')


# For processing user data
@app.route('/processing...')
def processing_user_info():
    # Parsing user data coming from frontend
    
    # Pushing user data to database and yet again displaying the entry.html file so that user can enter his credentials to login to his account
    return render_template('entry.html')


# Logging in to get into the Questionaire page
@app.route('/questionare')
def login():
    # Querying for relevant user details while logging an user in.
    # if match is found:
    # return render_template("questionaire.html")
    # else:
    return render_template("entry.html")

# User's account page. Left to be done
#@app.route('/MyAccount')
#def My_Account():
#    return render_template('MyAccount.html') 

if __name__ == '__main__':
    app.run(debug=True)

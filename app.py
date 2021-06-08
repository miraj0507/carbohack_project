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

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup')
def signup():
    return render_template('entry.html')



@app.route('/questionare')
def questionare():
    return render_template('questionare.html')



@app.route('/login')
def login():
    return render_template('login.html')



if __name__ == '__main__':
    app.run(debug=True)

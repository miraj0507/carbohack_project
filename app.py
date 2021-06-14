
import requests
import json

from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from authlib.integrations.flask_client import OAuth


import os, sys
sys.path.append(".")
from oauth_user import Google, Facebook, Linkedin, Twitter
from databse import Database_Soumee


app = Flask(__name__)
app.secret_key = 'random key'

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#session={}
#session["message_code"]=1

# Set up database
#engine = create_engine("URL for database")
#db = scoped_session(sessionmaker(bind=engine))

db_S = Database_Soumee()


#*********************************************** OUTSIDER VIEW /START ***************************************************************

# Index page
@app.route('/')
def index():
    if 'user' in session:
        return redirect('/MyAccount')
    return render_template('index.html')


@app.route('/entry_signin')
@app.route('/entry_signup')
def entry():
    if 'user' in session:
        return redirect('/MyAccount')
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
    if 'user' in session:
        return redirect('/MyAccount')
    user_info = request.json
    print(user_info) 
    db_S_respond=db_S.write_user_table(user_info)
    print(user_info)
    return jsonify(resp1="Correct", resp2=db_S_respond)

@app.route('/processing_signin', methods=['POST'])
def processing_signin():
    if 'user' in session:
        return redirect('/MyAccount')
    user_info = request.json
    #user_info['email'] = request.form['email']
    #user_info['password'] = request.form['password']
    if db_S.check_user_table(user_info):
        session['user']=user_info
        if db_S.check_user_input_table(user_info):
            return jsonify(resp1="Correct", resp2='/MyAccount')
        else:
            return jsonify(resp1="Correct", resp2="/questionare")
    print(user_info)
    return jsonify(resp1="Incorrect", resp2='You are not in database, Please Sign Up First')

# /END
#**************************************************************************

#************************************************** OUTSIDER VIEW /END **************************************************************

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


#************************************************** INSIDER VIEW /START**************************************************************


#QUESTIONARE FILLING /START
@app.route('/questionare')
def questionare():
    if not ('user' in session):
        return redirect('/')

    if db_S.check_user_input_table(session['user']):
        return redirect('/MyAccount')
    
    return render_template("questionare.html")

@app.route("/questionare_filling", methods=['POST'])
def questionare_filling():
    if not('user' in session):
        return redirect('/')

    user_info = request.json
    db_S_respond='Registered'#db_S.example(user_info)
    return jsonify(resp1='Correct', resp2=db_S_respond)

@app.route("/questionare_update", methods=['POST'])
def questionare_update():
    if not('user' in session):
        return redirect('/')

    user_info = request.json
    print(user_info)
    db_S_respond='Registered'#db_S.example(user_info)
    return jsonify(resp1='Correct', resp2=db_S_respond)
#QUESTIONARE FILLING /END


#@app.route("/")
# User's account page. Left to be done
@app.route('/MyAccount')
def My_Account():
    if not ('user' in session):
        return redirect('/')
    
    #if not db_S.check_user_input_table(session['user']):
    #    return redirect('/questionare')
#    Details of the parameters taken in from the questionaire. Stored in the database. Graph is plotted. Things to be calculated according to formulae present here.
#    https://docs.google.com/document/d/1qZepM5Bbe13qaWUCraEf1Hmmb-otN7MImFnaBgSw44w/edit?ts=60bf9810
    return render_template('dashboard.html')

@app.route("/logout")
def logout():
    if not ('user' in session):
        return redirect('/')
    session.pop('user', None)
    db_S.gbl_email=''
    return redirect('/')

@app.route('/User_Profile')
def User_Profile():
    if not ('user' in session):
        return redirect('/')
    
    #if not db_S.check_user_input_table(session['user']):
    #    return redirect('/questionare')
#    Details of the parameters taken in from the questionaire. Stored in the database. Graph is plotted. Things to be calculated according to formulae present here.
#    https://docs.google.com/document/d/1qZepM5Bbe13qaWUCraEf1Hmmb-otN7MImFnaBgSw44w/edit?ts=60bf9810
    return render_template('user.html', fullname='Aunomitra Ghosh', state='West Bengal', email='aunomitra.ghosh1999@gmail.com')


if __name__ == '__main__':
    app.run(debug=True)

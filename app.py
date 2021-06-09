from flask import Flask, url_for, session, request, redirect
from flask import render_template
from authlib.integrations.flask_client import OAuth

import os, sys
sys.path.append(".")
from oauth_user import Google, Facebook

app = Flask(__name__)
app.secret_key = 'random key'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/entry')
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


@app.route('/questionare')
def qustionare():
    return render_template('questionare.html')



@app.route('/login')
def login():
    return render_template('login.html')



if __name__ == '__main__':
    app.run(debug=True)

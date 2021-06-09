from flask import Flask, url_for, session, request, redirect
from authlib.integrations.flask_client import OAuth

class Google():
	
	app = Flask(__name__)
	app.secret_key='random key'

	oauth = OAuth(app)
	google = oauth.register(
	    name='google',
	    client_id='605004903750-9idp7cggojabevccn697qbbg2cthb1bc.apps.googleusercontent.com',
	    client_secret='fF9LnK2QFou9Wb6TM10fl_rf',
	    access_token_url='https://accounts.google.com/o/oauth2/token',
	    access_token_params=None,
	    authorize_url='https://accounts.google.com/o/oauth2/auth',
	    authorize_params=None,
	    api_base_url='https://www.googleapis.com/oauth2/v1/',
	    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
	    client_kwargs={'scope': 'openid email profile'},
    )

	g = oauth.create_client('google')


	def to_auth_page(self):
		return self.g

	def send_user_info(self):
		token=(self.oauth).google.authorize_access_token()
		resp = (self.oauth).google.get('userinfo')
		return resp.json()


import requests
import urllib.parse
import random

class Facebook:
	CLIENT_ID='2896973843953926'
	CLIENT_SECRET='ca2531220b6a1259e046d0c406633a42'
	
	redirect_url=''
	auth_endpoint = ''


	def __init__(self):
		pass

	def create_auth_endpoint(self):
			self.redirect_url=urllib.parse.quote(url_for('auth_facebook',_scheme='https',_external=True))
			print(self.redirect_url)

			state = ''.join([str(random.randint(1,7)) for i in range(0,6)])

			self.auth_endpoint = f"https://www.facebook.com/v6.0/dialog/oauth?client_id={self.CLIENT_ID}&redirect_uri={self.redirect_url}&state={state}"





	def get_User_Info(self, code):

		access_token_url=f"https://graph.facebook.com/v6.0/oauth/access_token?redirect_uri={self.redirect_url}&client_id={self.CLIENT_ID}&client_secret={self.CLIENT_SECRET}&code={code}"
		response = requests.get(access_token_url)

		acctok=response.json()['access_token']
		headerDict={'Accept':'application/json','Authorization':f"Bearer {acctok}"}
		userInfo=(requests.get('https://graph.facebook.com/me',headers=headerDict)).json()

		print(acctok)

		user_email_link=f"https://graph.facebook.com/v11.0/{userInfo['id']}/"
		param={'access_token':acctok}
		print(requests.get(user_email_link, param).json())


		return userInfo

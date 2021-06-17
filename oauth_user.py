from flask import Flask, url_for, session, request, redirect
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key='random key'


class Google():

	oauth = OAuth(app)
	google = oauth.register(
	    name='google',
	    client_id='605004903750-php7rvke8a2puumjs1pv3u12br843nqc.apps.googleusercontent.com',
	    client_secret='-BErL6826bBu2-vY9ekIwCuU',
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


class Facebook():
	
	oauth = OAuth(app)
	facebook = oauth.register(
	    name='facebook',
	    client_id='2896973843953926',
	    client_secret='ca2531220b6a1259e046d0c406633a42',
	    access_token_url='https://graph.facebook.com/v6.0/oauth/access_token',
	    access_token_params=None,
	    authorize_url='https://www.facebook.com/v6.0/dialog/oauth',
	    authorize_params=None,
	    api_base_url='https://graph.facebook.com/',
	    userinfo_endpoint='https://graph.facebook.com/me',  # This is only needed if using openId to fetch user info
	    client_kwargs={'scope': 'email'},
	    )
	f = oauth.create_client('facebook')
	
	def to_auth_page(self):
		return self.f

	def send_user_info(self):
		token = (self.oauth).facebook.authorize_access_token()
		print(token)
		resp = (self.oauth).facebook.get('/me',params={'fields':'name,email'})
		user_info = resp.json()
		return user_info
	
	
class Linkedin():
	
	oauth = OAuth(app)
	linkedin = oauth.register(
	    name='linkedin',
	    client_id='78u7oehwxtcfhl',
	    client_secret='Wib8hXLBq2if1Aki',
	    access_token_url='https://www.linkedin.com/oauth/v2/accessToken',
	    access_token_params=None,
	    access_token_method='POST',
	    authorize_url='https://www.linkedin.com/oauth/v2/authorization',
	    api_base_url='https://api.linkedin.com/v2',
	    client_kwargs={'scope': 'r_liteprofile r_emailaddress'},
	)
	
	l = oauth.create_client('linkedin')
	
	def to_auth_page(self):
		return self.l
	
	def send_user_info(self):
		token = (self.oauth).linkedin.authorize_access_token()
		resp1 = (self.oauth).linkedin.get('https://api.linkedin.com/v2/me').json()
		resp2 = (self.oauth).linkedin.get('https://api.linkedin.com/v2/emailAddress', params={'q':'members','projection':'(elements*(handle~))'}).json()
		user_info = {}
		user_info['firstname']=resp1['localizedFirstName']
		user_info['lastname']=resp1['localizedLastName']
		user_info['id']=resp1['id']
		user_info['email']=resp2['elements'][0]['handle~']['emailAddress']
		return user_info
	

class Twitter():
	
	oauth = OAuth(app)
	oauth.register(
	    name='twitter',
	    client_id='KEmpKPQEWrVPWNXEOYhEuI4EO',
	    client_secret='EgEzFqSYUrHIuw7Jil4kluUHFnL07zu9v6LBfTCRO9oXUgHoGj',
	    api_base_url='https://api.twitter.com/1.1/',
	    request_token_url='https://api.twitter.com/oauth/request_token',
	    access_token_url='https://api.twitter.com/oauth/access_token',
	    authorize_url='https://api.twitter.com/oauth/authenticate',
	    #fetch_token=lambda: session.get('token'),  # DON'T DO IT IN PRODUCTION
	)
	
	t = oauth.create_client('twitter')
	
	def to_auth_page(self):
		return self.t
	
	def send_user_info(self):
		token = (self.oauth).twitter.authorize_access_token()
		url = 'account/verify_credentials.json'
		resp = (self.oauth).twitter.get(url, params={'include_email':'true'}).json()
		user_info = {}
		name = resp['name'].split()
		user_info['firstname']=name[0]
		user_info['lastname']=' '.join([i for i in name[1:]])
		user_info['id']=resp['id']
		user_info['email']=resp['email']
		return user_info
	

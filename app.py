
import requests
import json

from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from authlib.integrations.flask_client import OAuth
import datetime
from datetime import date

import os, sys
sys.path.append(".")
from oauth_user import Google, Facebook, Linkedin, Twitter
from databse import Database_Soumee
from calculations import Calculations

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
calc_S = Calculations()


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
    try:
        user_info = gg.send_user_info()
        print(user_info)
        user_info['password']=None
        #input()
        session['user']=user_info
        #Use the user_info
        return redirect('/MyAccount')
    except:
        return render_template('error.html', err="403 Unauthorized")

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
    user_info['password']=None
    print(user_info)
    session['user']=user_info
    #Use the user_info
    return redirect('/MyAccount')

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
    session['user']=user_info
    #use the user_info
    return redirect('/MyAccount')
    
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
    session['user']=user_info
    #use the user_info
    return redirect('/MyAccount')


# /END
#***************************************************************************

# MANUAL INPUT USER DATA /START
@app.route('/processing_signup', methods=['POST'])
def processing_signup():
    if 'user' in session:
        return redirect('/MyAccount')
    #user_info = request.json
    user_info = {}
    user_info['firstname'] = request.form['firstname']
    user_info['lastname'] = request.form['lastname']
    user_info['email'] = request.form['email']
    user_info['password'] = request.form['password']
    user_info['location'] = request.form['location']
    print(user_info) 
    db_S_respond=db_S.write_user_table(user_info)
    print(user_info)
    return jsonify({'resp':"Correct", 'resp2':db_S_respond})

@app.route('/processing_signin', methods=['POST'])
def processing_signin():
    if 'user' in session:
        return redirect('/MyAccount')
    #user_info = request.json
    user_info = {}
    user_info['email'] = request.form['email']
    user_info['password'] = request.form['password']
    #user_info['id']=None
    if db_S.check_user_table(user_info):
        session['user']=user_info
        if db_S.check_user_input_table(user_info):
            return jsonify({"resp" : "Correct", "resp2":'/MyAccount'})
        else:
            return jsonify({'resp': "Correct", 'resp2':"/questionare"})
    print(user_info)
    return jsonify({'resp':"Incorrect", 'resp2':'Invalid Credentials'})
'''
    user_info = request.json
    #user_info['email'] = request.form['email']
    #user_info['password'] = request.form['password']
    print(user_info)
    return jsonify(resp1="Correct", resp2='Invalid Credentials')
'''

# /END
#**************************************************************************

#************************************************** OUTSIDER VIEW /END **************************************************************


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


#************************************************** INSIDER VIEW /START**************************************************************


#QUESTIONARE FILLING /START *********************
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

    dates=str(datetime.datetime.date(datetime.datetime.now()))
    user_info = request.json
    print(user_info)
    travel_data={}
    travel_data['bus']=int(user_info['bus'])
    travel_data['taxi']=int(user_info['taxi'])
    travel_data['train']=int(user_info['train'])
    travel_data['car']=int(user_info['car'])
    travel_data['bike']=int(user_info['bike'])
    travel_data['fly']=0
    travel_data['bicycle']=0
    travel_data['walking']=0
    travel_data['dates']=dates
    
    db_S.write_travel_table(session['user'], travel_data)
    
    time={}
    time['hour']=int(user_info['hour'])
    time['minutes']=int(user_info['minute'])
    calc_S.travel_f(travel_data, time)
    
    food_type=user_info['food']
    calc_S.food_f(food_type)

    #elec['bill']=user_info['elec_bill']
    #elec['members']=user_info['no_of_member']
    calc_S.elec_f(int(user_info['elec_bill']), int(user_info['no_of_member']))
    
    user_input={}
    user_input['travel']=calc_S.travel
    #elec={}
    user_input['diet']=user_info['food']
    user_input['elec']=calc_S.elec
    user_input['no_of_flights']=int(user_info['flights'])
    user_input['dates']=dates
    db_S.write_user_input_table(session['user'], user_input)

    db_S.update_state(session['user'], user_info['state'])
    
    db_S_respond='Registered'#db_S.example(user_info)
    
    calc_S.initial_set_up()
    user_output={}
    user_output['carbon_footprint']=calc_S.x
    user_output['monthly_average']=calc_S.avg
    user_output['dates']=dates
    db_S.write_output_table(session['user'], user_output)
    #put output values in output_table
    return jsonify(resp1='Correct', resp2=db_S_respond)

@app.route("/questionare_update", methods=['POST'])
def questionare_update():
    if not('user' in session):
        return redirect('/')

    user_info = request.json
    print(user_info)
    today_date = str(datetime.datetime.date(datetime.datetime.now()))
    travel_data={}
    travel_data['bus']=int(user_info['bus'])
    travel_data['taxi']=int(user_info['taxi'])
    travel_data['train']=int(user_info['train'])
    travel_data['car']=int(user_info['car'])
    travel_data['bike']=int(user_info['bike'])
    #travel_data['bicycle']=0
    travel_data['fly']=int(user_info['flying'])
    travel_data['walking']=0
    travel_data['dates']=today_date

    time={}
    time['hour']=int(user_info['hour'])
    time['minutes']=int(user_info['minute'])
    
    db_S_respond='Registered'#db_S.example(user_info)
    #latest_date=db_S.latestDate(session['user'])
    if db_S.check_dates(session['user'], today_date):
        calc_S.x = int(db_S.fetch_data(session['user'],'user_output','carbon_footprint',today_date)) #total co2 from databse
        
        calc_S.elec = 0
        calc_S.food_f((db_S.fetch_data(session['user'],'user_input', 'diet',today_date))) #food
        calc_S.travel = int(db_S.fetch_data(session['user'],'user_input', 'travel', today_date)) #travel
        
        calc_S.delete_data()
        db_S.update_travel_table(session['user'],travel_data,today_date)

        
        calc_S.travel_f(travel_data, time)
        
        food_type=user_info['food']
        calc_S.food_f(food_type)

        #elec['bill']=user_info['elec_bill']
        #elec['members']=user_info['no_of_member']
        #calc_S.elec_f(int(user_info['elec_bill']), int(user_info['no_of_member']))
        
        user_input={}
        user_input['travel']=calc_S.travel
        #elec={}
        user_input['diet']=user_info['food']
        user_input['elec']=calc_S.elec
        user_input['no_of_flights']=int(user_info['flying'])
        user_input['dates']=today_date

        db_S.update_user_input_table(session['user'], user_input, today_date)

        calc_S.entry_every_day()

        db_S.update_data(session['user'], 'user_output', 'carbon_footprint',calc_S.x, today_date)

    else:
        latestDate = db_S.latest_date(session['user'], 'user_output')

        calc_S.x = int(db_S.fetch_data(session['user'],'user_output','carbon_footprint',latestDate)) #total co2 from databse
        
        db_S.write_travel_table(session['user'], travel_data)
    
        calc_S.travel_f(travel_data, time)
        
        food_type=user_info['food']
        calc_S.food_f(food_type)

        #elec['bill']=user_info['elec_bill']
        #elec['members']=user_info['no_of_member']
        #calc_S.elec_f(int(user_info['elec_bill']), int(user_info['no_of_member']))
        
        user_input={}
        user_input['travel']=calc_S.travel
        #elec={}
        user_input['diet']=user_info['food']
        user_input['elec']=0
        user_input['no_of_flights']=int(user_info['flying'])
        user_input['dates']=today_date
        db_S.write_user_input_table(session['user'], user_input)

        
        db_S_respond='Registered'#db_S.example(user_info)
        
        calc_S.entry_every_day()
        user_output={}
        user_output['carbon_footprint']=calc_S.x
        
        user_output['monthly_average']=int(db_S.fetch_data(session['user'], 'user_output', 'monthly_average', latestDate))
        user_output['dates']=today_date
        db_S.write_output_table(session['user'], user_output)

    
    #put output values in output_table
    return jsonify(resp1='Correct', resp2=db_S_respond)

#QUESTIONARE FILLING /END******************************


#@app.route("/")
# User's account page. Left to be done
@app.route('/MyAccount')
def My_Account():
    if not ('user' in session):
       return redirect('/')
    
    
    if not db_S.check_user_input_table(session['user']):
        return redirect('/questionare')

    today_date=db_S.latest_date(session['user'], 'user_output')#str(datetime.datetime.date(datetime.datetime.now()))
    calc_S.avg=db_S.fetch_data(session['user'], 'user_output', 'monthly_average', today_date)
    calc_S.x=db_S.fetch_data(session['user'], 'user_output', 'carbon_footprint', today_date)
    calc_S.goal_selector()

    d= date.today()
    travel = db_S.get_table_data(session['user'], 'travel','user_input',d)
    elec = db_S.get_table_data(session['user'], 'electricity','user_input',d)
    food = db_S.get_food_total(session['user'], d)
    t_food=0
    for i in food:
        calc_S.food_f(i)
        t_food+=calc_S.food
        #print(i,str(calc_S.food))

    #print(t_food)
    #input()
    fly = db_S.get_table_data(session['user'], 'fly','travel',d)
    print(fly)
    car_taxi = db_S.get_table_data(session['user'], 'car','travel',d) + db_S.get_table_data(session['user'], 'taxi','travel',d)
    print(car_taxi)
    motorbike = db_S.get_table_data(session['user'], 'motorbike', 'travel',d)
    print(motorbike)
    # Details of the parameters taken in from the questionaire. Stored in the database. Graph is plotted. Things to be calculated according to formulae present here.
    #https://docs.google.com/document/d/1qZepM5Bbe13qaWUCraEf1Hmmb-otN7MImFnaBgSw44w/edit?ts=60bf9810
    return render_template('dashboard.html', avg=calc_S.avg, x=calc_S.x, percent=(calc_S.r/calc_S.avg), elec=elec, travel=travel, food=t_food, fly = fly, car_taxi = car_taxi, motorbike=motorbike)

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
    
    if not db_S.check_user_input_table(session['user']):
        return redirect('/questionare')
    
    state = db_S.fetch_user(session['user'], 'location_state')
    #if not db_S.check_user_input_table(session['user']):
    #    return redirect('/questionare')
#    Details of the parameters taken in from the questionaire. Stored in the database. Graph is plotted. Things to be calculated according to formulae present here.
#    https://docs.google.com/document/d/1qZepM5Bbe13qaWUCraEf1Hmmb-otN7MImFnaBgSw44w/edit?ts=60bf9810
    return render_template('user.html', fullname=session['user']['name'], state=state, email=session['user']['email'])


@app.route('/community')
def community():
    if not( 'user' in session):
        return redirect('/')

    if not db_S.check_user_input_table(session['user']):
        return redirect('/questionare')

    return render_template('community.html')



if __name__ == '__main__':
    app.run(debug=True)

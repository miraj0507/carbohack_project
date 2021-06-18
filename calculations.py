import datetime

import os, sys
sys.path.append(".")
from databse import Database_Soumee


class Calculations():

    def __init__(self):
        pass



    db_S = Database_Soumee()
    x = 0
    avg = 0
    g = 200
    goal = 0
    r = 0

    travel = 0
    food = 0
    elec = 0

    summ = 0

    def goal_selector(self):
        if self.avg > self.g:
            self.goal = self.g
            self.r = self.avg - self.g
        else:
            self.goal = self.avg
            self.r = 0



    def travel_f(self, travel_data, t):
        time = lambda percent: (percent/10)*((t['hour']*60 + t['minutes'])/60)

        #fly = [0,0,0] #db_S.example('fly')
        fly_emi = 138.45*(time(travel_data['fly']))

        #car = [0,0,0] #db_S.example('fly')
        car_emi = 0.23*35*(time(travel_data['car']))

        #train = [0,0,0] #db_S.example('fly')
        train_emi = 0.035*80*(time(travel_data['train']))

        #bus = [0,0,0] #db_S.example('fly')
        bus_emi = 0.5*35*(time(travel_data['bus']))/20

        #motorbike = [0,0,0] #db_S.example('fly')
        motorbike = 0.23*40*(time(travel_data['bike']))

        #bicycle = [0,0,0] #db_S.example('fly')
        bicycle_emi = 0

        #walking = [0,0,0] #db_S.example('fly')
        walking_emi = 0

        #taxi = [0,0,0] #db_S.example('fly')
        taxi_emi = 0.23*30*(time(travel_data['taxi']))

        self.travel = car_emi+train_emi+bus_emi+motorbike+taxi_emi+fly_emi



    
    def food_f(self, food_choice):
        #food_choice = '' #db_S.example()
        #print(food_choice)
        if food_choice == 'Vegan':
            self.food = 2.89
        elif food_choice == 'Vegetarian':
            self.food = 3.81
        elif food_choice == 'Pescatarian':
            self.food = 3.91
        elif food_choice == 'low meat':
            self.food = 4.67
        elif food_choice == 'lots of meat':
            self.food = 7.19
        #return self.food

    def elec_f(self, spend, no_of_people=1):
        #spend, no_of_people = (0,1) # db_S.example
        spend = spend/no_of_people
        self.elec = spend*0.42/(30*6)

    def initial_set_up(self, fli):
        flight = int(fli) #db_S.example()
        fly = 138.45*2*flight
        print(f"travel {self.travel} food {self.food} elec{self.food}")
        self.avg = (self.travel + self.food + self.elec)*30 + fly/12

        self.summ = self.avg

        date = int((datetime.datetime.now()).strftime("%d")) - 1
        print(f"date {date} avg {self.avg}")

        self.x = (self.avg/30)*date

        self.goal_selector()

        

    def delete_data(self):
        self.x = self.x - (self.travel + self.food + self.elec)

    def entry_every_day(self):
        self.x = self.x + self.travel + self.food + self.elec
        
    def first_month(self):
        self.summ = self.summ + self.x
        self.avg = self.sum/2
        self.x = 0

        self.goal_selector()
    
    def calculate_month(self):
        creation_month, creation_year = (0,0) #db_S.example()
        current_month = int((datetime.datetime.now()).strftime("%m"))
        current_year =  int((datetime.datetime.now()).strftime("%y"))
        month_spend = 0

        if current_year == creation_year:
            month_spend = current_month - creation_month
        else:
            month_spend = (12-creation_month) + (current_year - creation_year-1)*12 + current_month
        
        return month_spend


    def first_of_every_month(self):
        month = 0 #self.calculate_month()

        self.summ += self.x

        self.avg = self.summ/(month+1)

        self.x = 0

        self.goal_selector()

import datetime

import os, sys
sys.path.append(".")
from databse import Database_Soumee


class Calculations():

    def __init__():
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

    def travel_f(self):
        time = lambda percent, hr, minutes: (percent/10)*((hr*60 + minutes)/60)

        fly = [0,0,0] #db_S.example('fly')
        fly_emi = 138.45*(time(fly[0],fly[1], fly[2]))

        car = [0,0,0] #db_S.example('fly')
        car_emi = 0.23*35*(time(car[0],car[1],car[2]))

        train = [0,0,0] #db_S.example('fly')
        train_emi = 0.035*80*(time(train[0], train[1], train[2]))

        bus = [0,0,0] #db_S.example('fly')
        bus_emi = 0.5*35*(time(bus[0],bus[1],bus[2]))/20

        motorbike = [0,0,0] #db_S.example('fly')
        motorbike = 0.23*40*(time(motorbike[0], motorbike[1], motorbike[2]))

        bicycle = [0,0,0] #db_S.example('fly')
        bicycle_emi = 0

        walking = [0,0,0] #db_S.example('fly')
        walking_emi = 0

        taxi = [0,0,0] #db_S.example('fly')
        taxi_emi = 0.23*30*(time(taxi[0], taxi[1], taxi[2]))

    
    def food_f(self):
        food_choice = '' #db_S.example()
        if food_choice == 'Vegan':
            self.food = 2.89
        elif food_choice == 'Vegetarian':
            self.food = 3.81
        elif food_choice == 'Pescatarian':
            self.food = 3.91
        elif food_choice == 'Low meat':
            self.food = 4.67
        elif food_choice == 'High meat':
            self.food = 7.19

    def elec_f(self):
        spend, no_of_people = (0,0) # db_S.example
        spend = spend/no_of_people
        self.elec = spend*0.42/(30*6)

    def initial_set_up(self):
        flight = 0 #db_S.example()
        fly = 138.45*2*flight

        self.avg = (self.travel + self.food + self.elec)*30 + fly/12

        self.summ = self.avg

        date = (datetime.datetime.now()).strftime("%d") - 1

        self.x = (self.avg/30)*date

        if self.avg > self.g:
            self.goal = self.g
            self.r = self.avg - self.g
        else:
            self.goal = self.avg
            self.r = 0

    def delete_data(self):
        self.x = self.x - (self.travel + self.food + self.elec)

    def entry_every_day(self):
        self.x = self.x + self.travel + self.food + self.elec
        
    def first_month(self):
        self.summ = self.summ + self.x
        self.avg = self.sum/2
        self.x = 0

        if self.avg > self.g:
            self.goal = self.g
            self.r = self.avg - self.g
        else:
            self.goal = self.avg
            self.r = 0
    
    def calculate_month(self):
        creation_month, creation_year = (0,0) #db_S.example()
        current_month = (datetime.datetime.now()).strftime("%m")
        current_year =  (datetime.datetime.now()).strftime("%y")
        month_spend = 0

        if current_year == creation_year:
            month_spend = current_month - creation_month
        else:
            month_spend = (12-creation_month) + (current_year - creation_year-1)*12 + current_month
        
        return month_spend


    def first_of_every_month(self):
        month = self.calculate_month()

        self.summ += self.x

        self.avg = self.summ/(month+1)

        self.x = 0

        if self.avg > self.g :
            self.goal = self.g
            self.r = self.avg - self.g

        else:
            self.goal = self.avg
            self.r = 0
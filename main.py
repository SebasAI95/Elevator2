import random

import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import numpy as np
from time import sleep

#App
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databases/elevator.db'
db = SQLAlchemy(app,session_options={"autoflush": False})

class Demands(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #Objective level
    lvl_object = db.Column(db.Integer, default = 1)
    #Current level (random number)
    lvl_current = db.Column(db.Integer, default = 1)
    #Resting_lvl
    lvl_rest = db.Column(db.Integer, default = 1)
    #Demand date
    lvl_date = db.Column(db.DateTime, default = datetime.now())

db.create_all()


@app.route('/')
def root():

    demands = Demands.query.all()
    demands2 = []
    id = []
    date = []
    lvl_rest = []
    lvl_curr = []
    lvl_obj = []

    for dm in demands:
        if dm.id > 1:
            id.append(dm.id)
            date.append(dm.lvl_date)
            lvl_rest.append(dm.lvl_rest)
            lvl_curr.append(dm.lvl_current)
            lvl_obj.append(dm.lvl_object)

            demands2.append(str(dm.lvl_date.strftime("%m/%d/%Y, %H:%M:%S")) + " Elevator resting on " + str(dm.lvl_rest) + " and demand from level " + str(dm.lvl_current) + " to level " + str(dm.lvl_object))

    demands = pd.DataFrame()
    demands['id'] = id
    demands['rest'] = lvl_rest
    demands['curr'] = lvl_curr
    demands['obj'] = lvl_obj

    demands.to_csv('demands.csv',index=False)



    return render_template('index.html', demands2 = demands2)

@app.route('/demands', methods=['POST'])
def demand():
    n = request.form['demands_number']

    #create initial elevator state
    ini = Demands.query.first()
    #if Demands database empty
    if not ini:
        dem_init = Demands()
        db.session.add(dem_init)
        db.session.commit()

    rest_ini = 1

    for i in range(int(n)):
        act_db = Demands.query.all()

        curr_lvl = np.random.randint(1, high=11, size=1, dtype=int)
        curr_lvl = int(curr_lvl[0])
        list = np.array(np.linspace(1,10,10))
        id_curr = np.where(list == curr_lvl)
        list = np.delete(list,id_curr[0][0])
        obj_lvl = random.choice(list)
        lvl_rest = rest_ini
        rest_ini = obj_lvl
        print("lvl_rest is ", lvl_rest)

        #delaytime
        sleep(random.randint(2,8))
        date_lvl = datetime.now()

        demand = Demands(lvl_object = obj_lvl, lvl_current = curr_lvl, lvl_rest = lvl_rest, lvl_date = date_lvl)
        db.session.add(demand)

    db.session.commit()

    return redirect(url_for('root'))

if __name__ == '__main__':
    app.run(debug=True)



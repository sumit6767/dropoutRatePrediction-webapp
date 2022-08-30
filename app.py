from flask import Flask,render_template,request,session, url_for, redirect,flash

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
#from sklearn import datasets
import pickle
import pymysql
import numpy as np
import math
import pickle
import collections
from sklearn.metrics import average_precision_score
from sklearn.model_selection import cross_val_score
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_curve
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score,recall_score
from sklearn.metrics import roc_auc_score,roc_curve
from sklearn.metrics import auc
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import re

import sys
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def dbConnection():
    connection = pymysql.connect(host="localhost", user="root", password="root", database="studdrop")
    return connection

def dbClose():
    dbConnection().close()
    return


app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/home.html')
def home():
    return render_template('home.html')

@app.route('/predict',methods=['POST','GET'])
def prediction():
    if request.method == "POST":
        dict = {'completeprocess':request.form.get("completeprocess"),
                'weatherroads':request.form.get("weatherroads"),
                'Minority':request.form.get("Minority"),
                'teachertrain':request.form.get("teachertrain"),
                'schoolmanage':request.form.get("schoolmanage"),
                'mediumofinstr':request.form.get("mediumofinstr"),
                'gp':request.form.get("gp"),
                'Electricity_Connection':request.form.get("Electricity_Connection"),
                'not_having_Playground':request.form.get("not_having_Playground"),
                'not_having_Library':request.form.get("not_having_Library"),
                'not_having_Furniture':request.form.get("not_having_Furniture"),
                'Boys_Toilet':request.form.get("Boys_Toilet"),
                'Girls_Toilet':request.form.get("Girls_Toilet"),
                'Drinking_Water_Facility':request.form.get("Drinking_Water_Facility"),
                "Medical_Checkup_Facility" :request.form.get("Medical_Checkup_Facility"),
                "Internet_Facility" : request.form.get("Internet_Facility"),
                "Computer_Available" :  request.form.get("Computer_Available"),
                "Pupil_teacher" : request.form.get("Pupil_teacher"),
                "Professional_Qualification" : request.form.get("Professional_Qualification")}
        df=pd.DataFrame(dict,index=[0])
        #flash(df)
        with open('model_pkl_RandomForestRegressor2.sav','rb') as f:
            mp=pickle.load(f)
        red=mp.predict(df)

        
        flash("Student Dropout Rate Predicted "+str(red[0])+" %")
        imagepath="static/image/Feature Importance.jpg"
        return render_template('prediction.html',imagepath=imagepath)
       
                
                
        
        
        
        
    
           
    return render_template('prediction.html')
            
        
        
           
            
            
     


@app.route('/register',methods=['POST','GET'] )
def register():
    if request.method == "POST":
        try:
            status=""
            fname = request.form.get("Name")
            add = request.form.get("add")
            email = request.form.get("email")
            pass1 =  request.form.get("pass1")
            con = dbConnection()
            cursor = con.cursor()
            cursor.execute('SELECT * FROM userdetailes WHERE email = %s', (email))
            res = cursor.fetchone()
            #res = 0
            if not res:
                sql = "INSERT INTO userdetailes (name, address,email,password) VALUES (%s,%s, %s, %s)"
                val = (fname ,add ,email ,pass1)
                print(sql," ",val)
                cursor.execute(sql, val)
                con.commit()
                status= "success"
                return render_template("login.html")
            else:
                status = "Already available"
            #return status
            return redirect(url_for('index'))
        except Exception as e:
            print(e)
            print("Exception occured at user registration")
            return redirect(url_for('index'))
        finally:
            dbClose()
    return render_template('register.html')


@app.route('/login',methods=['POST','GET'])
def login():
    msg = ''
    if request.method == "POST":
        session.pop('user',None)
        mailid = request.form.get("email")
        password = request.form.get("pass1")
        #print(mobno+password)
        con = dbConnection()
        cursor = con.cursor()
        result_count = cursor.execute('SELECT * FROM userdetailes WHERE email = %s AND password = %s', (mailid, password))
        #a= 'SELECT * FROM userdetails WHERE mobile ='+mobno+'  AND password = '+ password
        print(result_count)
        #result_count=cursor.execute(a)
        # result = cursor.fetchone()
        if result_count>0:
            print(result_count)
            session['user'] = mailid
            return render_template("home.html")
        else:
            print(result_count)
            msg = 'Incorrect username/password!'
            return msg
    return render_template('login.html')


@app.route('/about')
def aboutus():
    return render_template('aboutus.html')
@app.route('/analysis.html')
def analysis():
   return render_template('analysis.html')
@app.route('/modification.html')
def Modification():
    return render_template('modification.html')


if __name__=="__main__":
    app.run("0.0.0.0")
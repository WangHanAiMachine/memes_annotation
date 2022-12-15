from flask import Flask, render_template, request, redirect, url_for, flash, session
from apscheduler.schedulers.background import BackgroundScheduler
from bs4 import BeautifulSoup
from threading import Timer
import sqlite3
import time
import datetime
from datetime import timedelta
import hashlib
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Rckjr43jkiubfheriuggrb34f34'


@app.route('/consentPage', methods = ['GET','POST'])
def consentPage():
    if request.method == 'POST':
        aggreement = request.form["aggreement"]
        if(aggreement != "yes"):
            flash('Aggreement is required to continue the survey')
            return redirect(url_for('consentPage'))
        else:
            tweetId, strategyId, annotationId, startTime= sampleQuestion()
            a = random.randint(1, 10)
            b = random.randint(1, 10)
            correctAnswer = a + b 

            session.permanent = True
            session["tweetId"] = str(tweetId)
            session["strategyId"] = str(strategyId)
            session["annotationId"] = str(annotationId)
            app.permanent_session_lifetime = timedelta(minutes=30)
            session.modified = True 

            return redirect(url_for('questionPage', tweetId=tweetId, strategyId=strategyId, annotationId=annotationId, startTime=startTime, a=a, b=b, correctAnswer=correctAnswer))

    return render_template('consentPage.html')

@app.route('/questionPage/<tweetId>/<strategyId>/<annotationId>/<startTime>/<a>/<b>/<correctAnswer>', methods = ['GET','POST'])
def questionPage(tweetId, strategyId, annotationId, startTime, a, b, correctAnswer):
    if("tweetId" in session and "strategyId" in session and "annotationId" in session):
        if(str(tweetId) in session["tweetId"] and str(strategyId) in session["strategyId"] and str(annotationId) in session["annotationId"]):

            tweet, explanation, explanation1, explanation2 = loadQuestion(int(tweetId), int(strategyId))

            numbers = list(range(1, 100))
            numbers.remove(int(correctAnswer))
            ansList = [random.choice(numbers), random.choice(numbers), random.choice(numbers)]
            ansList.insert(random.randint(0, 3), int(correctAnswer))

            if(int(tweetId) < 0  or int(strategyId) < 0 or int(annotationId) < 0):
                return redirect(url_for('notAvaiablePage'))
            
            if request.method == 'POST' and checkProgress(request, strategyId):
                fluency = -1
                informativeness = -1
                persuasiveness = -1
                soundness = -1
                fluency2 = -1
                informativeness2 = -1
                persuasiveness2 = -1
                soundness2 = -1
                if(str(strategyId) != "1"):
                    fluency = request.form["fluency"]
                    informativeness = request.form["informativeness"]
                    persuasiveness = request.form["persuasiveness"]
                    soundness = request.form["soundness"]
                    if(str(strategyId) == "6" or str(strategyId) == "7"):
                        fluency2 = request.form["fluencyExp2"]
                        informativeness2 = request.form["informativenessExp2"]
                        persuasiveness2 = request.form["persuasivenessExp2"]
                        soundness2 = request.form["soundnessExp2"]
                hatefulness = request.form["hatefulness"]
                controlQuestion = request.form["controlQuestion"]

                m = hashlib.md5()
                id = (str(tweetId) + str(strategyId) + str(annotationId)).encode('utf-8')
                m.update(id)
                surveyCode = str(int(m.hexdigest(), 16))[0:12]

                if(int(controlQuestion) ==int(correctAnswer) ):
                    submitQuestion(tweetId, strategyId, annotationId, int(startTime), surveyCode, fluency, fluency2, \
                        informativeness, informativeness2, persuasiveness, persuasiveness2, soundness, soundness2, hatefulness)

                    return redirect(url_for('endPage', surveyCode = surveyCode))
                else:
                    print()
                    return redirect(url_for('wrongAnswerPage', tweetId=tweetId, strategyId=strategyId, annotationId=annotationId))

            elif request.method == 'POST':
                flash('Before submitting, kindly respond to all of the questions.')
            
            
            return render_template('questionPage.html', tweet = tweet, explanation = explanation, explanation1=explanation1, \
            explanation2=explanation2, tweetId = tweetId, strategyId = strategyId, a=a, b=b, ansList=ansList)
        else:
            return redirect(url_for('timeOutPage'))

    else:
        return redirect(url_for('timeOutPage'))



@app.route('/endPage/<surveyCode>', methods = ['GET','POST'])
def endPage(surveyCode):
    return render_template('endPage.html', surveyCode=surveyCode)

@app.route('/wrongAnswerPage/<tweetId>/<strategyId>/<annotationId>')
def wrongAnswerPage(tweetId, strategyId, annotationId):
    conn = get_db_connection()
    conn.execute('DELETE FROM inprogress WHERE tweetId = ? AND strategyId = ? AND annotationId = ?', 
                        (tweetId, strategyId, annotationId))

    conn.execute('UPDATE questionsStatus SET annotated = ?'
                    ' WHERE tweetId = ? AND strategyId = ? AND annotationId = ?', 
                    (0, tweetId, strategyId, annotationId))
    conn.commit()
    conn.close()
    session.clear()
    return render_template('wrongAnswerPage.html')

@app.route('/timeOutPage')
def timeOutPage():
    return render_template('timeOutPage.html')

@app.route('/notAvaiablePage')
def notAvaiablePage():
    return render_template('notAvaiablePage.html')

def sampleQuestion():
    conn = get_db_connection()
    questionsStatus = conn.execute('SELECT * FROM questionsStatus').fetchall()
    tweetId = -1
    strategyId = -1
    annotationId = -1
    for record in questionsStatus:
        if(int(record["annotated"]) == 0):
            tweetId = record["tweetId"]
            strategyId = record["strategyId"]
            annotationId = record["annotationId"]
            break

    conn.execute('UPDATE questionsStatus SET annotated = ?'
                         ' WHERE tweetId = ? AND strategyId = ? AND annotationId = ?',
                         (1, tweetId, strategyId, annotationId))

    startTime = int(time.time())
    conn.execute("INSERT INTO inprogress (tweetId, strategyId, annotationId, startTime ) VALUES (?, ?, ?, ?)",
            (tweetId, strategyId, annotationId, startTime)
            )
    conn.commit()
    conn.close()
    return tweetId, strategyId, annotationId, startTime


def loadQuestion(tweetId, strategyId):
    conn = get_db_connection()
    tweet = conn.execute('SELECT tweet FROM questionsBank WHERE tweetId = ?',
                         (tweetId,)).fetchall()[0][0]
    explanation = "None"
    explanation1 = "None"
    explanation2 = "None"

    if(strategyId == 2):
        explanation = conn.execute('SELECT hateExpWO FROM questionsBank WHERE tweetId = ?',
                         (tweetId,)).fetchall()[0][0]
    if(strategyId == 3):
        explanation = conn.execute('SELECT nonhateExpWO FROM questionsBank WHERE tweetId = ?',
                         (tweetId,)).fetchall()[0][0]
    if(strategyId == 4):
        explanation = conn.execute('SELECT hateExpStep FROM questionsBank WHERE tweetId = ?',
                         (tweetId,)).fetchall()[0][0]

    if(strategyId == 5):
        explanation = conn.execute('SELECT nonhateExpStep FROM questionsBank WHERE tweetId = ?',
                         (tweetId,)).fetchall()[0][0]
    if(strategyId == 6):
        explanation1 = conn.execute('SELECT hateExpWO FROM questionsBank WHERE tweetId = ?',
                         (tweetId,)).fetchall()[0][0]
        explanation2 = conn.execute('SELECT nonhateExpWO FROM questionsBank WHERE tweetId = ?',
                         (tweetId,)).fetchall()[0][0]

    if(strategyId == 7):
        explanation1 = conn.execute('SELECT hateExpStep FROM questionsBank WHERE tweetId = ?',
                         (tweetId,)).fetchall()[0][0]
        explanation2 = conn.execute('SELECT nonhateExpStep FROM questionsBank WHERE tweetId = ?',
                         (tweetId,)).fetchall()[0][0]

    if(strategyId == 8):
        explanation = conn.execute('SELECT contxtExp FROM questionsBank WHERE tweetId = ?',
                         (tweetId,)).fetchall()[0][0]

    conn.close()
    return tweet, explanation, explanation1, explanation2



def submitQuestion(tweetId, strategyId, annotationId, startTime, surveyCode, fluency, fluency2, informativeness,\
     informativeness2, persuasiveness, persuasiveness2, soundness, soundness2, hatefulness):
    conn = get_db_connection()
    cur_time = time.time()
    cur_time_format = datetime.datetime.fromtimestamp(cur_time).strftime('%Y-%m-%d %H:%M:%S')
    startTime = datetime.datetime.fromtimestamp(int(startTime)).strftime('%Y-%m-%d %H:%M:%S')

    conn.execute('DELETE FROM inprogress WHERE tweetId = ? AND strategyId = ? AND annotationId = ?', (tweetId, strategyId, annotationId))
    
    conn.execute("INSERT INTO submitted (tweetId, strategyId, annotationId, startTime, end_time, surveycode, fluency, informativeness, persuasiveness, soundness, fluency2, informativeness2, persuasiveness2, soundness2, hatefulness) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (tweetId, strategyId, annotationId, startTime, cur_time_format, surveyCode, fluency, informativeness, persuasiveness, soundness, fluency2, informativeness2, persuasiveness2, soundness2, hatefulness)
            )
    conn.commit()
    conn.close()
    session.clear()


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def checkProgress(request, strategyId):
    if(str(strategyId) == "1"):
        return "hatefulness" in request.form and "controlQuestion" in request.form
    elif(str(strategyId) == "6" or str(strategyId) == "7"):
        return "fluency" in request.form and "fluencyExp2" in request.form and "informativeness" in request.form and "informativenessExp2" in request.form\
            and "persuasiveness" in request.form  and "persuasivenessExp2" in request.form and "soundness" in request.form and "soundnessExp2" in request.form \
           and "hatefulness" in request.form and "controlQuestion" in request.form
    else:
        return "fluency" in request.form and "informativeness" in request.form and "persuasiveness" in request.form \
            and "soundness" in request.form and "hatefulness" in request.form and "controlQuestion" in request.form



def checkTimeOut():
    cur_time = int(time.time())
    conn = get_db_connection()

    inProgress = conn.execute('SELECT * FROM inProgress').fetchall()
    for record in inProgress:
        startTime = record["startTime"]
        if((cur_time-startTime)//60 > 30):
            tweetId = record["tweetId"]
            strategyId = record["strategyId"]
            annotationId = record["annotationId"]

            conn.execute('DELETE FROM inprogress WHERE tweetId = ? AND strategyId = ? AND annotationId = ?', 
                        (tweetId, strategyId, annotationId))

            conn.execute('UPDATE questionsStatus SET annotated = ?'
                         ' WHERE tweetId = ? AND strategyId = ? AND annotationId = ?', 
                         (0, tweetId, strategyId, annotationId))
            conn.commit()
    conn.close()

scheduler = BackgroundScheduler()
scheduler.add_job(func=checkTimeOut, trigger="interval", seconds=60) # check
scheduler.start()
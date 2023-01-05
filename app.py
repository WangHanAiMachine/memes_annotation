from flask import Flask, render_template, request, redirect, url_for, flash, session
from apscheduler.schedulers.background import BackgroundScheduler
import sqlite3
import time, datetime
from datetime import timedelta
import hashlib, random
from flask_ngrok import run_with_ngrok
import random
import string
  
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Rckjr43jkiubfheriuggrb34f34'
run_with_ngrok(app)

@app.route('/', methods = ['GET','POST'])
def consentPage():
    agreement = "None"
    if("agreement" in session):
        agreement = session["agreement"]
     
    if('user_id' in request.args and 'user_id' not in session):
        user_id = request.args.get('user_id')
        conn = get_db_connection()
        user_ids = conn.execute('SELECT user_id FROM recordedUser').fetchall()
        conn.close()
        user_ids = [item[0] for item in user_ids]
        
        if(user_id in user_ids):
            session.clear()
            return redirect(url_for('multipleAccessPage'))
        else:
            session["user_id"] = str(user_id)
    elif('user_id' not in request.args and 'user_id' not in session):
        session.clear()
        return redirect(url_for('noUserIdPage'))

    if request.method == 'GET':
        return render_template('consentPage.html', agreement = agreement)

    elif request.method == 'POST':
        if("agreement" in request.form):
            agreement = request.form["agreement"]
            session["agreement"] = agreement

        if(agreement != "yes"):
            flash('agreement is required to continue the survey')
            return redirect(url_for('consentPage'))
        else:
            if("tweetId" in session and "strategyId" in session and "annotationId" in session):
                return redirect(url_for('questionPage'))
            else:
                user_id = session["user_id"]
                tweetId, strategyId, annotationId, startTime= sampleQuestion()
                a = random.randint(1, 10)
                b = random.randint(1, 10)
                session.permanent = True
                session["tweetId"] = str(tweetId)
                session["strategyId"] = str(strategyId)
                session["annotationId"] = str(annotationId)
                session["startTime"] = str(startTime)
                session["a"] = str(a)
                session["b"] = str(b)

                correctAns = int(a) + int(b)
                ansList = [correctAns-3, correctAns-2,correctAns-1, correctAns, correctAns+1, correctAns+2, correctAns+3]
                index = random.randint(0, 3)
                ansList = ansList[index:index+4]
                random.shuffle(ansList)
                session["ansList1"] = ansList[0]
                session["ansList2"] = ansList[1]
                session["ansList3"] = ansList[2]
                session["ansList4"] = ansList[3]
                app.permanent_session_lifetime = timedelta(minutes=30, seconds=3) 
                session.modified = True 
                return redirect(url_for('questionPage'))



@app.route('/questionPage', methods = ['GET','POST'])
def questionPage():
    if("tweetId" in session and "strategyId" in session and "annotationId" in session and "user_id" in session):
        
        tweetId  = session["tweetId"]
        strategyId = session["strategyId"]
        annotationId = session["annotationId"]
        startTime = session["startTime"]
        user_id =  session["user_id"]

        a = session["a"]
        b = session["b"]
        if(int(tweetId) < 0  or int(strategyId) < 0 or int(annotationId) < 0):
            session.clear()
            return redirect(url_for('notAvailablePage'))

        tweet, explanation, explanation1, explanation2 = loadQuestion(int(tweetId), int(strategyId))

        fluency = -1
        informativeness = -1
        persuasiveness = -1
        soundness = -1
        fluency2 = -1
        informativeness2 = -1
        persuasiveness2 = -1
        soundness2 = -1
        hatefulness = -1
        controlQuestion = -1
        ansList = []

        if("fluency" in session):
            fluency = session["fluency"]
            informativeness = session["informativeness"]
            persuasiveness = session["persuasiveness"]
            soundness = session["soundness"]
        if("fluency2" in session):
            fluency2 = session["fluency2"]
            informativeness2 = session["informativeness2"]
            persuasiveness2 = session["persuasiveness2"]
            soundness2 = session["soundness2"]
        if("hatefulness" in session):
            hatefulness = session["hatefulness"]
            controlQuestion = session["controlQuestion"]
        if("ansList1" in session):
            for i in range(1, 5):
                ansList.append(session["ansList" + str(i)])

        if request.method == 'POST':
                
            if("fluency" in request.form):
                fluency = request.form["fluency"]
            if("informativeness" in request.form):
                informativeness = request.form["informativeness"]
            if("persuasiveness" in request.form):
                persuasiveness = request.form["persuasiveness"]
            if("soundness" in request.form):
                soundness = request.form["soundness"]
            if("fluencyExp2" in request.form):
                fluency2 = request.form["fluencyExp2"]
            if("informativenessExp2" in request.form):
                informativeness2 = request.form["informativenessExp2"]
            if("persuasivenessExp2" in request.form):
                persuasiveness2 = request.form["persuasivenessExp2"]
            if("soundnessExp2" in request.form):
                soundness2 = request.form["soundnessExp2"]
            if("hatefulness" in request.form):
                hatefulness = request.form["hatefulness"]
            if("controlQuestion" in request.form):
                controlQuestion = request.form["controlQuestion"]

            session["fluency"] = fluency
            session["informativeness"] = informativeness
            session["persuasiveness"] = persuasiveness
            session["soundness"] = soundness
            session["fluency2"] = fluency2
            session["informativeness2"] = informativeness2
            session["persuasiveness2"] = persuasiveness2
            session["soundness2"] = soundness2
            session["hatefulness"] = hatefulness
            session["controlQuestion"] = controlQuestion

            if(checkProgress(request, strategyId)):
                
                # surveyCode = ''.join([random.choice(string.ascii_letters
                #             + string.digits) for n in range(16)])
                            
                # conn = get_db_connection()
                # surveyCodes = conn.execute('SELECT surveyCode FROM submitted').fetchall()
                # surveyCodes = [item[0] for item in surveyCodes]
                # while(surveyCode in surveyCodes):
                #     surveyCode = ''.join([random.choice(string.ascii_letters
                #                         + string.digits) for n in range(16)])
                # conn.close()

                surveyCode = "TOm7JHEJZ5vbVTNk"
                
                session.clear()
                if(int(controlQuestion) ==int(a) + int(b) ):
                    submitQuestion(user_id, tweetId, strategyId, annotationId, int(startTime), surveyCode, fluency, fluency2, \
                        informativeness, informativeness2, persuasiveness, persuasiveness2, soundness, soundness2, hatefulness)
                    return redirect(url_for('endPage', surveyCode = surveyCode))
                else:
                    closeSurvey(tweetId, strategyId, annotationId)
                    return redirect(url_for('wrongAnswerPage'))

            else:

                flash('Before submitting, please respond to all of the questions.')
                return redirect(url_for('questionPage'))

        elif request.method == 'GET':
            
            return render_template('questionPage.html', tweet = tweet, explanation = explanation, explanation1=explanation1, \
            explanation2=explanation2, tweetId = tweetId, strategyId = strategyId, startTime=startTime, a=a, b=b, ansList=ansList, \
                fluency=fluency, informativeness=informativeness, persuasiveness=persuasiveness, soundness=soundness,\
                fluency2=fluency2, informativeness2=informativeness2, persuasiveness2=persuasiveness2, soundness2=soundness2,\
                    hatefulness=hatefulness, controlQuestion=controlQuestion)
    return redirect(url_for('notAvailablePage'))


@app.route('/endPage/<surveyCode>', methods = ['GET','POST'])
def endPage(surveyCode):
    return render_template('endPage.html', surveyCode=surveyCode)

@app.route('/wrongAnswerPage')
def wrongAnswerPage():
    return render_template('wrongAnswerPage.html')

@app.route('/multipleAccessPage')
def multipleAccessPage():
    return render_template('multipleAccessPage.html')

@app.route('/noUserIdPage')
def noUserIdPage():
    return render_template('noUserIdPage.html')

@app.route('/notAvailablePage')
def notAvaiablePage():
    return render_template('notAvailablePage.html')

@app.route('/timeOutPage')
def timeOutPage():
    if("tweetId" in session and "strategyId" in session and "annotationId" in session):
        tweetId  = session["tweetId"]
        strategyId = session["strategyId"]
        annotationId = session["annotationId"]
        session.clear()
        closeSurvey(tweetId, strategyId, annotationId)
    return render_template('timeOutPage.html')

def sampleQuestion():
    conn = get_db_connection()
    questionsStatus = conn.execute('SELECT * FROM questionsStatus').fetchall()
    tweetId = -1
    strategyId = -1
    annotationId = -1
    startTime = int(time.time())
    for record in questionsStatus:
        if(int(record["annotated"]) == 0):
            tweetId = record["tweetId"]
            strategyId = record["strategyId"]
            annotationId = record["annotationId"]
            break

    if(tweetId >0 and strategyId > 0 and annotationId > 0):
        conn.execute('UPDATE questionsStatus SET annotated = ?'
                            ' WHERE tweetId = ? AND strategyId = ? AND annotationId = ?',
                            (1, tweetId, strategyId, annotationId))

        
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


def submitQuestion(user_id, tweetId, strategyId, annotationId, startTime, surveyCode, fluency, fluency2, informativeness,\
     informativeness2, persuasiveness, persuasiveness2, soundness, soundness2, hatefulness):
    conn = get_db_connection()
    cur_time = time.time()
    cur_time_format = datetime.datetime.fromtimestamp(cur_time).strftime('%Y-%m-%d %H:%M:%S')
    startTime = datetime.datetime.fromtimestamp(int(startTime)).strftime('%Y-%m-%d %H:%M:%S')
    conn.execute("INSERT INTO recordedUser (user_id, accepted ) VALUES (?, ?)",
                (user_id,  1)
                )

    conn.execute('DELETE FROM inprogress WHERE tweetId = ? AND strategyId = ? AND annotationId = ?', (tweetId, strategyId, annotationId))
    conn.execute('UPDATE questionsStatus SET annotated = ?'
                    ' WHERE tweetId = ? AND strategyId = ? AND annotationId = ?', 
                    (1, tweetId, strategyId, annotationId))

    conn.execute("INSERT INTO submitted (user_id, tweetId, strategyId, annotationId, startTime, end_time, surveycode, fluency, informativeness, persuasiveness, soundness, fluency2, informativeness2, persuasiveness2, soundness2, hatefulness) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (user_id, tweetId, strategyId, annotationId, startTime, cur_time_format, surveyCode, fluency, informativeness, persuasiveness, soundness, fluency2, informativeness2, persuasiveness2, soundness2, hatefulness)
            )
    conn.commit()
    conn.close()

def closeSurvey(tweetId, strategyId, annotationId):
    conn = get_db_connection()

    conn.execute('DELETE FROM inprogress WHERE tweetId = ? AND strategyId = ? AND annotationId = ?', 
                        (tweetId, strategyId, annotationId))

    conn.execute('UPDATE questionsStatus SET annotated = ?'
                    ' WHERE tweetId = ? AND strategyId = ? AND annotationId = ?', 
                    (0, tweetId, strategyId, annotationId))
    conn.commit()
    conn.close()


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
        if((cur_time-startTime)//60 >= 15):
            tweetId = record["tweetId"]
            strategyId = record["strategyId"]
            annotationId = record["annotationId"]

            closeSurvey(tweetId, strategyId, annotationId)
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
    
with app.app_context():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=checkTimeOut, trigger="interval", seconds=30) # check
    scheduler.start()

if __name__ == "__main__":
    app.run()
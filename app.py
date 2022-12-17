from flask import Flask, render_template, request, redirect, url_for, flash, session
from apscheduler.schedulers.background import BackgroundScheduler
import sqlite3
import time, datetime
from datetime import timedelta
import hashlib, random
from flask_ngrok import run_with_ngrok
  
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Rckjr43jkiubfheriuggrb34f34'
run_with_ngrok(app)

@app.route('/', methods = ['GET','POST'])
def consentPage():
    aggreement = "None"
    if("aggreement" in session):
        aggreement = session["aggreement"]

    if request.method == 'GET':
        return render_template('consentPage.html', aggreement = aggreement)

    elif request.method == 'POST':
        if("aggreement" in request.form):
            aggreement = request.form["aggreement"]
            session["aggreement"] = aggreement

        if(aggreement != "yes"):
            flash('Aggreement is required to continue the survey')
            return redirect(url_for('consentPage'))
        else:
            if("tweetId" in session and "strategyId" in session and "annotationId" in session):
                
                return redirect(url_for('questionPage'))
            else:
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
                app.permanent_session_lifetime = timedelta(minutes=30)
                session.modified = True 
                return redirect(url_for('questionPage'))


@app.route('/questionPage', methods = ['GET','POST'])
def questionPage():
    if("tweetId" in session and "strategyId" in session and "annotationId" in session):
        
        tweetId  = session["tweetId"]
        strategyId = session["strategyId"]
        annotationId = session["annotationId"]
        startTime = session["startTime"]
        a = session["a"]
        b = session["b"]
        if(int(tweetId) < 0  or int(strategyId) < 0 or int(annotationId) < 0):
            session.clear()
            return redirect(url_for('notAvaiablePage'))

        tweet, explanation, explanation1, explanation2 = loadQuestion(int(tweetId), int(strategyId))

        correctAns = int(a) + int(b)
        ansList = [correctAns-3, correctAns-2,correctAns-1, correctAns, correctAns+1, correctAns+2, correctAns+3]
        index = random.randint(0, 3)
        ansList = ansList[index:index+4]
        random.shuffle(ansList)

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

        if("fluency" in session):
            fluency = session["fluency"]
        if("fluency2" in session):
            fluency2 = session["fluency2"]
        if("informativeness" in session):
            informativeness = session["informativeness"]
        if("informativeness2" in session):
            informativeness2 = session["informativeness2"]
        if("persuasiveness" in session):
            persuasiveness = session["persuasiveness"]
        if("persuasiveness2" in session):
            persuasiveness2 = session["persuasiveness2"]
        if("soundness" in session):
            soundness = session["soundness"]
        if("soundness2" in session):
            soundness2 = session["soundness2"]
        if("hatefulness" in session):
            hatefulness = session["hatefulness"]
        if("controlQuestion" in session):
            controlQuestion = session["controlQuestion"]

        if request.method == 'POST':
            # cur_time = int(time.time())
            # if((cur_time-startTime)//60 > 1):
                
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
                m = hashlib.md5()
                id = (str(tweetId) + str(strategyId) + str(annotationId)).encode('utf-8')
                m.update(id)
                surveyCode = str(int(m.hexdigest(), 16))[0:12]

                session.clear()
                if(int(controlQuestion) ==int(a) + int(b) ):
                    submitQuestion(tweetId, strategyId, annotationId, int(startTime), surveyCode, fluency, fluency2, \
                        informativeness, informativeness2, persuasiveness, persuasiveness2, soundness, soundness2, hatefulness)
                    return redirect(url_for('endPage', surveyCode = surveyCode))
                else:
                    closeSurvey(tweetId, strategyId, annotationId)
                    return redirect(url_for('wrongAnswerPage'))

            else:

                flash('Before submitting, kindly respond to all of the questions.')
                return redirect(url_for('questionPage'))

        elif request.method == 'GET':
            
            return render_template('questionPage.html', tweet = tweet, explanation = explanation, explanation1=explanation1, \
            explanation2=explanation2, tweetId = tweetId, strategyId = strategyId, startTime=startTime, a=a, b=b, ansList=ansList, \
                fluency=fluency, informativeness=informativeness, persuasiveness=persuasiveness, soundness=soundness,\
                fluency2=fluency2, informativeness2=informativeness2, persuasiveness2=persuasiveness2, soundness2=soundness2,\
                    hatefulness=hatefulness, controlQuestion=controlQuestion)
    return redirect(url_for('notAvaiablePage'))


@app.route('/endPage/<surveyCode>', methods = ['GET','POST'])
def endPage(surveyCode):
    return render_template('endPage.html', surveyCode=surveyCode)

@app.route('/wrongAnswerPage')
def wrongAnswerPage():
    return render_template('wrongAnswerPage.html')

@app.route('/notAvaiablePage')
def notAvaiablePage():
    return render_template('notAvaiablePage.html')

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
        if((cur_time-startTime)//60 >= 30):
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
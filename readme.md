# Plush Survey APP

## 1. Activate virtual env (one-time set-up)

### If my_env folder not exists, run:  `python3 -m venv my_env`  to generate.
### Activate virtual environment by running:  `source my_env/bin/activate`

## 2. Initialize database

### Run `python init_db.py` to initialize the database, it will clear all recorded data, be careful to use it.

## 3. Run the survey app

### Run `flask run` to run the survey app, then copy http://127.0.0.1:5000/consentPage in brower to enter the survey.

## 4. Save all the data in csv format

### Run `python saveData.py`

# Development log

### 1. Add a timer to let the annoatoters know how much time is remaining. Finished.
### 2. Adding more details to the error message for the users who provided incorrect answers to the control questions.  Finished.
### 3. Modify the math problem so that incorrect responses are more likely to be near to the correct answer. Finished.
### 4. Using bootstrap to test the survey's mobile user interface. 
### 5. Make the tweet and exp float so that users can still see them even after scrolling to the bottom of the page.
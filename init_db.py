import sqlite3
import pandas as pd




tweet = pd.read_csv("questionBank/tweet.csv")
hate_exp_wo = pd.read_csv("questionBank/tweetHateExplanation.csv")
nonhate_exp_wo = pd.read_csv("questionBank/tweetNonHateExplanation.csv")
hate_exp_step = pd.read_csv("questionBank/tweetHateExplanationWithDetails.csv")
nonhate_exp_step = pd.read_csv("questionBank/tweetNonHateExplanationWithDetails.csv")
contxt_exp = pd.read_csv("questionBank/tweetContextExplanation.csv")

demo_size = range(75, 100)
strategy_size = [1] 
annotation_size = 3



connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    conn = sqlite3.connect('database.db', isolation_level=None,
                       detect_types=sqlite3.PARSE_COLNAMES)
    db_df = pd.read_sql_query("SELECT * FROM submitted", conn)
    db_df.to_csv('questionAnswer/submitted.csv', index=False)
    conn.close()

    connection.executescript(f.read())


cur = connection.cursor()

for i in demo_size: # demosize
    tweet_i = tweet["Tweet"][i]
    hate_exp_wo_i = hate_exp_wo["Explanation"][i]
    nonhate_exp_wo_i = nonhate_exp_wo["Explanation"][i]
    hate_exp_step_i = hate_exp_step["Explanation"][i]
    nonhate_exp_step_i = nonhate_exp_step["Explanation"][i]
    contxt_exp_i = contxt_exp["Explanation"][i]

    cur.execute("INSERT INTO questionsBank (tweetId, tweet, hateExpWO, nonhateExpWO, hateExpStep, nonhateExpStep, contxtExp) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (i + 1, tweet_i, hate_exp_wo_i, nonhate_exp_wo_i, hate_exp_step_i, nonhate_exp_step_i, contxt_exp_i)
                )
    

for i in range(76, 101): # demosize
    for j in strategy_size:
        for k in range(1, annotation_size + 1):
            cur.execute("INSERT INTO questionsStatus (tweetId, strategyId, annotationId) VALUES (?, ?, ?)",
                (i, j, k)
                )
            
connection.commit()
connection.close()

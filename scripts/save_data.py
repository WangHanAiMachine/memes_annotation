import sqlite3
import pandas as pd

results_dir = "../questionAnswer"

conn = sqlite3.connect('../database.db', isolation_level=None,
                       detect_types=sqlite3.PARSE_COLNAMES)

db_df = pd.read_sql_query("SELECT * FROM submitted", conn)
db_df.to_csv(f"{results_dir}/submitted.csv", index=False)

db_df = pd.read_sql_query("SELECT * FROM inprogress", conn)
db_df.to_csv(f"{results_dir}/inprogress.csv", index=False)

db_df = pd.read_sql_query("SELECT * FROM questionsStatus", conn)
db_df.to_csv(f"{results_dir}/questionsStatus.csv", index=False)

conn.close()
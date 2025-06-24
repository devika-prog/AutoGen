import json
import pandas as pd

def get_log(dbname="logs.db", table="chat_completions"):
    import sqlite3

    con = sqlite3.connect(dbname)
    query = f"SELECT * from {table}"
    cursor = con.execute(query)
    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    data = [dict(zip(column_names, row)) for row in rows]
    con.close()
    return data

def str_to_dict(s):
    return json.loads(s)


log_data = get_log()
log_data_df = pd.DataFrame(log_data)

log_data_df["total_tokens"] = log_data_df.apply(
    lambda row: str_to_dict(row["response"])["usage"]["total_tokens"], axis=1
)

log_data_df["request"] = log_data_df.apply(lambda row: str_to_dict(row["request"])["messages"][0]["content"], axis=1)

log_data_df["response"] = log_data_df.apply(
    lambda row: str_to_dict(row["response"])["choices"][0]["message"]["content"], axis=1
)

log_data_df
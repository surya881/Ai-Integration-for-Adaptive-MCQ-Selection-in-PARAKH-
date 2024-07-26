import json
import sqlite3
import random

db_name = "database.db"
def load_questions(filename):
  """
  Load questions from a JSON file and return them as a list of dictionaries.
  Each dictionary represents a question with keys: 'level', 'question', 'options', 'answer'.
  """
  with open(filename, 'r') as json_file:
    questions = json.load(json_file)
  return questions

easy_length, hard_length = 0, 0
def init_db():
    global easy_length, hard_length

    print("loading content to db ...")

    connection = sqlite3.connect('database.db')
    with open('schema.sql') as f:
        connection.executescript(f.read())
    cur = connection.cursor()

    for q in load_questions("questions.json"):
        if q["level"] == "Hard": hard_length += 1
        else: easy_length += 1
        table_name = "questions_" + q["level"].lower()
        cur.execute(f"INSERT INTO {table_name} (json) VALUES ('{json.dumps(q)}')")
    connection.commit()
    connection.close()

    print("db loaded succesfully ...")

easy_index, hard_index = 0, 0

def fetch_question(diff):
    global easy_index, hard_index

    table_name, index = 0, 0
    if diff == "easy":
        table_name = "questions_hard"
        easy_index = easy_index % easy_length + 1
        index = easy_index
    elif diff == "hard":
        table_name = "questions_hard"
        hard_index = hard_index % hard_length + 1
        index = hard_index
    else:
        raise Exception("invalid diff level in fetch_questions")

    query = f"SELECT json FROM {table_name} WHERE rowid = {index}"
    conn = sqlite3.connect(db_name)
    res = conn.execute(query).fetchone()
    conn.close()

    if res == None:
        raise Exception("query failed!")
    return json.loads(res[0])

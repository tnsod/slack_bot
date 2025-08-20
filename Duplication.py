import mysql.connector
from config import DB_CONFIG

def get_conn():
    return mysql.connector.connect(**DB_CONFIG)

def dup_id(user_text):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT BOJ_id FROM users")
    result = cur.fetchall()
    cur.close()
    conn.close()
    data = {i[0] for i in result}
    return user_text in data

def dup_name(user_id, user_text):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT user_id, user_name FROM users")
    result = cur.fetchall()
    cur.close()
    conn.close()
    for _id, name in result:
        if name == user_text and _id != user_id:
            return True
    return False

def same_name(user_id, user_text):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT user_id, user_name FROM users")
    result = cur.fetchall()
    cur.close()
    conn.close()
    for _id, name in result:
        if name == user_text and _id == user_id:
            return "same"
        elif name == user_text:
            return "duplicate"
    return "complete"
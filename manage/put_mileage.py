import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from src.utils.config import DB_CONFIG
import mysql.connector

def get_conn():
    return mysql.connector.connect(**DB_CONFIG)

def weekly_data():
    file = open('weekly.txt')
    data = file.read().split('\n')
    users = [[(user, 1), tuple(user.split())][' ' in user] for user in data]
    print(users)

def add(cur, BOJ_id, diff):
    cur.execute("""
                UPDATE users
                SET mileage = mileage + %i
                WHERE BOJ_ID=%s
            """,
                (diff, BOJ_id),
            )

def main():
    conn = get_conn()
    cur = conn.cursor()
    user = weekly_data()

    for u in user:
        id, diff = u
        diff = int(diff)
        add(cur, id, diff)
    
    cur.close()
    conn.close()

main()
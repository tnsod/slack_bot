import sqlite3

def dup_id(user_text):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('SELECT BOJ_id FROM users')
    result = cursor.fetchall()

    conn.commit()
    conn.close()

    data = set()
    for id in result:
        for i in id:
            data.add(i)

    if user_text in data:
        return True
    return False

def dup_name(user_id, user_text):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('SELECT user_id, user_name FROM users')
    result = cursor.fetchall()

    conn.commit()
    conn.close()

    for id, name in result:
        if name == user_text and id != user_id:
            return True
    return False

def same_name(user_id, user_text):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('SELECT user_id, user_name FROM users')
    result = cursor.fetchall()

    conn.commit()
    conn.close()

    for id, name in result:
        if name == user_text and id == user_id:
            return 'same'
        elif name == user_text:
            return 'duplicate'
    return 'complete'
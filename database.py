import sqlite3

class UserDB:
    def __init__(self, db_name='users.db'):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # user 정보
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                slack_name TEXT,
                BOJ_id TEXT,
                user_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # user 상태
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_states (
                user_id TEXT PRIMARY KEY,
                current_state TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_slack_name(self, user_id, slack_name):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO users (user_id, slack_name)
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                slack_name = ?
        ''', (user_id, slack_name, slack_name))
        
        conn.commit()
        conn.close()

    def save_user_info(self, user_id, BOJ_id=None, user_name=None):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT BOJ_id, user_name FROM users WHERE user_id = ?', (user_id,))
            existing = cursor.fetchone()
            
            if existing:
                current_id, current_name = existing
                new_id = BOJ_id if BOJ_id is not None else current_id
                new_name = user_name if user_name is not None else current_name
                
                cursor.execute('''
                    UPDATE users 
                    SET BOJ_id = ?, user_name = ?, updated_at = datetime('now')
                    WHERE user_id = ?
                ''', (new_id, new_name, user_id))
            else:
                cursor.execute('''
                    INSERT INTO users (user_id, BOJ_id, user_name)
                    VALUES (?, ?, ?)
                ''', (user_id, BOJ_id, user_name))
            
            conn.commit()
            
        except Exception as e:
            print(f"사용자 정보 저장 실패: {e}")
        finally:
            conn.close()
    
    def get_user_info(self, user_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT BOJ_id, user_name
                FROM users WHERE user_id = ?
            ''', (user_id,))
            
            result = cursor.fetchone()
            
            if result:
                return {
                    'BOJ_id': result[0],
                    'user_name': result[1]
                }
            return None
            
        except Exception as e:
            print(f"사용자 정보 조회 실패: {e}")
            return None
        finally:
            conn.close()
    
    def save_user_state(self, user_id, state):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO user_states (user_id, current_state)
                VALUES (?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    current_state = ?,
                    updated_at = datetime('now')
            ''', (user_id, state, state))
            
            conn.commit()
            
        except Exception as e:
            print(f"상태 저장 실패: {e}")
        finally:
            conn.close()
    
    def get_user_state(self, user_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT current_state FROM user_states WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()
            return result[0] if result else None
            
        except Exception as e:
            print(f"상태 조회 실패: {e}")
            return None
        finally:
            conn.close()
    
    def clear_user_data(self, user_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM user_states WHERE user_id = ?', (user_id,))
            cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
            conn.commit()
            
        except Exception as e:
            print(f"데이터 삭제 실패: {e}")
        finally:
            conn.close()
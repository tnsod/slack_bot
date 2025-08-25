from config import DB_CONFIG
from mysql.connector import pooling

class UserDB:
    def __init__(self, **kwargs):
        self.pool = pooling.MySQLConnectionPool(
            **{**DB_CONFIG, **kwargs}, charset="utf8mb4", autocommit=True
        )
        self.init_database()

    def _get_conn(self):
        return self.pool.get_connection()

    def init_database(self):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id VARCHAR(255) PRIMARY KEY,
                slack_name VARCHAR(255),
                BOJ_id VARCHAR(255),
                user_name VARCHAR(255),
                mileage TINYINT(1) NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS user_states (
                user_id VARCHAR(255) PRIMARY KEY,
                current_state VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        )
        # cur.execute(
        #     """
        #     CREATE TABLE IF NOT EXISTS user_friends (
        #         user_id VARCHAR(255) PRIMARY KEY,
        #         friend VARCHAR(255),
        #         friend_state TINYINT(1)
        #     ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        # """
        # )
        cur.close()
        conn.close()

    def save_slack_name(self, user_id, slack_name):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO users (user_id, slack_name)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE
                slack_name = VALUES(slack_name),
                updated_at = CURRENT_TIMESTAMP;
        """,
            (user_id, slack_name),
        )
        cur.close()
        conn.close()

    def save_user_info(self, user_id, BOJ_id=None, user_name=None):
        conn = self._get_conn()
        cur = conn.cursor(buffered=True)
        cur.execute("SELECT BOJ_id, user_name FROM users WHERE user_id=%s", (user_id,))
        row = cur.fetchone()
        if row:
            new_id = BOJ_id if BOJ_id is not None else row[0]
            new_name = user_name if user_name is not None else row[1]
            cur.execute(
                """
                UPDATE users
                SET BOJ_id=%s, user_name=%s, updated_at=CURRENT_TIMESTAMP
                WHERE user_id=%s
            """,
                (new_id, new_name, user_id),
            )
        else:
            cur.execute(
                """
                INSERT INTO users (user_id, BOJ_id, user_name)
                VALUES (%s, %s, %s)
            """,
                (user_id, BOJ_id, user_name),
            )
        cur.close()
        conn.close()

    def get_user_info(self, user_id):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT BOJ_id, user_name FROM users WHERE user_id=%s", (user_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return {"BOJ_id": row[0], "user_name": row[1]} if row else None

    def save_user_state(self, user_id, state):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO user_states (user_id, current_state)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE
                current_state=VALUES(current_state),
                updated_at=CURRENT_TIMESTAMP;
        """,
            (user_id, state),
        )
        cur.close()
        conn.close()

    def get_user_state(self, user_id):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT current_state FROM user_states WHERE user_id=%s", (user_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return row[0] if row else None

    # def save_user_friend(self, user_id, friend):
    #     conn = self._get_conn()
    #     cur = conn.cursor()
    #     cur.execute(
    #         """
    #         INSERT INTO user_friends (user_id, friend, friend_state)
    #         VALUES (%s, %s, %s)
    #     """,
    #         (user_id, friend, 0),
    #     )
    #     cur.close()
    #     conn.close()
    
    def clear_user_data(self, user_id):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM user_states WHERE user_id=%s", (user_id,))
        cur.execute("DELETE FROM users WHERE user_id=%s", (user_id,))
        cur.close()
        conn.close()

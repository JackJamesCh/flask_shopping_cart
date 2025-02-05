import sqlite3
from model.User import User

class UserDao:
    def __init__(self, db_name="database.db"):
        self.db_name = db_name
        self._create_table()

    def _connect(self):
        """Establish a database connection."""
        return sqlite3.connect(self.db_name)

    def _create_table(self):
        """Ensure the 'products' table exists."""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users
            (
                email    TEXT    not null
                    constraint email
                        primary key,
                password TEXT    not null,
                is_admin BOOLEAN not null
            )
        ''')
        conn.commit()
        conn.close()

    def insert_user(self, user):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (email, password, is_admin)
            VALUES (?, ?, ?)
        ''', (user.email, user.password, user.is_admin))
        conn.commit()
        conn.close()

    def get_all_users(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        conn.close()
        return [User(email=row[0], password=row[1], is_admin=bool(row[2])).to_dict() for row in rows]

    def get_all_admins(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE is_admin = 1")
        rows = cursor.fetchall()
        conn.close()
        return [User(email=row[0], password=row[1], is_admin=bool(row[2])).to_dict() for row in rows]

    def get_user_by_email_password(self, email, password):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password,))
        row = cursor.fetchone()
        conn.close()
        return User(email=row[0], password=row[1], is_admin=bool(row[2])).to_dict() if row else None
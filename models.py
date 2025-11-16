import pymysql
from config import Config

def get_db_connection():
    return pymysql.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        db=Config.MYSQL_DB,
        cursorclass=pymysql.cursors.DictCursor
    )

class User:
    @staticmethod
    def create(email, password):
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
        conn.commit()
        conn.close()

    @staticmethod
    def find_by_email(email):
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
        conn.close()
        return user

class OTP:
    @staticmethod
    def create(email, otp, expires_at):
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO otps (email, otp, expires_at) VALUES (%s, %s, %s)", (email, otp, expires_at))
        conn.commit()
        conn.close()

    @staticmethod
    def find_by_email_and_otp(email, otp):
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM otps WHERE email = %s AND otp = %s AND expires_at > NOW()", (email, otp))
            otp_record = cursor.fetchone()
        conn.close()
        return otp_record

    @staticmethod
    def delete_by_email(email):
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM otps WHERE email = %s", (email,))
        conn.commit()
        conn.close()
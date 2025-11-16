import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'  # Replace with your MySQL username
    MYSQL_PASSWORD = 'ilyas'  # Replace with your MySQL password
    MYSQL_DB = '2fa_db'
    
    # Email configuration (use Gmail SMTP)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'authotp2fa@gmail.com'  # Replace with your Gmail
    MAIL_PASSWORD = 'trkv udqf qofn ecrt'     # Use app password if 2FA enabled
    MAIL_DEFAULT_SENDER = 'no-reply@yourapp.com'  # No-reply sender
from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from flask_mail import Mail, Message
import bcrypt
import random
import string
from datetime import datetime, timedelta
from models import User, OTP
from config import Config

routes = Blueprint('routes', __name__)
mail = Mail()

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

@routes.route('/')
def home():
    return redirect(url_for('routes.login'))

@routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if User.find_by_email(email):
            flash('Email already registered. Please use a different email.', 'error')
            return redirect(url_for('routes.register'))
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        User.create(email, hashed_password.decode('utf-8'))
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('routes.login'))
    
    return render_template('register.html')

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.find_by_email(email)
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            # Generate OTP
            otp = generate_otp()
            expires_at = datetime.now() + timedelta(minutes=5)  # OTP expires in 5 minutes
            OTP.create(email, otp, expires_at)
            
            # Send OTP email
            msg = Message('Your OTP Code', sender=Config.MAIL_DEFAULT_SENDER, recipients=[email])
            msg.body = f'Your one-time password is: {otp}. It expires in 5 minutes.'
            mail.send(msg)
            
            session['email'] = email  # Store email in session for OTP verification
            flash('OTP sent to your email. Please verify.', 'info')
            return redirect(url_for('routes.verify_otp'))
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('login.html')

@routes.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if 'email' not in session:
        return redirect(url_for('routes.login'))
    
    if request.method == 'POST':
        otp = request.form['otp']
        email = session['email']
        
        otp_record = OTP.find_by_email_and_otp(email, otp)
        if otp_record:
            OTP.delete_by_email(email)  # Clean up OTP
            session.pop('email', None)
            session['logged_in'] = True
            session['user_email'] = email
            return redirect(url_for('routes.dashboard'))
        else:
            flash('Invalid or expired OTP.', 'error')
    
    return render_template('otp_verify.html')

@routes.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('routes.login'))
    return render_template('dashboard.html')

@routes.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('routes.login'))
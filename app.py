from flask import Flask
from flask_session import Session
from flask_mail import Mail
from config import Config
from routes import routes, mail
import os

app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-secret-key-change-me')
app.config['SESSION_TYPE'] = 'filesystem' 
Session(app)

mail.init_app(app)
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, logout_user, login_required, UserMixin
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///webeval.db'
app.config['SECRET_KEY'] = 'secretkey'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


if (__name__ == '__main__'):
    # db.create_all()
    app.run(port=8000, debug=True)

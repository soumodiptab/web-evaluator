from flask import Flask, render_template, redirect, url_for, jsonify, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
import json
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost/eval'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class Admin(UserMixin, db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(150), default='', nullable=False)
    def __init__(self, username, password):
        self.username = username
        self.password = password


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), default='', unique=True)
    firstname = db.Column(db.String(50), default='', nullable=False)
    lastname = db.Column(db.String(50), default='', nullable=False)
    password = db.Column(db.String(150), default='', nullable=False)
    isadmin = db.Column(db.Boolean, default=False, nullable=False)
    events = db.relationship('Event', backref='user')


class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    url = db.Column(db.String(255))
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    mouse_clicks = db.Column(db.String(100))
    heat_map = db.Column(db.String(200))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginForm(FlaskForm):
    username = StringField('User Name', validators=[
        InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember Me')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('User Name', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    firstname = StringField('First Name', validators=[
        InputRequired(), Length(min=4, max=15)])
    lastname = StringField('Last Name', validators=[
        InputRequired(), Length(min=4, max=15)])
    # admin = BooleanField('Tick if you are admin')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                # return redirect(url_for('dashboard'))
                if user.isadmin == True:
                    return redirect(url_for('dashboard_admin'))
                else:
                    return redirect(url_for('dashboard'))
            else:
                print("password mismatch!")
        # return str(user.username) + " " + str(user.password) + " " + str(form.username.data) + " " + str(form.password.data)

        return '<h1>Invalid username or password</h1>'
        # return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        print(hashed_password)
        # new_user = User(username=form.username.data, email=form.email.data, 
        #                 firstname=form.firstname.data, lastname=form.lastname.data, 
        #                 password=hashed_password, isadmin=form.admin.data)
        new_user = User(username=form.username.data, email=form.email.data,
                        firstname=form.firstname.data, lastname=form.lastname.data,
                        password=hashed_password, isadmin=False)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
        # return '<h1>New user has been created!</h1>'
        # return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)


@app.route('/dashboard_admin')
@login_required
def dashboard_admin():
    return render_template('dashboard_admin.html', name=current_user.username)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/observer/users/query', methods=['GET'])
def users_fetch():
    users = User.query.all()
    userlist = []
    for user in users:
        userlist.append({'id': user.id, 'username': user.username})
    return jsonify({'users': userlist})


@app.route('/observer/event/remove', methods=['POST'])
def remove_event():
    id = int(request.form['id'])
    event = Event.query.filter_by(id=id).first()
    db.session.delete(event)
    db.session.commit()
    return jsonify({'id': id})


@app.route('/observer/event/update', methods=['POST'])
def update_events():
    id = request.form['id']
    event = Event.query.filter_by(id=id).first()
    event.start = datetime.strptime(request.form['start'], '%d/%m/%y %H:%M')
    event.end = datetime.strptime(request.form['end'], '%d/%m/%y %H:%M')
    db.session.commit()
    return jsonify('Event has been updated')


@app.route('/observer/event/entry', methods=['POST'])
def event_entry():
    title = request.form['title']
    start = datetime.strptime(request.form['start'], '%d/%m/%y %H:%M')
    end = datetime.strptime(request.form['end'], '%d/%m/%y %H:%M')
    userid = request.form['userid']
    event = Event(test_name=title, user_id=userid, start=start, end=end, status='NOTCOMPLETED')
    db.session.add(event)
    db.session.commit()
    return jsonify({'id': event.id, 'title': event.test_name, 'start': event.start, 'end': event.end,
                    'username': event.user.username, 'status': event.status})


@app.route('/observer/event/calendar', methods=['GET'])
def view_events():
    events = Event.query.all()
    calendar_populate = []
    for event in events:
        if event.status == 'COMPLETED':
            color = 'green'
        else:
            color = 'blue'
        new_event = {
            'id': event.id, 'title': event.test_name, 'start': event.start, 'end': event.end,
            'username': event.user.username, 'url': event.url, 'backgroundColor': color, 'status': event.status
        }
        calendar_populate.append(new_event)
    return render_template('calender.html', events=calendar_populate)


def database_init():
    db.drop_all()
    db.create_all()
    # adding a static admin account at the beginning of the program
    hashed_password = generate_password_hash("admin@123", method='sha256')
    obj = User(username="admin", email='', firstname='', lastname='', password=hashed_password, isadmin=True)
    db.session.add(obj)
    db.session.commit()

    obj = Admin(username="admin", password=hashed_password)
    db.session.add(obj)
    db.session.commit()
    # adding a static user account at the beginning of the program
    hashed_password = generate_password_hash(
        "test@123", method='sha256')
    obj = User(username="user", email='user@gmail.com',
               firstname='User', lastname='User', password=hashed_password, isadmin=False)
    db.session.add(obj)
    db.session.commit()


if __name__ == '__main__':
    database_init()
    app.run(port=8000, debug=True, use_debugger=False, use_reloader=False, passthrough_errors=True)

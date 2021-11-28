from flask import Flask, flash, render_template, redirect, url_for, jsonify, request
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
from util.send_gmail_utiltity import *

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] ="mysql+mysqlconnector://root:password@localhost/eval"
#app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:mYSQLSERVER@localhost:3306/testdb"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/login'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost:8080/eval'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'




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


class Coordinates(UserMixin, db.Model):
    coordinate_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, db.ForeignKey('event.id'))
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)


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
                flash("Password Mismatch!")
                return render_template('login.html', form=form)
        # return str(user.username) + " " + str(user.password) + " " + str(form.username.data) + " " + str(form.password.data)
        flash("User does not exist!!")
        return render_template('login.html', form=form)
        # return '<h1>Invalid username or password</h1>'
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

        return redirect(url_for('index'))
        # return '<h1>New user has been created!</h1>'
        # return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    current_datetime = datetime.now()
    # eligible_events= Event.query.filter_by(user_id=current_user.id, status='NOTCOMPLETED')
    eligible_events= Event.query.filter(Event.start <= current_datetime, Event.end >= current_datetime, Event.user_id==current_user.id, Event.status=='NOTCOMPLETED')
    return render_template('dashboard.html', name=current_user.username,event_data=eligible_events)


@app.route('/user/take_test/')
@login_required
def start_test():
    print(request.args.get('id'))
    return render_template('Test.html', id=request.args.get('id'),is_admin=False)

@app.route('/admin/view_test/')
@login_required
def view_test():
    print(request.args.get('id'))
    data = Coordinates.query.filter_by(id=request.args.get('id'))
    returnVal = []
    for i in data:
        returnVal.append(i.x)
        returnVal.append(i.y)
    print(returnVal)
    return render_template('Test.html',is_admin=True,coordinates=returnVal)



@app.route('/user/addcoordinates',methods=['POST'])
@login_required
def add_coordinates():
    coordinates_posted_by_user = request.get_json()
    for i in coordinates_posted_by_user['data']:
        new_coordinates = Coordinates(id=coordinates_posted_by_user['id'],x=i['x'],y=i['y'])
        db.session.add(new_coordinates)
    
    corresponding_event = Event.query.filter_by(id=coordinates_posted_by_user['id']).first()

    corresponding_event.status = 'COMPLETED'
    corresponding_event.mouse_clicks = len(coordinates_posted_by_user['data'])
    
    db.session.commit()
    return 'success'



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
    users = User.query.filter_by(isadmin = False)
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


@app.route('/sendemail/<event_id>')
def sendEventEmail(event_id):
    event = Event.query.filter_by(id=event_id).first()
    if(event is not None):
        user_id = event.user_id
        if(user_id is not None):
            user = User.query.filter_by(id=user_id).first()
        sendEmail(str(event.test_name), str(user.email), str(event.start), str(event.end), str(event.url))
        return "Successfully sent email"
    return "Event retrieval failed"


@app.route('/eventInvite')
def eventInvite():
    events = Event.query.filter_by(status='NOTCOMPLETED')
    return render_template('send_email.html', events=events)


@app.route('/eventDashboard')
def eventDashboard():
    events = Event.query.filter_by(status='COMPLETED')
    return render_template('event_dashboard.html', events=events,)


# pip install --upgrade 'SQLAlchemy<1.4'
def database_init():
    db.drop_all()
    db.create_all()
    # adding a static admin account at the beginning of the program
    hashed_password = generate_password_hash("admin@123", method='sha256')
    obj = User(username="admin", email='', firstname='', lastname='', password=hashed_password, isadmin=True)
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

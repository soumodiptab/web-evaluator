from flask import Flask, request, render_template ,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import json

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost/eval'
app.config['SECRET_KEY'] = 'secretkey'

db = SQLAlchemy(app)


class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    url = db.Column(db.String(255))
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False)



class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), default='', unique=True)
    firstname = db.Column(db.String(50), default='', nullable=False)
    lastname = db.Column(db.String(50), default='', nullable=False)
    password = db.Column(db.String(150),  default='', nullable=False)
    isadmin = db.Column(db.Boolean, default=False, nullable=False)
    events =db.relationship('Event', backref='user')

    def __init__(self, username, email, firstname, lastname, password, isadmin):
        self.username = username
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.isadmin = isadmin

@app.route('/observer/users/query',methods=['GET'])
def users_fetch():
    users=User.query.all()
    userlist=[]
    for user in users:
        userlist.append({'id':user.id, 'username':user.username})
    return jsonify({'users':userlist})

@app.route('/observer/event/remove',methods=['POST'])
def remove_event():
    id = int(request.form['id'])
    event=Event.query.filter_by(id=id).first()
    db.session.delete(event)
    db.session.commit()
    return jsonify({'id':id})

@app.route('/observer/event/update',methods=['POST'])
def update_events():
    id=request.form['id']
    event=Event.query.filter_by(id=id).first()
    event.title=request.form['title']
    event.start=datetime.strptime(request.form['start'], '%d/%m/%y %H:%M')
    event.end=datetime.strptime(request.form['end'], '%d/%m/%y %H:%M')
    db.session.commit()
    return jsonify('Event has been updated')



@app.route('/observer/event/entry',methods=['POST'])
def event_entry():
    title = request.form['title']
    start = datetime.strptime(request.form['start'], '%d/%m/%y %H:%M')
    end = datetime.strptime(request.form['end'], '%d/%m/%y %H:%M')
    event=Event(title=title,start=start,end=end,status='NOTCOMPLETED')
    db.session.add(event)
    db.session.commit()
    return jsonify({'id':event.id,'title': event.title, 'start': event.start, 'end': event.end})

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
            'id':event.id,'title': event.title, 'start': event.start, 'end': event.end, 'backgroundColor': color
        }
        calendar_populate.append(new_event)
    return render_template('calender.html', events=calendar_populate)


if (__name__ == '__main__'):
    app.run(port=8000, debug=True, use_debugger=False, use_reloader=False, passthrough_errors=True)

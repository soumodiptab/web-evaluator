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
    url = db.Column(db.String(255))
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False)


class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)


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
    event.start=datetime.strptime(request.form['start'], '%d/%m/%y %H:%M:%S')
    event.end=datetime.strptime(request.form['end'], '%d/%m/%y %H:%M:%S')
    db.session.commit()
    return jsonify('Event has been updated')



@app.route('/observer/event/entry',methods=['POST'])
def event_entry():
    title = request.form['title']
    start = datetime.strptime(request.form['start'], '%d/%m/%y %H:%M:%S')
    end = datetime.strptime(request.form['end'], '%d/%m/%y %H:%M:%S')
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

<<<<<<< HEAD
import json
from sqlalchemy import DateTime
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from util.send_gmail_utiltity import sendEmail

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SECRET_KEY'] = 'secretkey'
db = SQLAlchemy(app)


class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)


class Events(db.Model):
    test_id = db.Column(db.Integer, primary_key=True, nullable=False)
    test_name = db.Column(db.String(100))
    date = db.Column(db.String(10))
    mouse_clicks = db.Column(db.String(100))
    heat_map = db.Column(db.String(200))
    event_url = db.Column(db.String(200))

    def __init__(self, test_name, date, mouse_clicks, heat_map, event_url):
        self.test_name = test_name
        self.date = date
        self.mouse_clicks = mouse_clicks
        self.heat_map = heat_map
        self.event_url = event_url


@app.route('/sendemail/<event_id>')
def sendEventEmail(event_id):
    event = Events.query.filter_by(test_id=event_id).first()
    if(event is not None):
        subject = "Invite sent for event " + event.test_name
        to_users = ['arshad4000@gmail.com']
        sendEmail(subject, to_users)
        return "Successfully sent email"
    return "Event retrieval failed"


@app.route('/eventInvite')
def eventInvite():
    events = Events.query.all()
    return render_template('send_email.html', events=events)

@app.route('/eventDashboard')
def eventDashboard():
    events = Events.query.all()
    return render_template('event_dashboard.html', events=events)


@app.route('/createEvent', methods=['POST'])
def createEvent():
    if(request.method == 'POST'):
        data = request.get_json()
        test_name = data['test_name']
        date = data['date']
        mouse_clicks = data['mouse_clicks']
        heat_map = data['heat_map']
        event_url = data['event_url']
        event = Events(test_name, date, mouse_clicks, heat_map, event_url)
        db.session.add(event)
        db.session.commit()
    return "Event created successfully", 200


@app.route('/getEvents', methods=['GET'])
def getEvents():
    response = []
    events = Events.query.all()
    for e in events:
        row = dict()
        row['test_id'] = e.test_id
        row['test_name'] = e.test_name
        row['date'] = e.date
        row['mouse_clicks'] = e.mouse_clicks
        row['heat_map'] = e.heat_map
        row['event_url'] = e.event_url
        response.append(row)
    return json.dumps(response)


def initializeDB():
    e1 = Events("test1", "10-10-2021", "click1", "heat1", "https://www.google.com")
    db.session.add(e1)
    e2 = Events("test2", "10-10-2021", "click2", "heat2", "https://www.google.com")
    db.session.add(e2)
    e3 = Events("test3", "10-10-2021", "click3", "heat3", "https://www.google.com")
    db.session.add(e3)
    db.session.commit()
    return


if(__name__ == '__main__'):
    db.create_all()
    # initializeDB()
    app.run(port=8000, debug=True)

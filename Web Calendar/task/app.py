import datetime

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, inputs
from marshmallow import Schema, fields
import sys

app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
parser = reqparse.RequestParser()

parser.add_argument(
    'event',
    type=str,
    help="The event name is required!",
    required=True
)

parser.add_argument(
    'date',
    type=inputs.date,
    help="The event date with the correct format is required! The correct format is YYYY-MM-DD!",
    required=True
)

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(), nullable=False)
    date = db.Column(db.Date, nullable=False)

class EventSchema(Schema):
    id = fields.Integer()
    event = fields.String()
    date = fields.Date()

class AllEventsGet(Resource):
    def get(self):
        event_list = Event.query.all()
        schema = EventSchema(many=True)
        return schema.dump(event_list)

class TodayEventsGet(Resource):
    def get(self):
        today = datetime.date.today()
        event_list = Event.query.filter(Event.date == today)
        schema = EventSchema(many=True)
        return schema.dump(event_list)

class TodayEventPost(Resource):
    def post(self):
        args = parser.parse_args()
        res = {
            "message": "The event has been added!",
            "event": args['event'],
            "date": str(args['date'].date())
        }
        ev = Event(event=args["event"], date=args['date'].date())
        db.session.add(ev)
        db.session.commit()
        return res

db.create_all()

api.add_resource(TodayEventsGet, '/event/today')
api.add_resource(AllEventsGet, '/', '/event')
api.add_resource(TodayEventPost, '/event')

# do not change the way you run the program
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()

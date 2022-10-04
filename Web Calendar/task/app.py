from flask import Flask
from flask_restful import Resource, Api, reqparse, inputs
import sys

app = Flask(__name__)
api = Api(app)

# write your code here
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

class TodayEventGet(Resource):
    def get(self):
        return {'data': 'There are no events for today!'}

class TodayEventPost(Resource):
    def post(self):
        args = parser.parse_args()
        response = {
            "message": "The event has been added!",
            "event": args['event'],
            "date": str(args['date'].date())
        }
        return response

api.add_resource(TodayEventGet, '/', '/event/today')
api.add_resource(TodayEventPost, '/event')

# do not change the way you run the program
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run(debug=True)

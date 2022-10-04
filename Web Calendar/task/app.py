from flask import Flask
from flask_restful import Resource, Api
import sys

app = Flask(__name__)
api = Api(app)

# write your code here
class TodayEvent(Resource):
    def get(self):
        return {'data': 'There are no events for today!'}

api.add_resource(TodayEvent, '/', '/event/today')

# do not change the way you run the program
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run(debug=True)
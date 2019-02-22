import markdown
import api
import os

# Import the framework
from flask import Flask

# Create an instance of Flask
app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("devices.db")
    return db

@app.route("/")
def index():
    """present some documentation """

    #Open the README file
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:

            # Read the content of the file
            content = markdown_file.read()

            # Convertn to HTML
            return markdown.markdown(content)

class DeviceList(Resources):
    def get(self):
            shelf = get_db()
            keys = list(shelf.keys())

            devices = []

            for key in keys:
                    devices.append(shelf[key])
            
            return {'message': 'success', 'data': devices}

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('identifier', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('device_type', required=True)
        parser.add_argument('controller_gateway', required=True)

        # parse the arguments into an object
        args = parser.parse_args()

        shelf = get_db()
        shelf[args['identifier']] = args

    return {'message': 'Device registered', 'data': args}, 201

class Device(Resource):
    def get(self, identifier):
        shelf = get_db()

        # If the key does not exist in the data store, return a 404 error
        if not (identifier in shelf):
            return {'message': 'Device not found', 'data0': {}}, 404
        
        return {'message': 'Device found', 'data': shelf[identifier]}, 200

    def delete(self, identifier):
        shelf = get_db()

        # If the key does not exist in the data store, return a 404 error
        if not (identifier in shelf):
            return {'message': 'Device not found', 'data0': {}}, 404
        
        del shelf[identifier]
        return '', 204

api.add_resource(DeviceList, '/devices')
api.add_resource(Device, '/device/<string:identifier>')
api.add_resource(DeviceList, '/devices')
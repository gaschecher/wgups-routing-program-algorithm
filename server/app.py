from flask import Flask
from flask_cors import CORS
from api.routes import api
from src.main import package_hash, trucks, initialize_data

app = Flask(__name__)
CORS(app)

initialize_data()

api.package_hash = package_hash
api.trucks = trucks

app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
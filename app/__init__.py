from flask import Flask
from .routes.devices_routes import device_blueprint
from .routes.phone_tracker import phone_blueprint

def create_app():
    app = Flask(__name__)
    app.register_blueprint(phone_blueprint, url_prefix='/api')
    app.register_blueprint(device_blueprint, url_prefix='/api/devices')
    return app

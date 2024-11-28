from flask import Blueprint
import app.db.service.device_service as device_service

device_blueprint = Blueprint('/device', __name__)

@device_blueprint.route('/bluetooth', methods=['GET'])
def get_devices_by_bluetooth():
    devices = device_service.find_devices_by_bluetooth_connection()
    return {"devices": devices}, 200

@device_blueprint.route('/signal', methods=['GET'])
def get_devices_by_signal():
    devices = device_service.find_devices_with_strong_signal_strength()
    return {"devices": devices}, 200

@device_blueprint.route('/count/<device_id>', methods=['GET'])
def get_device_count(device_id):
    count = device_service.count_connections(device_id)
    return {"count": count}, 200

@device_blueprint.route('/direct/<device_id1>/<device_id2>', methods=['GET'])
def get_direct_connection(device_id1, device_id2):
    connection = device_service.direct_connection(device_id1, device_id2)
    return {"connection": connection}, 200

@device_blueprint.route('/most_recent/<device_id>', methods=['GET'])
def get_most_recent_interaction(device_id):
    interaction = device_service.fetch_most_recent_interaction(device_id)
    return {"interaction": interaction}, 200
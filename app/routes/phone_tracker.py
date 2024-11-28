from flask import Blueprint, request
import app.db.service.device_service as device_service
from app.db.utils.convert_utils import convert_from_dict_to_models

phone_blueprint = Blueprint('phone_tracker', __name__)

@phone_blueprint.route("/phone_tracker", methods=['POST'])
def get_interaction():
    data = request.get_json()
    device1, device2, interaction = convert_from_dict_to_models(data)
    if device1.id == device2.id:
        return {"message": "Devices are the same"}, 400
    results = device_service.create_interaction_between_devices(device1, device2, interaction)
    print(results)
    return {"message": "Success"}, 200

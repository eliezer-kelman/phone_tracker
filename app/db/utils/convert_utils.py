from typing import Dict

from returns.maybe import Maybe

from app.db.models.device import Device
from app.db.models.interaction import Interaction
from app.db.models.location import Location


def convert_from_dict_to_models(message):

    device1_data = message['devices'][0]
    device2_data = message['devices'][1]
    interaction_data = message['interaction']

    device1 = Device(
        id=device1_data['id'],
        brand=device1_data['brand'],
        model=device1_data['model'],
        os=device1_data['os'],
        location=Location(
            latitude=device1_data['location']['latitude'],
            longitude=device1_data['location']['longitude'],
            altitude_meters=device1_data['location']['altitude_meters'],
            accuracy_meters=device1_data['location']['accuracy_meters']
        )
    )

    device2 = Device(
        id=device2_data['id'],
        brand=device2_data['brand'],
        model=device2_data['model'],
        os=device2_data['os'],
        location=Location(
            latitude=device2_data['location']['latitude'],
            longitude=device2_data['location']['longitude'],
            altitude_meters=device2_data['location']['altitude_meters'],
            accuracy_meters=device2_data['location']['accuracy_meters']
        )
    )

    interaction = Interaction(
        from_device=interaction_data['from_device'],
        to_device=interaction_data['to_device'],
        method=interaction_data['method'],
        bluetooth_version=interaction_data['bluetooth_version'],
        signal_strength_dbm=interaction_data['signal_strength_dbm'],
        distance_meters=interaction_data['distance_meters'],
        duration_seconds=interaction_data['duration_seconds'],
        timestamp=interaction_data['timestamp']
    )

    return device1, device2, interaction


def create_device_from_data(device_data: Dict) -> Maybe[Device]:

    location = Location(
        latitude=device_data['latitude'],
        longitude=device_data['longitude'],
        altitude_meters=device_data['altitude'],
        accuracy_meters=device_data['accuracy']
    )

    device = Device(
        id=device_data['id'],
        brand=device_data['brand'],
        model=device_data['model'],
        os=device_data['os'],
        location=location
    )

    return Maybe.from_value(device)

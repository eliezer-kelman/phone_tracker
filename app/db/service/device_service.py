from returns.maybe import Maybe
import app.db.repository.device_repository as device_repository
from app.db.models.device import Device
from app.db.models.interaction import Interaction


def create_device_if_not_exist(device: Device) -> Maybe[Device]:
    maybe_device = device_repository.find_device_by_id(device.id)
    if maybe_device.value_or(None):
        return maybe_device
    return device_repository.create_device(device)

def create_interaction_if_not_exist(device1: Device, device2: Device, interaction: Interaction):
    if not device_repository.interaction_exists(device1, device2, interaction):
        return device_repository.create_interaction(interaction)
    else:
        print("Interaction already exists.")
        return None


def create_interaction_between_devices(device1: Device, device2: Device, interaction: Interaction):
    create_device_if_not_exist(device1)
    create_device_if_not_exist(device2)
    return create_interaction_if_not_exist(device1, device2, interaction)


def find_devices_by_bluetooth_connection():
    return device_repository.find_devices_by_bluetooth()


def find_devices_with_strong_signal_strength():
    return device_repository.find_devices_with_strong_signal()


def count_connections(device_id: str):
    return device_repository.count_connections(device_id)


def direct_connection(device_id1: str, device_id2: str):
    return device_repository.direct_connection(device_id1, device_id2)


def fetch_most_recent_interaction(device_id: str):
    return device_repository.fetch_most_recent_interaction(device_id)

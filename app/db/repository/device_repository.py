from typing import Dict
from returns.maybe import Maybe
from app.db.database import driver
from app.db.models.device import Device
from app.db.models.interaction import Interaction
import toolz as tz
import app.db.utils.convert_utils as convert_utils
from app.db.models.location import Location


def create_device(device: Device) -> Maybe[Device]:
    with driver.session() as session:
        query = """
                    CREATE (d:Device {
                        id: $id, 
                        brand: $brand, 
                        model: $model, 
                        os: $os, 
                        latitude: $latitude, 
                        longitude: $longitude, 
                        altitude_meters: $altitude_meters, 
                        accuracy_meters: $accuracy_meters
                    })
                    RETURN d
                    """
        parameters = {
            "id": device.id,
            "brand": device.brand,
            "model": device.model,
            "os": device.os,
            "latitude": device.location.latitude,
            "longitude": device.location.longitude,
            "altitude_meters": device.location.altitude_meters,
            "accuracy_meters": device.location.accuracy_meters
        }
        result = session.run(query, parameters).single()
        return convert_utils.create_device_from_data(result.get('d'))


def create_interaction(interaction: Interaction):
    with driver.session() as session:
        query = """
        MATCH (a:Device {id: $from_device_id}), (b:Device {id: $to_device_id})
        CREATE (a)-[r:INTERACTED_WITH {
            method: $method,
            bluetooth_version: $bluetooth_version,
            signal_strength: $signal_strength,
            distance: $distance,
            duration: $duration,
            timestamp: $timestamp
        }]->(b)
        RETURN a, r, b
        """
        parameters = {
            "from_device_id": interaction.from_device,
            "to_device_id": interaction.to_device,
            "method": interaction.method,
            "bluetooth_version": interaction.bluetooth_version,
            "signal_strength": interaction.signal_strength_dbm,
            "distance": interaction.distance_meters,
            "duration": interaction.duration_seconds,
            "timestamp": interaction.timestamp
        }
        result = session.run(query, parameters).data()
        return tz.pipe(
            result,
            tz.partial(tz.pluck, 'r'),
            list
        )


def find_device_by_id(device_id: str) -> Maybe[Device]:
    with driver.session() as session:
        query = """
        MATCH (d:Device {id: $id})
        RETURN d
        """
        parameters = {"id": device_id}
        result = session.run(query, parameters).single()
        if result is None or result.get('d') is None:
            return Maybe.from_value(None)
        return convert_utils.create_device_from_data(result.get('d'))


def interaction_exists(device1: Device, device2: Device, interaction: Interaction) -> bool:
    with driver.session() as session:
        query = """
        MATCH (a:Device {id: $from_device_id})-[r:INTERACTED_WITH {
            method: $method,
            bluetooth_version: $bluetooth_version,
            signal_strength: $signal_strength,
            distance: $distance,
            duration: $duration,
            timestamp: $timestamp
        }]->(b:Device {id: $to_device_id})
        RETURN r
        """
        parameters = {
            "from_device_id": device1.id,
            "to_device_id": device2.id,
            "method": interaction.method,
            "bluetooth_version": interaction.bluetooth_version,
            "signal_strength": interaction.signal_strength_dbm,
            "distance": interaction.distance_meters,
            "duration": interaction.duration_seconds,
            "timestamp": interaction.timestamp
        }
        result = session.run(query, parameters).data()
        return len(result) > 0


def find_devices_by_bluetooth() -> list[Dict]:
    with driver.session() as session:
        query = """
            MATCH (start:Device)
            MATCH (end:Device)
            WHERE start <> end
            MATCH path = shortestPath((start)-[:INTERACTED_WITH*]->(end))
            WHERE ALL(r IN relationships(path) WHERE r.method = 'Bluetooth')
            WITH path, length(path) as pathLength
            ORDER BY pathLength DESC
            LIMIT 1
            RETURN path
        """
        result = session.run(query).data()
        return result


def find_devices_with_strong_signal() -> list[Dict]:
    with driver.session() as session:
        query = """
            MATCH (d1:Device)-[r:INTERACTED_WITH]->(d2:Device)
            WHERE r.signal_strength > -60
            RETURN d1.id AS device1_id, d2.id AS device2_id, r.signal_strength AS signal_strength
        """
        result = session.run(query).data()
        return result


def count_connections(device_id: str) -> int:
    with driver.session() as session:
        query = """
            MATCH (d1:Device {id: $device_id})-[r:INTERACTED_WITH]->(d2:Device)
            RETURN count(r) AS connections
        """
        parameters = {"device_id": device_id}
        result = session.run(query, parameters).single()
        return result.get('connections')


def direct_connection(device_id_1: str, device_id_2: str) -> bool:
    with driver.session() as session:
        query = """
            MATCH (d1:Device {id: $device_id_1})-[r:INTERACTED_WITH]->(d2:Device {id: $device_id_2})
            RETURN r
        """
        parameters = {"device_id_1": device_id_1, "device_id_2": device_id_2}
        result = session.run(query, parameters).data()
        return len(result) > 0

def fetch_most_recent_interaction(device_id: str) -> list[Dict]:
    with driver.session() as session:
        query = """
            MATCH (d:Device {id: $device_id})-[r:INTERACTED_WITH]->(other:Device)
            RETURN other.id AS interacted_device, r.timestamp AS timestamp
            ORDER BY r.timestamp DESC
        """
        parameters = {"device_id": device_id}
        result = session.run(query, parameters).data()
        return result
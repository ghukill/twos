from lib import ltr390
from sensor import SensorValue

from utils import get_i2c


class Light:
    def __init__(self):
        i2c = get_i2c()
        self.ltr = ltr390.LTR390(i2c)

    def get_als(self) -> int:
        """ambient light"""
        return self.ltr.lux

    def get_uvi(self) -> int:
        """UV Index"""
        return self.ltr.uvi

    def get_als_str(self) -> str:
        """ambient light"""
        return f"{int(self.ltr.lux)} lum"

    def get_uvi_str(self) -> str:
        """UV Index"""
        return str(self.ltr.uvi)

    def get_sensor_values(self) -> list:
        """Return list of SensorValue instances"""
        return [
            SensorValue("Amb", int(self.ltr.lux), "lum"),
            SensorValue("UVi", self.ltr.uvi, ""),
        ]

    def ha_mqtt_discover(self, station):
        import json
        import time
        
        # Ambient light sensor
        topic = f"homeassistant/sensor/{station.config['name']}/illuminance/config"
        payload = {
            "name": "Illuminance",
            "state_topic": f"twos/{station.config['name']}/Amb",
            "unique_id": f"{station.config['name']}_illuminance",
            "device_class": "illuminance",
            "unit_of_measurement": "lx",
            "device": station.ha_device_config,
        }
        station.mqtt.publish(topic, json.dumps(payload))
        
        time.sleep(0.1)
        
        # UV Index sensor
        topic = f"homeassistant/sensor/{station.config['name']}/uv_index/config"
        payload = {
            "name": "UV Index",
            "state_topic": f"twos/{station.config['name']}/UVi",
            "unique_id": f"{station.config['name']}_uv_index",
            "unit_of_measurement": "",
            "device": station.ha_device_config,
        }
        station.mqtt.publish(topic, json.dumps(payload))

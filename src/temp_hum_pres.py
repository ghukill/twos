import json
import time

from lib.bme280_float import BME280
from sensor import SensorValue

from utils import get_i2c

I2C_ADDRESS = 119


class TempHumPres:
    def __init__(self):
        i2c = get_i2c()
        self.bme = BME280(i2c=i2c, address=I2C_ADDRESS)

    def c_to_f(self, c):
        f = (c * 9 / 5) + 32
        return f

    def get_temp_str(self):
        return "{:.2f}F".format(self.get_temp())

    def get_pressure_str(self):
        return self.bme.values[1]

    def get_humidity_str(self):
        return self.bme.values[2]

    def get_temp(self) -> float:
        """Returns fahrenheit"""
        c = self.bme.read_compensated_data()[0]
        return self.c_to_f(c)

    def get_pressure(self):
        return self.bme.read_compensated_data()[1]

    def get_humidity(self):
        return self.bme.read_compensated_data()[2]

    def get_altitude(self):
        return self.bme.altitude

    def get_dew_point(self):
        return self.bme.dew_point

    def get_sensor_values(self) -> list:
        """Return list of SensorValue instances"""
        return [
            SensorValue("Temp", round(self.get_temp(), 2), "F"),
            SensorValue("Pres", round(self.get_pressure() / 100, 2), "hPa"),
            SensorValue("Hum", round(self.get_humidity(), 2), "%"),
        ]

    # TODO: eventually, move into base Sensor class?
    def ha_mqtt_discover(self, station):
        topic = f"homeassistant/sensor/{station.config['name']}/temperature/config"
        payload = {
            "name": "Temperature",
            "state_topic": f"twos/{station.config['name']}/Temp",
            "unique_id": f"{station.config['name']}_temperature",
            "device_class": "temperature",
            "unit_of_measurement": "°F",
            "device": station.ha_device_config,
        }
        station.mqtt.publish(topic, json.dumps(payload).encode("utf-8"))

        time.sleep(0.1)

        topic = f"homeassistant/sensor/{station.config['name']}/pressure/config"
        payload = {
            "name": "Pressure",
            "state_topic": f"twos/{station.config['name']}/Pres",
            "unique_id": f"{station.config['name']}_pressure",
            "device_class": "atmospheric_pressure",
            "unit_of_measurement": "hPa",
            "device": station.ha_device_config,
        }
        station.mqtt.publish(topic, json.dumps(payload))

        time.sleep(0.1)

        topic = f"homeassistant/sensor/{station.config['name']}/humidity/config"
        payload = {
            "name": "Humidity",
            "state_topic": f"twos/{station.config['name']}/Hum",
            "unique_id": f"{station.config['name']}_humidity",
            "device_class": "humidity",
            "unit_of_measurement": "%",
            "device": station.ha_device_config,
        }
        station.mqtt.publish(topic, json.dumps(payload))

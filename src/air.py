import time

from lib import adafruit_sgp30
from sensor import SensorValue
from temp_hum_pres import TempHumPres
from utils import get_i2c


class Air:
    def __init__(self):
        i2c = get_i2c()
        self.sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)

        # Initialize temp/humidity sensor for compensation
        self.temp_hum_pres = TempHumPres()

        # Track last humidity compensation update
        self._last_humidity_update = 0
        self._humidity_update_interval = 30  # Update every 30 seconds

    def init_algo(self):
        self.sgp30.iaq_init()
        time.sleep(15)

    def _update_humidity_compensation(self):
        """Update humidity compensation if enough time has passed"""
        current_time = time.time()

        # Only update if enough time has passed since last update
        if current_time - self._last_humidity_update >= self._humidity_update_interval:
            try:
                # Get temperature in Celsius
                temp_f = self.temp_hum_pres.get_temp()
                temp_c = (temp_f - 32) * 5 / 9  # Convert F to C

                # Get humidity percentage
                humidity_percent = self.temp_hum_pres.get_humidity()

                # Set humidity compensation
                self.sgp30.set_iaq_rel_humidity(humidity_percent, temp_c)

                self._last_humidity_update = current_time

                print(
                    f"Updated SGP30 humidity compensation: {humidity_percent:.1f}% RH, {temp_c:.1f}°C"
                )

            except Exception as e:
                print(f"Warning: Could not update humidity compensation: {e}")

    def read(self) -> tuple:
        # Update humidity compensation before reading
        self._update_humidity_compensation()

        co2eq, tvoc = self.sgp30.iaq_measure()
        return co2eq, tvoc

    def get_co2eq(self):
        "CO2 concentration"
        return self.read()[0]

    def get_tvoc(self):
        "organic compounds"
        return self.read()[1]

    def get_co2eq_str(self):
        return f"{self.get_co2eq()} ppm"

    def get_tvoc_str(self):
        return f"{self.get_tvoc()} ppb"

    def get_sensor_values(self) -> list:
        """Return list of SensorValue instances"""
        return [
            SensorValue("CO2", self.get_co2eq(), "ppm"),
            SensorValue("TVOC", self.get_tvoc(), "ppb"),
        ]

    def force_humidity_update(self):
        """Force an immediate humidity compensation update"""
        self._last_humidity_update = 0
        self._update_humidity_compensation()

    def set_humidity_update_interval(self, seconds: int):
        """Set how often to update humidity compensation (in seconds)"""
        self._humidity_update_interval = seconds

    def ha_mqtt_discover(self, station):
        import json
        
        # CO2 sensor
        topic = f"homeassistant/sensor/{station.config['name']}/co2/config"
        payload = {
            "name": "CO2",
            "state_topic": f"twos/{station.config['name']}/CO2",
            "unique_id": f"{station.config['name']}_co2",
            "device_class": "carbon_dioxide",
            "unit_of_measurement": "ppm",
            "device": station.ha_device_config,
        }
        station.mqtt.publish(topic, json.dumps(payload))
        
        time.sleep(0.1)
        
        # TVOC sensor
        topic = f"homeassistant/sensor/{station.config['name']}/tvoc/config"
        payload = {
            "name": "TVOC",
            "state_topic": f"twos/{station.config['name']}/TVOC",
            "unique_id": f"{station.config['name']}_tvoc",
            "unit_of_measurement": "ppb",
            "device": station.ha_device_config,
        }
        station.mqtt.publish(topic, json.dumps(payload))
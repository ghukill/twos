import time

from air import Air
from battery import Battery
from display import Display
from light import Light
from mqtt import MQTT
from sensor import SensorValue
from storage import Storage
from temp_hum_pres import TempHumPres
from utils import time_diff_s
from wifi import WiFi

DEFAULT_STATION_CONFIG = {
    "name": "TWOS Station XYZ",
    "wifi": {
        "connect": True,
        "ssid": None,
        "password": None,
    },
    "data": {
        "local": {
            "filepath": None,
        },
        "mqtt": {
            "broker": None,
            "port": None,
        },
    },
}


class Station:
    def __init__(self):
        t0 = time.time_ns()

        # storage and config
        self.storage = Storage()
        self.config = self.load_config()

        # peripherals
        self.display = Display()
        self.battery = Battery()

        # comms
        self.mqtt = MQTT(
            f"esp32_twos_{self.config['name']}",
            self.config["data"]["mqtt"]["broker"],
            self.config["data"]["mqtt"]["port"],
        )
        self.wifi = WiFi(
            ssid=self.config["wifi"]["ssid"],
            password=self.config["wifi"]["password"],
        )

        # sensors
        self.temp_hum_pres = TempHumPres()
        self.air = Air()
        self.light = Light()

        print(f"Station loaded: {time_diff_s(t0)}s")

    def load_config(self):
        config = self.storage.read_config()
        if not config:
            config = DEFAULT_STATION_CONFIG
            self.storage.write_config(config)
        return config

    # TODO: drive from SD config
    @property
    def ha_device_config(self):
        return {
            "identifiers": [self.config["name"]],
            "name": f"TWOS Station - {self.config['name']}",
            "model": "TWOS.v1",
            "manufacturer": "HenonDesigns",
        }

    def welcome_display(self):
        self.display.screen.large_text("TWOS", x=0, y=0, m=3)
        self.display.simple_text(f'''"{self.config["name"]}"''', 4)
        self.display.simple_text(
            f"B:{self.battery.get_voltage_str()}, W:{self.wifi.is_connected_str()}", 7
        )

    def warmup(self):
        if not self.wifi.is_connected():
            self.wifi.connect()

        # TODO: consider moving to method
        for sensor in [self.temp_hum_pres, self.air, self.light]:
            sensor.ha_mqtt_discover(self)

        # Add battery to HA discovery
        self.battery.ha_mqtt_discover(self.mqtt, self)

        self.air.init_algo()

    def get_sensor_readings(self) -> list:
        """Return list of all sensor values"""
        readings = []
        readings.extend(self.temp_hum_pres.get_sensor_values())
        readings.extend(self.air.get_sensor_values())
        readings.extend(self.light.get_sensor_values())
        readings.extend(self.battery.get_sensor_values())
        return readings

    def print_sensor_readings(self, readings: list[SensorValue]):
        print("\nSensor reading: ---------------------------")
        for sv in readings:
            print(str(sv))
        print("-------------------------------------------")

    def display_sensor_readings(self, readings: list[SensorValue]):
        self.display.clear()

        readings = [reading for reading in readings if reading.name != "Battery"]

        lines = []
        for i, reading in enumerate(readings):
            lines.append((str(reading), i))

        # QUESTION: turn this into a system "sensor"?
        lines.append(
            (
                f"B:{self.battery.get_voltage_str()}, W:{self.wifi.is_connected_str()}",
                7,
            )
        )

        self.display.eight_text_lines(lines)

    def store_sensor_readings(self, readings: list[SensorValue]):
        pass

    def send_sensor_readings(self, readings: list[SensorValue]):
        for sv in readings:
            topic = f"twos/{self.config['name']}/{sv.name}"
            message = str(sv.value)
            print(f"Sending MQTT message: {topic} --> {message}")
            self.mqtt.publish(topic, message)

    def _average_sensor_readings(
        self, all_readings: list[list[SensorValue]]
    ) -> list[SensorValue]:
        """Average multiple sets of sensor readings"""
        if not all_readings:
            return []

        # Group readings by sensor name
        readings_by_name = {}
        for reading_set in all_readings:
            for sv in reading_set:
                if sv.name not in readings_by_name:
                    readings_by_name[sv.name] = []
                readings_by_name[sv.name].append(sv)

        # Calculate averages for each sensor
        averaged_readings = []
        for sensor_name, sensor_values in readings_by_name.items():
            # Get the first reading as a template
            template = sensor_values[0]

            # Calculate average value
            values = [sv.value for sv in sensor_values]
            avg_value = sum(values) / len(values)

            # Create averaged sensor reading
            averaged_sv = SensorValue(
                name=template.name, value=round(avg_value, 2), unit=template.unit
            )
            averaged_readings.append(averaged_sv)

        return averaged_readings

    def process_sensor_readings(self):
        t0 = time.time_ns()

        # Collect multiple readings over 30 seconds (6 readings, 5 seconds apart)
        all_readings = []
        num_samples = 6
        sample_interval = 5  # seconds

        print(
            f"Collecting {num_samples} sensor samples over {(num_samples - 1) * sample_interval} seconds..."
        )

        for i in range(num_samples):
            sample_readings = self.get_sensor_readings()
            all_readings.append(sample_readings)
            print(f"  Sample {i + 1}/{num_samples} collected")

            # Sleep between samples (except after the last one)
            if i < num_samples - 1:
                time.sleep(sample_interval)

        # Average the readings
        averaged_readings = self._average_sensor_readings(all_readings)

        self.print_sensor_readings(averaged_readings)
        self.display_sensor_readings(averaged_readings)
        self.store_sensor_readings(averaged_readings)
        self.send_sensor_readings(averaged_readings)
        print(f"Sensor processing elapsed: {time_diff_s(t0)}s")

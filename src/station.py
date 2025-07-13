import time

from air import Air
from battery import Battery
from display import Display
from light import Light
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
        "remote": {
            "endpoint": None,
            "username": None,
            "password": None,
        },
    },
}


class Station:
    def __init__(self):
        t0 = time.time_ns()
        self.storage = Storage()
        self.config = self.load_config()

        self.display = Display()
        self.battery = Battery()
        self.wifi = WiFi(
            ssid=self.config["wifi"]["ssid"],
            password=self.config["wifi"]["password"],
        )

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

    def welcome_display(self):
        self.display.screen.large_text("TWOS", x=0, y=0, m=3)
        self.display.simple_text(f'''"{self.config["name"]}"''', 4)
        self.display.simple_text(
            f"B:{self.battery.get_voltage_str()}, W:{self.wifi.is_connected_str()}", 7
        )

    def warmup(self):
        if not self.wifi.is_connected():
            self.wifi.connect()
        self.air.init_algo()

    def get_sensor_readings(self) -> list:
        """Return list of all sensor values"""
        readings = []
        readings.extend(self.temp_hum_pres.get_sensor_values())
        readings.extend(self.air.get_sensor_values())
        readings.extend(self.light.get_sensor_values())
        return readings

    def print_sensor_readings(self, readings: list[SensorValue]):
        print("\nSensor reading: ---------------------------")
        for sv in readings:
            print(str(sv))
        print("-------------------------------------------")

    def display_sensor_readings(self, readings: list[SensorValue]):
        self.display.clear()

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
        pass

    def process_sensor_readings(self):
        t0 = time.time_ns()
        readings = self.get_sensor_readings()
        self.print_sensor_readings(readings)
        self.display_sensor_readings(readings)
        self.store_sensor_readings(readings)
        self.send_sensor_readings(readings)
        print(f"Sensor processing elapsed: {time_diff_s(t0)}s")

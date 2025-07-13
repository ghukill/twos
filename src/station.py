import time

from air import Air
from battery import Battery
from display import Display
from light import Light
from sensor import SensorValue
from storage import Storage
from temp_hum_pres import TempHumPres
from wifi import WiFi

DEFAULT_STATION_CONFIG = {
    "name": "TWOS Station XYZ",
    "wifi": {
        "ssid": None,
        "password": None,
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
        print(f"Station loaded: {(time.time_ns() - t0) / 1_000_000_000}s")

    def load_config(self):
        config = self.storage.read_config()
        if not config:
            config = DEFAULT_STATION_CONFIG
            self.storage.write_config(config)
        return config

    def welcome_display(self):
        self.display.simple_text("Welcome to TWOS", 0)
        self.display.horizontal_line(8)
        self.display.simple_text(
            f"B:{self.battery.get_voltage_str()}, W:{self.wifi.is_connected_str()}", 7
        )

    def warmup(self):
        if not self.wifi.is_connected():
            self.wifi.connect()
        self.air.init_algo()

    def sensor_display_simple(self):
        self.display.clear()

        lines = []
        readings = self.get_sensor_readings()
        for i, reading in enumerate(readings):
            lines.append((str(reading), i))

        # TODO: turn this into a system "sensor"?
        lines.append(
            (
                f"B:{self.battery.get_voltage_str()}, W:{self.wifi.is_connected_str()}",
                7,
            )
        )

        print("\n---------------------------")
        for text, _ in lines:
            print(text)
        print("---------------------------")
        self.display.eight_text_lines(lines)

    def get_sensor_readings(self) -> list:
        """Return list of all sensor values"""
        readings = []
        readings.extend(self.temp_hum_pres.get_sensor_values())
        readings.extend(self.air.get_sensor_values())
        readings.extend(self.light.get_sensor_values())
        return readings

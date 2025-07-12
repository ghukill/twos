import time

from air import Air
from battery import Battery
from display import Display
from light import Light
from temp_hum_pres import TempHumPres
from wifi import WiFi


class Station:
    def __init__(self):
        t0 = time.time_ns()
        self.display = Display()
        self.battery = Battery()
        self.wifi = WiFi(ssid="Ruby", password="DumpsterTurkey")  # TODO: use config

        self.temp_hum_pres = TempHumPres()
        self.air = Air()
        self.light = Light()
        print(f"Station loaded: {(time.time_ns() - t0) / 1_000_000_000}s")

    def welcome_display(self):
        self.display.simple_text("Welcome to TWOS", 0)
        self.display.horizontal_line(8)
        self.display.simple_text(
            f"B:{self.battery.get_voltage_str()}, W:{self.wifi.is_connected_str()}", 7
        )

        self.display.draw_weather_icon()

    def warmup(self):
        # if not self.wifi.is_connected():
        #     self.wifi.connect()  # TODO: will need config help
        self.air.init_algo()

    def sensor_display_simple(self):
        self.display.clear()

        # BME280
        self.display.simple_text(f"Temp: {self.temp_hum_pres.get_temp_str()}", 0)
        self.display.simple_text(f"Pres: {self.temp_hum_pres.get_pressure_str()}", 1)
        self.display.simple_text(f"Hum: {self.temp_hum_pres.get_humidity_str()}", 2)

        # SGP32
        self.display.simple_text(f"CO2: {self.air.get_co2eq_str()}", 3)
        self.display.simple_text(f"TVOC: {self.air.get_tvoc_str()}", 4)

        # LTR390
        self.display.simple_text(f"AmbL: {self.light.get_als_str()}", 5)
        self.display.simple_text(f"UVi: {self.light.get_uvi_str()}", 6)

        # Operations
        self.display.simple_text(
            f"B:{self.battery.get_voltage_str()}, W:{self.wifi.is_connected_str()}", 7
        )

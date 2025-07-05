import time

from air import Air
from battery import Battery
from display import Display
from light import Light
from temp_hum_pres import TempHumPres


class Station:
    def __init__(self):
        t0 = time.time_ns()
        self.display = Display()
        self.battery = Battery()
        self.temp_hum_pres = TempHumPres()
        self.air = Air()
        self.light = Light()
        print(f"Station loaded: {(time.time_ns() - t0) / 1_000_000_000}s")

    def display_simple(self):
        # BME280
        self.display.simple_text(f"Temp: {self.temp_hum_pres.get_temp_str()}", 0)
        self.display.simple_text(f"Pres: {self.temp_hum_pres.get_pressure_str()}", 1)
        self.display.simple_text(f"Hum: {self.temp_hum_pres.get_humidity_str()}", 2)

        # SGP32
        self.display.simple_text(f"CO2: {self.air.get_co2eq_str()}", 3)
        self.display.simple_text(f"TVOC: {self.air.get_tvoc_str()}", 4)

        # LTR390
        self.display.simple_text(f"AmbL: {self.light.get_als_str()} lum", 5)
        self.display.simple_text(f"UVi: {self.light.get_uvi_str()}", 6)

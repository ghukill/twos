import time

from lib import adafruit_sgp30
from utils import get_i2c


class Air:
    def __init__(self):
        i2c = get_i2c()
        self.sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)

    def init_algo(self):
        self.sgp30.iaq_init()
        time.sleep(15)

    def read(self) -> tuple:
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

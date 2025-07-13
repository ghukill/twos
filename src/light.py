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

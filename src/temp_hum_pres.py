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
            SensorValue("Temp", self.get_temp(), "F"),
            SensorValue("Pres", self.get_pressure(), "hPa"),
            SensorValue("Hum", self.get_humidity(), "%")
        ]

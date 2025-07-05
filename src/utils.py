from machine import Pin, I2C


def get_i2c() -> I2C:
    return I2C(0, scl=Pin(22), sda=Pin(23), freq=400000)


def connect_wifi():
    pass

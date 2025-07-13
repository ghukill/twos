from machine import Pin, I2C
import time


def get_i2c() -> I2C:
    return I2C(0, scl=Pin(22), sda=Pin(23), freq=400000)


def time_diff_s(start_time):
    return (time.time_ns() - start_time) / 1_000_000_000

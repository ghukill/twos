from micropython import const
import time

_LTR390_I2CADDR_DEFAULT = const(0x53)

_MAIN_CTRL = const(0x00)
_MEAS_RATE = const(0x04)
_GAIN = const(0x05)
_PART_ID = const(0x06)
_MAIN_STATUS = const(0x07)
_ALS_DATA = const(0x0D)
_UVS_DATA = const(0x10)

_MODE_ALS = const(0x00)
_MODE_UVS = const(0x01)

_GAIN_VALUES = [1, 3, 6, 9, 18]


class LTR390:
    def __init__(self, i2c, address=_LTR390_I2CADDR_DEFAULT):
        self.i2c = i2c
        self.address = address

        part_id = self._read_byte(_PART_ID)
        if part_id != 0xB2:
            raise RuntimeError("Failed to find LTR390 - check wiring!")

        self._write_byte(_MAIN_CTRL, 0x02)  # Enable

        # Default: ALS mode, gain 3, 100ms integration
        self.set_mode(_MODE_ALS)
        self.gain = 3
        self.integration_time_ms = 100

        self._write_byte(_GAIN, 0x02)  # Gain index 2 => 3x

        self._write_byte(_MEAS_RATE, (0x03 << 3) | 0x03)  # 100ms, 25ms resolution

    def _read_byte(self, register):
        return int.from_bytes(
            self.i2c.readfrom_mem(self.address, register, 1), "little"
        )

    def _write_byte(self, register, value):
        self.i2c.writeto_mem(self.address, register, bytes([value]))

    def _read_three_bytes(self, register):
        data = self.i2c.readfrom_mem(self.address, register, 3)
        return data[0] | (data[1] << 8) | (data[2] << 16)

    def set_mode(self, mode):
        ctrl = self._read_byte(_MAIN_CTRL) & 0xFE
        self._write_byte(_MAIN_CTRL, ctrl | (mode & 0x01))
        self.mode = mode

    def data_ready(self):
        status = self._read_byte(_MAIN_STATUS)
        return (status & 0x08) != 0

    def read_raw(self):
        if self.mode == _MODE_ALS:
            return self._read_three_bytes(_ALS_DATA)
        else:
            return self._read_three_bytes(_UVS_DATA)

    @property
    def raw_lux(self):
        self.set_mode(_MODE_ALS)
        while not self.data_ready():
            time.sleep_ms(5)
        return self.read_raw()

    @property
    def raw_uvi(self):
        self.set_mode(_MODE_UVS)
        while not self.data_ready():
            time.sleep_ms(5)
        return self.read_raw()

    @property
    def lux(self):
        raw = self.raw_lux

        # Gain and integration time scaling (approximate, matches Adafruit logic)
        gain = _GAIN_VALUES[2]  # gain index 2 => 3x, adjust if needed
        int_time_ms = 100  # default: 100ms

        # Empirical lux calculation factor (based on datasheet and Adafruit)
        # This factor normalizes raw counts to approximate lux
        return raw / (gain * int_time_ms * 0.0036)

    @property
    def uvi(self):
        raw = self.raw_uvi
        # Empirical factor per Adafruit CircuitPython
        return raw / 2300.0

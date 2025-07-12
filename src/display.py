import random

from lib import sh1107
import lib.framebuf2 as framebuf

from utils import get_i2c

I2C_ADDRESS = 60
WIDTH = 128
HEIGHT = 64


class Display:
    def __init__(self):
        self.screen = self.get_screen()

    def get_screen(self):
        i2c = get_i2c()
        return sh1107.SH1107_I2C(
            WIDTH, HEIGHT, i2c, address=I2C_ADDRESS, rotate=0, external_vcc=False
        )

    def clear(self):
        self.screen.fill(0)
        self.show()

    def show(self):
        self.screen.show()

    def random_lines(self, num_lines):
        for _ in range(num_lines):
            self.screen.line(
                random.randint(0, WIDTH),
                random.randint(0, HEIGHT),
                random.randint(0, WIDTH),
                random.randint(0, HEIGHT),
                random.choice([0, 1]),
            )
            self.show()

    def simple_text(self, text, line_num: int):
        if len(text) > 16:
            print(f"WARNING: text will exceed display width, '{text}'")
        self.screen.text(
            text,
            0,
            line_num * 8,
            1,
        )
        self.show()

    def line(self, a: tuple, b: tuple):
        x1, y1 = a
        x2, y2 = b
        self.screen.line(x1, y1, x2, y2, 1)
        self.show()

    def horizontal_line(self, line_num):
        self.line((0, line_num), (128, line_num))

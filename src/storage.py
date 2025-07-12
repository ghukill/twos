from machine import Pin, SDCard
import os


class Storage:
    def __init__(self):
        self.sd = SDCard(slot=2, sck=5, miso=19, mosi=18, cs=15)
        self.vfs = os.VfsFat(self.sd)
        os.mount(self.vfs, "/sd")

    def ls(self, path):
        return os.listdir(path)

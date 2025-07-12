import json
from machine import SDCard
import os


class Storage:
    """
    breakout to ESP32 wiring:
        - CLK: 5  (SCK)
        - DO:  19 (MISO)
        - DI:  18 (MOSI)
        - CS:  15 (A8)
        - CD:  21 <-- not yet implemented
    """

    MOUNT_DIR = "/twos-sd"
    CONFIG_FILENAME = "config.json"

    def __init__(self):
        try:
            os.listdir(self.MOUNT_DIR)
            print("SD card already mounted")
        except OSError:
            self.sd = SDCard(slot=2, sck=5, miso=19, mosi=18, cs=15)
            self.vfs = os.VfsFat(self.sd)
            os.mount(self.vfs, self.MOUNT_DIR)

    def walk(self, path):
        """
        Recursively walk through a directory tree.
        Yields (dirpath, dirnames, filenames) tuples similar to os.walk()
        """
        try:
            entries = os.listdir(path)
        except OSError:
            return

        dirnames = []
        filenames = []

        for entry in entries:
            full_path = path + "/" + entry if path != "/" else "/" + entry

            try:
                stat_info = os.stat(full_path)
                if stat_info[0] & 0x4000:  # directory (mode & 0x4000)
                    dirnames.append(entry)
                else:
                    filenames.append(entry)
            except OSError:
                continue

        yield (path, dirnames, filenames)

        for dirname in dirnames:
            subdir_path = path + "/" + dirname if path != "/" else "/" + dirname
            yield from self.walk(subdir_path)

    def rmtree(self, path):
        """Recursively delete a directory tree"""
        # Collect all directories in depth-first order (deepest first)
        dirs_to_remove = []

        for dirpath, dirnames, filenames in self.walk(path):
            # Delete all files in current directory
            for filename in filenames:
                file_path = (
                    dirpath + "/" + filename if dirpath != "/" else "/" + filename
                )
                try:
                    os.remove(file_path)
                except OSError as e:
                    print(f"Error deleting file {file_path}: {e}")

            # Add directory to removal list (will be processed in reverse order)
            dirs_to_remove.append(dirpath)

        # Remove directories in reverse order (deepest first)
        for dir_path in reversed(dirs_to_remove):
            try:
                os.rmdir(dir_path)
            except OSError as e:
                print(f"Error removing directory {dir_path}: {e}")

    def write_config(self, data: dict):
        with open(f"{self.MOUNT_DIR}/{self.CONFIG_FILENAME}", "w") as f:
            f.write(json.dumps(data))
        return True

    def read_config(self) -> dict:
        if self.CONFIG_FILENAME in os.listdir(self.MOUNT_DIR):
            with open(f"{self.MOUNT_DIR}/{self.CONFIG_FILENAME}") as f:
                return json.load(f)
        return None

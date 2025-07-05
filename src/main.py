"""
main.py - TWOS Weather Station
ESP32 HUZZAH32 Feather Board Startup Script
"""

import sys
import time

from station import Station
from utils import get_i2c

i2c = get_i2c()


def console_welcome():
    """Print welcome message with some flair"""
    print("=" * 40)
    print("Welcome to TWOS, v0.1")
    print("Board: Adafruit HUZZAH32 ESP32 Feather")
    print(f"Python version: {sys.version}")
    print(f"Platform: {sys.platform}")
    print("Status: System Starting...")
    print("=" * 40)


def main():
    """Main entry point for the weather station"""
    console_welcome()

    try:
        station = Station()

        # TODO: move to station method
        station.display.simple_text("Welcome to TWOS", 0)
        station.display.horizontal_line(8)
        time.sleep(3)

        # main loop
        while True:
            station.display.clear()

            station.display_simple()

            time.sleep(5)

    except KeyboardInterrupt:
        print("\nShutdown requested by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("DEBUG MODE: entering REPL")


if __name__ == "__main__":
    main()

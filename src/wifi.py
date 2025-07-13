import network
import time


class WiFi:
    def __init__(self, ssid: str = None, password: str = None):
        """
        Initialize the WiFi class.

        If ssid and password are provided, connection can be attempted immediately with connect().
        """
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.ssid = ssid
        self.password = password
        self.connected = False
        self.ip_address = None

    def connect(self, ssid: str = None, password: str = None, max_retries: int = 5):
        """
        Connect to a Wi-Fi network.

        If ssid and password are not provided here, it uses values from __init__.

        NOTE: on successful connect, these SSID + password will get stored internally on non-volatile storage (NVS).
        Calling .disconnect() + .connect() is a way to reset them.
        """
        ssid = ssid or self.ssid
        password = password or self.password

        if not ssid or not password:
            raise ValueError("SSID and password must be provided.")

        print(f"Connecting to {ssid}...")

        self.wlan.connect(ssid, password)
        retries = 0

        while not self.wlan.isconnected() and retries < max_retries:
            time.sleep(2)
            retries += 1
            print(f"  Retry {retries}/{max_retries}...")

        if self.wlan.isconnected():
            self.connected = True
            self.ip_address = self.wlan.ifconfig()[0]
            print(f"Connected. IP address: {self.ip_address}")
        else:
            self.connected = False
            raise RuntimeError("Failed to connect to Wi-Fi.")

    def disconnect(self):
        """
        Disconnect from the Wi-Fi network.
        """
        self.wlan.disconnect()
        self.wlan.active(False)
        self.connected = False
        self.ip_address = None
        print("Disconnected from Wi-Fi.")

    def get_ip(self) -> str:
        """
        Return the current IP address, or 'None' if not connected.
        """
        if self.wlan.isconnected():
            return self.wlan.ifconfig()[0]
        return "None"

    def is_connected(self) -> bool:
        """
        Return True if connected to Wi-Fi.
        """
        return self.wlan.isconnected()

    def is_connected_str(self) -> str:
        return "y" if self.is_connected() else "n"

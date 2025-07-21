from machine import ADC, Pin
import json
from sensor import SensorValue


class Battery:
    def __init__(self):
        self.attached = False
        try:
            self.vbat_adc = ADC(Pin(35))
            self.vbat_adc.atten(ADC.ATTN_11DB)
            self.attached = True
        except Exception as exc:
            print(f"Could not load battery: {exc}")

    def get_voltage(self) -> float:
        raw = self.vbat_adc.read()
        return raw / 4095 * 3.6 * 2

    def get_voltage_str(self) -> str:
        if self.attached:
            return "{:.2f}v".format(self.get_voltage())
        return "None"

    def get_sensor_values(self) -> list:
        """Return list of SensorValue instances"""
        if not self.attached:
            return []
        return [
            SensorValue("Battery", round(self.get_voltage(), 2), "V"),
        ]

    def ha_mqtt_discover(self, mqtt_client, station):
        """Publish battery sensor discovery to Home Assistant"""
        if not self.attached:
            return

        # TODO: convert to battery + percent
        # https://claude.ai/chat/d7047966-4c7e-419d-bd16-4b719146cb59
        discovery_config = {
            "name": f"{station.config['name']} Battery",
            "state_topic": f"twos/{station.config['name']}/Battery",
            "unique_id": f"twos_{station.config['name']}_battery",
            "device_class": "voltage",
            "unit_of_measurement": "V",
            "device": station.ha_device_config,
        }

        topic = f"homeassistant/sensor/{station.config['name']}/battery/config"
        mqtt_client.publish(topic, json.dumps(discovery_config))

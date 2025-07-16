from umqtt.simple import MQTTClient


class MQTT:
    def __init__(self, client_id, mqtt_broker, mqtt_port, keepalive=60):
        self.mqtt_client = MQTTClient(
            client_id,
            mqtt_broker,
            mqtt_port,
            keepalive=keepalive,
        )
        self.connected = False

    def connect(self):
        if not self.connected:
            print("MQTT connecting...")
            self.mqtt_client.connect()
            self.connected = True
            print("MQTT connected.")

    def publish(self, topic, message):
        if not self.connected:
            self.connect()
        return self.mqtt_client.publish(topic, message)

    def disconnect(self):
        if self.connected:
            self.mqtt_client.disconnect()
            self.connected = False

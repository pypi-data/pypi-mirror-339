from paho.mqtt.client import Client


class MqttClientMock(Client):
    def __init__(self):
        self.messages = []

    def publish(self, **kwargs) -> None:
        self.messages.append(kwargs)

    def _reset_sockets(self):
        pass

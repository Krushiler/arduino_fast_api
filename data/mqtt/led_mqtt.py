import paho.mqtt.client as mqtt_client


class LedMqtt:
    def __init__(self):
        broker = "broker.emqx.io"
        self._client = mqtt_client.Client('krushiler')
        self._client.connect(broker)
        self._client.loop_start()

    def publish_led_config(self, value, device_id):
        self._client.publish(f"lab/krushiler/strip/{device_id}/set_leds", value)
        print(f"Published {value} to lab/krushiler/strip/{device_id}/set_leds")

    # 255000000000255000255000000000255000000000255

    def close(self):
        self._client.disconnect()
        self._client.loop_stop()

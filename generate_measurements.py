from time import sleep
from random import randint, random
import paho.mqtt.client as mqtt
import signal
import sys
import settings

# Set up MQTT client and subscribe to topics
client = mqtt.Client("Generator")
client.connect(settings.mqtt_broker_ip)


# Set up a ctrl-C catcher
def signal_handler(sig, frame):
    print('SIGINT')

    try:
        print("Stopping MQTT client")
        client.loop_stop()
        client.disconnect()
    except Exception as e:
        print(e)

    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


while(True):
    client.publish(settings.topics[randint(0, 3)], str(random() * 100.))
    sleep(0.5)

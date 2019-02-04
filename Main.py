from MeasurementType import MeasurementType
from Measurement import Measurement
from Base import Session
from datetime import datetime
import paho.mqtt.client as mqtt
import settings


def print_all():
    session = Session()

    print("Measurement Types:")
    try:
        measurement_types = session.query(MeasurementType).all()
        for mtype in measurement_types:
            print(mtype)
    except Exception as e:
        print(e)

    print("Measurements:")
    try:
        measurements = session.query(Measurement).all()
        for m in measurements:
            print(m)
    except Exception as e:
        print(e)

    session.close()


if __name__ == "__main__":
    import signal
    import sys
    from time import sleep

    # Set up MQTT client and subscribe to topics
    client = mqtt.Client("SQL Logger")
    client.connect(settings.mqtt_broker_ip)
    client.subscribe("apt/temperature")
    client.subscribe("apt/humidity")
    client.subscribe("apt/pressure")
    client.subscribe("apt/co2")

    # SQL Session
    session = Session()

    def on_message(client, userdata, message):
        print("message received ", str(message.payload.decode("utf-8")))
        print("message topic=", message.topic)

        try:
            ts = datetime.now()
            mtype = settings.topics.index(message.topic) + 1
            data = float(message.payload)
        except Exception as e:
            print(e)
            return

        m = Measurement(ts=ts, mtype=mtype, data=data)
        print("Adding measurement {}".format(m))
        session.add(m)
        session.commit()

    client.on_message = on_message
    client.loop_start()

    # Set up a ctrl-C catcher
    def signal_handler(sig, frame):
        print('SIGINT')

        try:
            print("Stopping MQTT client")
            client.loop_stop()
        except Exception as e:
            print(e)

        try:
            print("Closing SQL connection")
            session.close()
        except Exception as e:
            print(e)

        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    # Sit here forever
    while(True):
        sleep(1)

from MeasurementType import MeasurementType
from Measurement import Measurement
from Base import Session
from datetime import datetime
import paho.mqtt.client as mqtt
import settings
import secrets
from influxdb import InfluxDBClient


influx_client = InfluxDBClient(secrets.influx_database_server,
                               secrets.influx_database_port,
                               secrets.influx_username,
                               secrets.influx_password,
                               database=settings.influx_database_name)



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


# Handler for subscribed messages
def on_message(client, userdata, message):

    t = datetime.now()

    try:
        msg_session = Session()
        ts = t
        mtype = settings.topics.index(message.topic) + 1
        data = float(message.payload)
    except Exception as e:
        print(e)

    m = Measurement(ts=ts, mtype=mtype, data=data)
    print("Adding measurement {}".format(m))
    msg_session.add(m)
    msg_session.commit()
    msg_session.close()

    try:
        json_body = [
            {
                "measurement": message.topic.split('/')[-1],
                "tags": {
                    "location": "bedroom",
                    "device": "photon_prototype",
                },
                "time": t.isoformat(),
                "fields": {
                    "value": data
                }
            }
        ]

        influx_client.write_points(json_body)
    except Exception as e:
        print(e)



def configure_mqtt_client(mqtt_client, broker_ip):

    # Set up MQTT client and subscribe to topics
    try:
        if mqtt_client.connect(broker_ip) == 0:
            print("MQTT client connected to broker at {}".format(broker_ip))
    except TimeoutError:
        print("MQTT broker connection timed out.  Check broker is running and IP address is correct.")
        return False

    # Subscribe to our database topics
    for topic in settings.topics:
        if mqtt_client.subscribe(topic)[0] == 0:
            print("Subscribed to topic \'{}\'".format(topic))

    mqtt_client.on_message = on_message

    return True


if __name__ == "__main__":
    import signal
    import sys
    from time import sleep

    # SQL Session
    session = Session()

    client = mqtt.Client(settings.mqtt_client_name)
    if configure_mqtt_client(client, settings.mqtt_broker_ip):
        client.loop_start()
        print("MQTT loop started")
    else:
        exit(-1)

    # Set up a ctrl-C catcher
    def signal_handler(sig, frame):
        print('SIGINT')

        try:
            print("Stopping MQTT client")
            client.loop_stop()
            client.disconnect()
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

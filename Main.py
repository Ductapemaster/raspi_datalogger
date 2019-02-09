from MeasurementType import MeasurementType
from Measurement import Measurement
from Base import Session
from datetime import datetime
import paho.mqtt.client as mqtt
import settings
from flask import Flask, render_template, request
import threading
import json



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
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)

    try:
        msg_session = Session()
        ts = datetime.now()
        mtype = settings.topics.index(message.topic) + 1
        data = float(message.payload)
    except Exception as e:
        print(e)
        return

    m = Measurement(ts=ts, mtype=mtype, data=data)
    print("Adding measurement {}".format(m))
    msg_session.add(m)
    msg_session.commit()
    msg_session.close()


def configure_mqtt_client(mqtt_client, broker_ip):

    # Set up MQTT client and subscribe to topics
    try:
        print(mqtt_client.connect(broker_ip))
    except TimeoutError:
        print("MQTT broker connection timed out.  Check broker is running and IP address is correct.")
        return False

    # Subscribe to our database topics
    for topic in settings.topics:
        print(mqtt_client.subscribe(topic))

    mqtt_client.on_message = on_message

    return True


def start_flask():
    # Flask setup
    app = Flask(__name__)

    @app.route("/")
    def main():
        return render_template("graph_base.html",
                               title="Plots",
                               plots=[
                                   {
                                       'id': 1,
                                       'content_title': "Temperature",
                                       'measurement_type': "Temperature"
                                   },
                                   {
                                       'id': 2,
                                       'content_title': "Humidity",
                                       'measurement_type': "Humidity"
                                   },
                                   {
                                       'id': 3,
                                       'content_title': "Pressure",
                                       'measurement_type': "Pressure"
                                   },
                                   {
                                       'id': 4,
                                       'content_title': "CO2",
                                       'measurement_type': "CO2"
                                   }
                               ]
                               )

    @app.route("/data")
    def data():
        mtype = str(request.args.get('type'))
        print(mtype)

        try:
            s = Session()
            measurements = s.query(Measurement).join(MeasurementType).filter(MeasurementType.mtype.ilike(mtype))
            mtype = s.query(MeasurementType).filter(MeasurementType.mtype.ilike(mtype)).first()
            s.close()
        except Exception as e:
            print("SQL fetch error: {}".format(e))
            measurements = []

        data = {
            'cols': [{
                'id': 'Timestamp',
                'label': 'Timestamp',
                'type': 'date',
            },
                {
                    'id': mtype.mtype,
                    'label': "{} ({})".format(mtype.mtype, mtype.units),
                    'type': 'number',
                }],
            'rows': [],
        }

        for m in measurements:
            time_str = "Date({},{},{},{},{},{},{})".format(
                m.ts.year,
                m.ts.month,
                m.ts.day,
                m.ts.hour,
                m.ts.minute,
                m.ts.second,
                int(m.ts.microsecond / 1000.),
            )
            row = {
                'c': [
                    {'v': time_str},
                    {'v': m.data},
                ]
            }

            data['rows'].append(row)

        json_data = json.dumps(data)
        return json_data

    def run():
        app.run(host="0.0.0.0", debug=False)

    flask_thread = threading.Thread(target=run)
    flask_thread.setDaemon(True)
    flask_thread.start()



if __name__ == "__main__":
    import signal
    import sys
    from time import sleep

    # SQL Session
    session = Session()

    client = mqtt.Client("SQL Logger Test")
    if configure_mqtt_client(client, settings.mqtt_broker_ip):
        client.loop_start()
        print("MQTT loop started")
    else:
        exit(-1)

    # Startup webserver
    start_flask()

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

import paho.mqtt.client as mqtt
import settings
import secrets
from influxdb import InfluxDBClient
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)8s [ %(name)s ]: %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

logger_main = logging.getLogger('main')
logger_main.setLevel(logging.DEBUG)


influx_client = InfluxDBClient(secrets.influx_database_server,
                               secrets.influx_database_port,
                               secrets.influx_username,
                               secrets.influx_password,
                               database=settings.influx_database_name)


# Handler for subscribed messages
def on_message(client, userdata, message):

    try:
        data = float(message.payload)
        measurement_type = message.topic.split('/')[-1]
        units = settings.units[measurement_type]

        # Measurements are tagged with server time when received
        # TODO: Consider more accurate timekeeping methods
        json_body = [
            {
                "measurement": measurement_type,
                "tags": {
                    "location": "bedroom",
                    "device": "photon_prototype",
                    "units": units
                },
                "fields": {
                    "value": data
                }
            }
        ]

        write_response = influx_client.write_points(json_body)
        if write_response:
            logger_main.info("Added measurement: {}".format(json_body))
        else:
            logger_main.warning("InfluxDB write failed")
    except Exception:
        logger.critical("MQTT message parsing failed: ", exc_info=True)


def configure_mqtt_client(mqtt_client, broker_ip):

    # Set up MQTT client and subscribe to topics
    try:
        if mqtt_client.connect(broker_ip) == 0:
            logger_main.info("MQTT client connected to broker at {}".format(broker_ip))
    except TimeoutError:
        logger_main.critical("MQTT broker connection timed out.  Check broker is running and IP address is correct.",
                             exc_info=True)
        return False

    # Subscribe to our database topics
    topics = "{}/#".format(settings.mqtt_prefix)
    reply = mqtt_client.subscribe(topics)
    if reply[0] == 0:
        logger_main.info("Subscribed to topics \'{}\'".format(topics))
    else:
        logger_main.critical(reply)
        return False

    mqtt_client.on_message = on_message

    return True


if __name__ == "__main__":
    import signal
    import sys
    from time import sleep

    client = mqtt.Client(settings.mqtt_client_name)
    if configure_mqtt_client(client, settings.mqtt_broker_ip):
        client.loop_start()
        logger_main.info("MQTT loop started")
    else:
        exit(-1)

    # Set up a ctrl-C catcher
    def signal_handler(sig, frame):
        logger_main.info('SIGINT')

        try:
            logger_main.info("Stopping MQTT client")
            client.loop_stop()
            client.disconnect()
        except Exception as e:
            logger_main.critical("Error stopping MQTT loop: ", exc_info=True)

        try:
            logger_main.info("Closing InfluxDB connection")
            influx_client.close()
        except Exception as e:
            logger_main.info("Error closing InfluxDB connection: ", exc_info=True)

        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    # Sit here forever
    while(True):
        sleep(1)

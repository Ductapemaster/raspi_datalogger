from flask import Flask, render_template, request
from Base import Session
from MeasurementType import MeasurementType
from Measurement import Measurement
import json
from datetime import datetime, timedelta
from influxdb import InfluxDBClient
import secrets
import settings

influx_client = InfluxDBClient(secrets.influx_database_server,
                               secrets.influx_database_port,
                               secrets.influx_username,
                               secrets.influx_password,
                               database=settings.influx_database_name)

# Flask setup
app = Flask(__name__)

@app.route("/")
def main():
    return render_template("graph_base.html",
                           title="Plots",
                           plots=[
                               {
                                   'id': 1,
                                   'content_title': "Temperature (deg C)",
                                   'measurement_type': "temperature"
                               },
                               {
                                   'id': 2,
                                   'content_title': "Humidity (%)",
                                   'measurement_type': "humidity"
                               },
                               {
                                   'id': 3,
                                   'content_title': "Pressure (hPa)",
                                   'measurement_type': "pressure"
                               },
                               {
                                   'id': 4,
                                   'content_title': "CO2 (ppm)",
                                   'measurement_type': "co2"
                               }
                           ]
                           )


@app.route("/data")
def data():
    mtype = str(request.args.get('type'))
    start_utc = datetime.fromtimestamp(int(request.args.get('start')) / 1000.)# + timedelta(hours=settings.timezone_offset)
    end_utc = datetime.fromtimestamp(int(request.args.get('end')) / 1000.)# + timedelta(hours=settings.timezone_offset)

    try:
        query = "SELECT value FROM {} WHERE time >= \'{}\' AND time <= \'{}\';".format(mtype, start_utc, end_utc)
        print(query)
        measurements = influx_client.query(query, epoch='u')
    except Exception as e:
        print("Influx fetch error: {}".format(e))
        measurements = []

    json_data = {
        'cols': [{
            'id': 'Timestamp',
            'label': 'Timestamp',
            'type': 'date',
        },
            {
                'id': mtype,
                'label': "{} ({})".format(mtype, settings.units[mtype] if mtype in settings.units.keys() else "unitless"),
                'type': 'number',
            }],
        'rows': [],
    }

    for m in measurements.get_points():
        ts = datetime.fromtimestamp(m['time'] / 1000000)
        time_str = "Date({},{},{},{},{},{},{})".format(
            ts.year,
            ts.month - 1,
            ts.day,
            ts.hour,
            ts.minute,
            ts.second,
            int(ts.microsecond / 1000.),
        )
        row = {
            'c': [
                {'v': time_str},
                {'v': m['value']},
            ]
        }

        json_data['rows'].append(row)

    json_data = json.dumps(json_data)
    return json_data


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)


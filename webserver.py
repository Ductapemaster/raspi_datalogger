from flask import Flask, render_template, request
from Base import Session
from MeasurementType import MeasurementType
from Measurement import Measurement
import json
import threading

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

    try:
        s = Session()
        measurements = s.query(Measurement).join(MeasurementType).filter(MeasurementType.mtype.ilike(mtype))
        mtype = s.query(MeasurementType).filter(MeasurementType.mtype.ilike(mtype)).first()
        s.close()
    except Exception as e:
        print("SQL fetch error: {}".format(e))
        measurements = []

    json_data = {
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
            m.ts.month - 1,
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

        json_data['rows'].append(row)

    json_data = json.dumps(json_data)
    return json_data


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)


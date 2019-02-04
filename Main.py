from MeasurementType import MeasurementType
from Measurement import Measurement
from Base import Session


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
    print_all()

from Base import Base, engine, Session
from MeasurementType import MeasurementType
from sqlalchemy import exc


def create_schema():
    Base.metadata.create_all(engine)
    print("Schema created\n")


def perform_inserts():

    session = Session()

    measurement_types = [
        MeasurementType(1, "Temperature", "Celsius"),
        MeasurementType(2, "Humidity", "%"),
        MeasurementType(3, "Pressure", "mPa"),
        MeasurementType(4, "CO2", "ppm"),
    ]

    for mt in measurement_types:
        session.add(mt)

    try:
        session.commit()
    except exc.IntegrityError as e:
        print("Error performing inserts: {}".format(e))

    session.close()


if __name__ == "__main__":
    create_schema()
    perform_inserts()
    print("DB Initialized")

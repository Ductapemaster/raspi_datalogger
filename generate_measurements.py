from Measurement import Measurement
from MeasurementType import MeasurementType
from Base import Session, Base, engine
from time import sleep
from datetime import datetime
from random import randint, random

Base.metadata.create_all(engine)

while(True):
    session = Session()
    m = Measurement(ts=datetime.now(), mtype=randint(1, 4), data=random() * 100.)
    print("Adding measurement {}".format(m))
    session.add(m)

    session.commit()
    session.close()

    sleep(0.5)

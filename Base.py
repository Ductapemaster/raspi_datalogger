import secrets
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

engine = create_engine("mysql://{}:{}@localhost/datalogger".format(secrets.sql_username, secrets.sql_password))
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

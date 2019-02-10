from secrets import sql_database_url
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

# Trying fix for "mysql server has gone away" exception:
# https://stackoverflow.com/questions/6471549/avoiding-mysql-server-has-gone-away-on-infrequently-used-python-flask-server
engine = create_engine(sql_database_url)
Session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()

from secrets import sql_database_url
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


engine = create_engine(sql_database_url)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

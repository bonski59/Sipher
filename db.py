

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Float, Boolean, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, load_only
from sqlalchemy.sql import exists, cast
from sqlalchemy.exc import IntegrityError, OperationalError
Base = declarative_base()



class File(Base):   # creates table named person
    __tablename__ = "file_characteristics"

    id = Column(Integer, primary_key=True)
    root_path = Column(String, unique=True, nullable=False)
    name = Column(String, unique=False)
    tech = Column(String, unique=False)
    data_type = Column(String, unique=False)
    date = Column(String, nullable=True)
    size = Column(String)
    max_lat = Column(Float)
    min_lat = Column(Float)
    max_lon = Column(Float)
    min_lon = Column(Float)


engine = create_engine('sqlite:///surveyfiles.db', echo=False)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()






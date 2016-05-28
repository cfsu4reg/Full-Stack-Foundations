import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DATE, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from sqlalchemy.dialects.sqlite.base import DATE

StateEnum = ('ca', 'ny', 'tx', 'pa')
GenderEnum = ('male', 'female')

Base = declarative_base()


class Shelter(Base):
    __tablename__ = 'shelter'
    name = Column(String(250), nullable=False)
    address = Column(String(1000), nullable=False)
    city = Column(String(250), nullable=False)
    state = Column(String(250), nullable=False)
    zipCode = Column(String(5), nullable=False)
    website = Column(String(1000), nullable=False)
    id = Column(Integer, primary_key=True)

class Puppy(Base):
    __tablename__ = 'puppy'
    name = Column(String(250), nullable=False)
    picture = Column(String)
    dateOfBirth = Column(DATE, nullable=False)
    gender = Column(Enum(*GenderEnum), nullable=False)
    weight = Column(Integer, nullable=False)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)
    id = Column(Integer, primary_key=True)


engine = create_engine('sqlite:///puppyshelter.db')


Base.metadata.create_all(engine)

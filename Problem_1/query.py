from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc, asc
from sqlalchemy import func
import datetime

from database_setup import Base, Shelter, Puppy


engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession()

def query1(session):
    puppies = session.query(Puppy).order_by(asc(Puppy.name))
    for puppy in puppies:
        print puppy.name
    
    print "\n"

def query2(session):
    today = datetime.date.today()
    
    puppies = session.query(Puppy).filter(Puppy.dateOfBirth > (today - datetime.timedelta(days = 6*30))).order_by(asc(Puppy.dateOfBirth))

    for puppy in puppies:
        print puppy.dateOfBirth
    
    print "\n"

def query3(session):
    puppies = session.query(Puppy).order_by(asc(Puppy.weight))

    for puppy in puppies:
        print puppy.weight
    
    print "\n"
    

def query4(session):
    puppyGroups = session.query(Puppy).group_by(Puppy.shelter_id)

    for puppyGroup in puppyGroups:
        shelter = session.query(Shelter).filter(Shelter.id == puppyGroup.shelter_id).one()
        print shelter.name
        puppies = session.query(Puppy).filter(Puppy.shelter_id == shelter.id)
        
        for puppy in puppies:
            print "   " + puppy.name
    print "\n"

def query5(session):
    """Query all puppies grouped by the shelter in which they are staying"""
    result = session.query(Shelter, func.count(Puppy.id)).join(Puppy).group_by(Shelter.id).all()
    for item in result:
        print item[0].id, item[0].name, item[1]

#query1(session)
#query2(session)
#query3(session)
query4(session)
query5(session)
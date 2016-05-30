from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc, asc
from sqlalchemy import func
from restaurant_schema import Base, Restaurant, MenuItem


def select_all_restaurants(session):
    return session.query(Restaurant).all()
        
def insert_restaurant(session, restaurant):
    session.add(restaurant)
    session.commit()

def update_restaurant(session, rid, rname):
    session.query(Restaurant).filter_by(id = rid).update({'name': rname})
    session.commit()
    
def select_restaurant_by_id(session, rid):
    return session.query(Restaurant).filter_by(id = rid).one()

def delete_restaurant_by_id(session, rid):
    session.query(Restaurant).filter_by(id = rid).delete()
    

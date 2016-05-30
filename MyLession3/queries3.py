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
    
def select_menus_from_restaurant(session, restaurant):
    return session.query(MenuItem).filter_by(restaurant_id = restaurant.id).all()

def select_menus_from_restaurant_id(session, rid):
    return session.query(MenuItem).filter_by(restaurant_id = rid).all()

def add_menu_to_restaurant_id(session, iname, rid):
    new_item = MenuItem(name = iname, restaurant_id = rid)
    session.add(new_item)
    session.commit()
    
def select_menu_by_id(session, menu_id):
    return session.query(MenuItem).filter_by(id = menu_id).one()
    
def update_menu(session, menu_id, new_name):
    session.query(MenuItem).filter_by(id = menu_id).update({'name': new_name})
    session.commit()

def delete_menu_by_id(session, menu_id):
    session.query(MenuItem).filter_by(id = menu_id).delete()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc, asc
from sqlalchemy import func
from restaurant_schema import Base, Restaurant, MenuItem
from sqlalchemy.sql.elements import Null


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
    
def select_menu_by_id(session, menu_id):
    return session.query(MenuItem).filter_by(id = menu_id).one()

def add_menu_to_restaurant_id(session, new_item, rid):
    new_item.restaurant_id = rid
    session.add(new_item)
    session.commit()
    
def update_menu(session, menu_id, new_item):
    item = session.query(MenuItem).filter_by(id = menu_id)
    result = item.update({'name': new_item.name}) if new_item.name is not None else None
    result = item.update({'price': new_item.price}) if new_item.price is not None else None
    result = item.update({'description': new_item.description}) if new_item.description is not None else None
    result = item.update({'course': new_item.course}) if new_item.course is not None else None
    session.commit()

def delete_menu_by_id(session, menu_id):
    session.query(MenuItem).filter_by(id = menu_id).delete()

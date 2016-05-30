'''
Created on May 29, 2016

@author: cfsu
'''
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base

from queries3 import select_all_restaurants, insert_restaurant, update_restaurant, select_restaurant_by_id,\
    delete_restaurant_by_id, select_menus_from_restaurant, update_menu, select_menu_by_id
from restaurant_schema import Base, Restaurant, MenuItem

class Test(unittest.TestCase):
    #engine = create_engine('sqlite:///restaurantmenu_test.db')
    engine = create_engine('sqlite:///:memory:')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    
    def setUp(self):
        Base.metadata.create_all(self.engine)       

    def tearDown(self):
        Base.metadata.drop_all(self.engine)
        
    def testInsertAndSelectRestaurants(self):
        restaurant = Restaurant(name="KFC")
        insert_restaurant(self.session, restaurant)
        
        foundRestaurants = select_all_restaurants(self.session)
        self.assertEqual(len(foundRestaurants), 1, "didn't find exactly one record")
        self.assertEqual(foundRestaurants[0], restaurant, 'restaurant name is not identical')

    def testUpdate(self):
        restaurant = Restaurant(name="KFC")
        insert_restaurant(self.session, restaurant)
        new_name = 'ABC'
        update_restaurant(self.session, restaurant.id, new_name)
        foundRestaurants = select_all_restaurants(self.session)
        self.assertEqual(len(foundRestaurants), 1, "didn't find exactly one record")
        self.assertEqual(foundRestaurants[0].name, new_name, 'restaurant name is not identical')
        
    def testSelectById(self):
        restaurant = Restaurant(name="KFC")
        insert_restaurant(self.session, restaurant)

        foundRestaurant = select_restaurant_by_id(self.session, restaurant.id)
        self.assertEqual(foundRestaurant.name, restaurant.name, 'restaurant name is not identical')
        

    def testDelete(self):
        restaurant1 = Restaurant(name="KFC1")
        foundRestaurants = select_all_restaurants(self.session)
        self.assertEqual(len(foundRestaurants), 0 , 'table is not empty')     

        insert_restaurant(self.session, restaurant1)
        restaurant2 = Restaurant(name="KFC2")
        insert_restaurant(self.session, restaurant2)
        delete_restaurant_by_id(self.session, restaurant1.id)
        
        foundRestaurants = select_all_restaurants(self.session)
        self.assertEqual(len(foundRestaurants), 1 , 'delete was not successful')     
        self.assertEqual(foundRestaurants[0].name, restaurant2.name, 'wrong entry was deleted')

        
    def testSelectItemsFromRestaurant(self):
        restaurant1 = Restaurant(name="KFC1")
        insert_restaurant(self.session, restaurant1)

        menuItem1 = MenuItem(name="French Fries", description="with garlic and parmesan",
                     price="$2.99", course="Appetizer", restaurant=restaurant1)
        self.session.add(menuItem1)
        self.session.commit()

        restaurant2 = Restaurant(name="KFC2")
        insert_restaurant(self.session, restaurant2)
        
        menuItem2 = MenuItem(name="Veggie Burger", description="Juicy grilled veggie patty with tomato mayo and lettuce",
                     price="$7.50", course="Entree", restaurant=restaurant1)
        self.session.add(menuItem2)
        self.session.commit()

        items1 = select_menus_from_restaurant(self.session, restaurant1)
        self.assertEqual(items1[0], menuItem1, 'wrong menu item was found')
        
    def testUpdateItem(self):
        restaurant1 = Restaurant(name="KFC1")
        insert_restaurant(self.session, restaurant1)

        menuItem1 = MenuItem(name="French Fries", description="with garlic and parmesan",
                     price="$2.99", course="Appetizer", restaurant=restaurant1)
        self.session.add(menuItem1)
        self.session.commit()
                
        update_menu(self.session, menuItem1.id, MenuItem(name="Noodle"))
        found_item = select_menu_by_id(self.session, menuItem1.id)
        self.assertEqual(found_item.name, "Noodle", 'menu name was not updated')
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testSelectRestaurants']
    unittest.main()
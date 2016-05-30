from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 

from queries3 import select_all_restaurants, insert_restaurant, select_restaurant_by_id, update_restaurant,\
     delete_restaurant_by_id,\
     select_menus_from_restaurant, select_menus_from_restaurant_id,\
     select_menu_by_id, add_menu_to_restaurant_id, update_menu, delete_menu_by_id
from restaurant_schema import Base, Restaurant, MenuItem

def start_db():
    engine = create_engine('sqlite:///restaurantmenu.db')
    DBSession = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)       
    session = DBSession()
    return session

app = Flask(__name__)
db_session = start_db()

#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]

#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree', 'id': '11'}


@app.route('/')
@app.route('/restaurant/')
def showRestaurants():
    restaurants = select_all_restaurants(db_session)
    return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        restaurant = Restaurant(name = request.form['name'])
        insert_restaurant(db_session, restaurant)
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newrestaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    restaurant = select_restaurant_by_id(db_session, restaurant_id)
    if request.method == 'POST':
        update_restaurant(db_session, restaurant_id, request.form['name'] )
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('editrestaurant.html', restaurant = restaurant)

@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurant = select_restaurant_by_id(db_session, restaurant_id)
    if request.method == 'POST':
        delete_restaurant_by_id(db_session, restaurant_id)
        return redirect(url_for('showRestaurants'))        
    else:
        return render_template('deleterestaurant.html', restaurant = restaurant)


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    restaurant = select_restaurant_by_id(db_session, restaurant_id)
    items = select_menus_from_restaurant_id(db_session, restaurant_id)
    return render_template('showmenu.html', restaurant = restaurant, items = items)

@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    restaurant = select_restaurant_by_id(db_session, restaurant_id)
    if request.method == 'POST':
        new_item = MenuItem(name = request.form['name'],\
                            price = request.form['price'],\
                            course = request.form['course'],\
                            description = request.form['description']\
                            )
        add_menu_to_restaurant_id(db_session, new_item, restaurant_id)
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant = restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:item_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, item_id):
    restaurant = select_restaurant_by_id(db_session, restaurant_id)
    item = select_menu_by_id(db_session, item_id)
    if request.method == 'POST':
        new_item = MenuItem(name = request.form['name'],\
                            price = request.form['price'],\
                            course = request.form['course'],\
                            description = request.form['description']\
                            )
        update_menu(db_session, item_id, new_item)
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant = restaurant, item = item)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:item_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, item_id):
    restaurant = select_restaurant_by_id(db_session, restaurant_id)
    item = select_menu_by_id(db_session, item_id)
    if request.method == 'POST':
        delete_menu_by_id(db_session, item_id)
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('deletemenuitem.html', restaurant = restaurant, item = item)

if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

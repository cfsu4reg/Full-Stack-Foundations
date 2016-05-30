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

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = select_restaurant_by_id(db_session, restaurant_id)
    items = select_menus_from_restaurant_id(db_session, restaurant_id)
    return render_template('menu.html', restaurant = restaurant, items = items)

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = select_restaurant_by_id(db_session, restaurant_id)
    items = select_menus_from_restaurant_id(db_session, restaurant_id)
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        add_menu_to_restaurant_id(db_session, request.form['name'], restaurant_id)
        flash("new menu item created")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id = restaurant_id)



@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    restaurant = select_restaurant_by_id(db_session, restaurant_id)
    menu = select_menu_by_id(db_session, menu_id)
    if request.method == 'POST':
        update_menu(db_session, menu_id, MenuItem(name = request.form['name']))
        flash("menu item updated")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant = restaurant, menu = menu)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def MenuItemJSON(restaurant_id, menu_id):
    restaurant = select_restaurant_by_id(db_session, restaurant_id)
    menu = select_menu_by_id(db_session, menu_id)
    return jsonify(Menu=menu.serialize)
    


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    restaurant = select_restaurant_by_id(db_session, restaurant_id)
    item = select_menu_by_id(db_session, menu_id)
    if request.method == 'POST':
        delete_menu_by_id(db_session, menu_id)
        flash("menu item deleted")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('deletemenuitem.html', restaurant_id = restaurant_id, item = item)


if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

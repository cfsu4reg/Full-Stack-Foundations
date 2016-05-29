from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base

from queries import select_all_restaurants, insert_restaurant, select_restaurant_by_id, update_restaurant,\
    delete_restaurant_by_id
from restaurant_schema import Base, Restaurant, MenuItem

def start_db():
    engine = create_engine('sqlite:///restaurantmenu.db')
    DBSession = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)       
    session = DBSession()
    return session

class webServerHandler(BaseHTTPRequestHandler):
    db_session = start_db()
    
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Create new restaurant</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>Please enter the name of new restaurant?</h2><input name="restaurant_name" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/edit"):
                start = self.path.find('restaurants/') + 13
                end = self.path.find('/edit', start)
                rid = self.path[start:end]
                restaurant = select_restaurant_by_id(self.db_session, rid)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h2>Enter the new name for %s</h2>" % restaurant.name
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurant/%s/edit'><input name="restaurant_name" type="text" ><input type="submit" value="Submit"> </form>''' % rid
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/delete"):
                rid = self.path.split('/')[2] # /restaurant/5/delete
                restaurant = select_restaurant_by_id(self.db_session, rid)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h2>Are you sure you want to delete %s ?</h2>" % restaurant.name
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurant/%s/delete'><input type="submit" value="Confirm"> </form>''' % rid
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurants = select_all_restaurants(self.db_session)
                output = ""
                output += "<html><body>"
                output += "<h1>Here are a list of restaurants</h1>"
                output += "<table>"
                for resturant in restaurants:
                    output += '<tr><td> %s </td>' % resturant.name
                    output += '<td><a href=\"restaurant/%s/edit\"> Edit</a> </td>' % resturant.id
                    output += '<td><a href=\"restaurant/%s/delete\"> Delete</a>  </td></tr>' % resturant.id
                output += "</table>"
                output += "<a href=\"restaurants/new\"> Create new restaurant</a>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurant = Restaurant(name = fields.get('restaurant_name')[0])
                    print "Creating restaurant %s" % restaurant.name
                    insert_restaurant(self.db_session, restaurant)
                    
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

            if self.path.endswith("/edit"):
                start = self.path.find('restaurants/') + 13
                end = self.path.find('/edit', start)
                rid = self.path[start:end]
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    update_restaurant(self.db_session, rid, fields.get('restaurant_name')[0])
                    
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')

            if self.path.endswith("/delete"):
                rid = self.path.split('/')[2] # /restaurant/5/delete
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    delete_restaurant_by_id(self.db_session, rid)
                    
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')

        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()

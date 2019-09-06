from requests import get, post
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, unquote
from os import environ
from threading import *
import psycopg2
from bleach import clean
from socketserver import ThreadingMixIn
from bookmark_form import bookmark_form_1, bookmark_form_2

memory = {}
short_form = '''<div style="background-color: #eee; padding: 20px">
                    <h3 style="font-weight: 300">The URL for your specified site is <a href="{0}">https://compacturl.herokuapp.com/{1}</a></h3>
                </div>'''

db_name = "postgres://pnivxdxccbwtsz:a88f54b5ee63d5724472a5bdd7eafdbf1fb3fb6ec2870cdba71d901d4e45f391@ec2-174-129-27-3.compute-1.amazonaws.com:5432/dac5dbdv3bg8q8"

class ThreadHTTPserver(ThreadingMixIn, HTTPServer):
    "This is an HTTPServer that supports thread based concurrency."


class bookmark_server(BaseHTTPRequestHandler):

    def do_GET(self):
        if len(self.path) > 1:
            # if there is a path (name) specified
            name = unquote(self.path[1:])
            # unquote it & chck if it is in memory

            # connect to database
            db_get = psycopg2.connect("dbname={0}".format(db_name))
            cur = db_get.cursor()
            cur.execute("select name, url from shortnames")
            result = cur.fetchall()
            # save data to memory
            for row in result:
                memory[row[0]] = row[1]
                
            
            if name in memory:
                # if name exist in the memory then there will be a url associated with it, redirect there
                self.send_response(303)
                self.send_header('Location', memory[name])
                self.end_headers()
            else:
                # if name not in memory, respond as not found.
                self.send_response(404)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write("There no such page as '{}'.".format(name).encode())
            

        else:
            # in case of no path (name) specified, send the form to make a short url.
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(bookmark_form_1.encode())

    
    def do_POST(self):
        # when we post the form for a url to make it short, this method gets trigred.
        # here we extract the information from the form
        post_req_headrs = self.headers
        raw_content = self.rfile.read(int(post_req_headrs.get('Content-length', 0))).decode()
        # read its content
        parsed_content = parse_qs(raw_content)
        # parse it into a dic of lists
        if len(parsed_content) == 2:
            # insure that there is a name and a url associated to it.
            url_given = parsed_content['url_body'][0]
            short_url = parsed_content['short-name'][0]
            # save those to a variable.
            if self.checkURI(url_given) == True:
                # check if the url specified is actual a page on the web

                # connect to database
                db_post = psycopg2.connect("dbname={0}".format(db_name))
                cur = db_post.cursor()
                try:
                    cur.execute("insert into shortnames values (%s, %s);", ((clean(short_url),), (clean(url_given),)))
                    db_post.commit()
                    db_post.close()
                    # then store it in a dic named memory.
                    # and send a response confirming that the url is shortened successfully 
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(short_form.format(url_given, short_url).encode())
                except Exception as e:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(bookmark_form_2.encode())
            else:
                # if there is no such page send 404.
                self.send_response(404)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write('<h2>The url you entered cannot be found</h2>'.encode())     
        else:
            # if something is missing in the form send a "Bad request" response.
            self.send_response(400)


    def checkURI(self, url_arg):
        # it does it by sending a get request to the url, if funcn gets a response back it returns true
        try:
            reponse_obj = get(url_arg)
            return True
        except Exception as error:
            # if there is no such page it gets an error, so the funcn returns false.
            print(error)
            return False

# Todo: Make memory permanent


if __name__ == '__main__':
    port = int(environ.get('PORT', 8000))
    server_address = ('', port)
    http_server = ThreadHTTPserver(server_address, bookmark_server)
    http_server.serve_forever()



from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from login import Login
from index import Index
from feed import Feed
from oauth_handler import OAuthHandler


app = webapp.WSGIApplication([	('/', Index),
								('/index', Index),
                                ('/login', Login),
                                ('/oauth_handler', OAuthHandler),
								(r'/feed/(.*)', Feed),
                                ],
                                debug=True)

def main():
    run_wsgi_app(app)

if __name__ == "__main__":
    main()
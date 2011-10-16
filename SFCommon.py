import jinja2
from google.appengine.ext import db
from instagram.client import InstagramAPI
import os

def get_jinja_environment():
	dirname = os.path.dirname(__file__)
	return jinja2.Environment(
    loader=jinja2.FileSystemLoader( os.path.join( dirname, "templates" ) ))

class SFInstagramAPI(InstagramAPI):
	def __init__(self, access_token=None ):
		client_id = "some Instagram API client id"
		client_secret = "some Instagram API client secret"
		redirect_uri = "http://some.url/oauth_handler"
		# redirect_uri = "http://localhost:8081/oauth_handler"
		super( SFInstagramAPI, self ).__init__( client_id=client_id,
												client_secret=client_secret,
												redirect_uri=redirect_uri,
												access_token=access_token )

class UserToken(db.Model):
	token = db.StringProperty(required=True)
	userid = db.StringProperty(required=True)

class SFTemplate(object):
	def __init__(self, template_path, subs ):
		self.template = get_jinja_environment().get_template( template_path )
		self.subs = subs
		
	def render(self):
		return self.template.render( self.subs )

class SFError( SFTemplate ):
	def __init__(self, error, reason, description ):
		subs = { 'error': error, 'reason':reason, 'description':description }
		super( SFError, self ).__init__( "error.html", subs )

class SFMessage( SFTemplate ):
	def __init__(self, in_message ):
		super( SFMessage, self ).__init__( "message.html", { 'message': in_message } )
		

import SFCommon
from google.appengine.ext import webapp

class Login(webapp.RequestHandler):

	def get(self):
		api = SFCommon.SFInstagramAPI()
		redirect_uri = api.get_authorize_login_url()
		self.redirect( redirect_uri )

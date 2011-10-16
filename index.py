import SFCommon
from google.appengine.ext import webapp

class Index(webapp.RequestHandler):
	def get(self):	
		template = SFCommon.get_jinja_environment().get_template('index.html')
		self.response.out.write( template.render() )
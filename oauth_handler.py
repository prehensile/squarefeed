from google.appengine.ext import webapp
from SFCommon import SFInstagramAPI, UserToken, SFError
import SFCommon
from google.appengine.ext import db
from instagram.oauth2 import OAuth2AuthExchangeError

class OAuthHandler(webapp.RequestHandler):
	
	def get(self):	
	
		code = self.request.get("code")
		error = self.request.get("error")
		error_reason = self.request.get("error_reason")
		error_description = self.request.get("error_description")
		
		if( code is '' ):
			self.response.out.write( SFError( error, error_reason, error_description ).render() )
		else: 
			api = SFInstagramAPI()
			try:
				access_token = api.exchange_code_for_access_token(code)
			except OAuth2AuthExchangeError:
				error_body = "This usually happens if you try to reload a page during the login process: the access code Squarefeed gets from Instagram only works once."
				self.response.out.write( SFError( "OAuth2AuthExchangeError", "exchange_code_for_access_token failed", error_body ).render() )
				return
				
			if( not access_token ):
				self.response.out.write( SFError( "No access token", "Didn't get an access token from Instagram", ":(" ).render() )
			else :
				api = SFInstagramAPI( access_token )
				user = api.user()
				user_id = user.id;
				uq = db.Query( UserToken );
				uq.filter( 'userid =', user_id )
				res = uq.get()
				if( res is None ):
					# new entity
					ut = UserToken( userid=user_id, token=access_token )
					ut.put()
				else:
					# update existing entity
					ut = res
					ut.token = access_token
					ut.put()
					
				feed_url = "/feed/%s" % user_id
				
				template = SFCommon.get_jinja_environment().get_template('auth_complete.html')
				self.response.out.write( template.render({ 'feed_url': feed_url, 'user_name':user.username }) )
				
			
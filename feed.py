import jinja2
import os
import SFCommon
from google.appengine.ext import db, webapp
from datetime import datetime

def rfc822( in_date ):
	return in_date.strftime( "%a, %d %b %Y %H:%M:%S +0000" )

class Feed(webapp.RequestHandler):
	
	def get(self,user_id):	
		
		# remove trailing path bits
		components = user_id.split( '/' )
		user_id = components[0];
			
		uq = db.Query( SFCommon.UserToken );
		uq.filter( 'userid =', user_id )
		res = uq.get()
		
		if( res is None ):
			self.response.out.write(SFCommon.SFError(	"NoToken",
														"Couldn't find a token for this user id.",
														"Squarefeed doesn't have any details stored for this user." ).render())
		else:
			api = SFCommon.SFInstagramAPI( res.token )
			user = api.user()
			
			items = []
			recent_media, next = api.user_recent_media(count=100)
			
			for media_item in recent_media:
				title = "Untitled photo"
				if( media_item.caption ):
					title = media_item.caption.text
				img_src = media_item.images['low_resolution'].url
				link = media_item.link
				if( link is None ):
					link = media_item.images['standard_resolution'].url
				items.append(	{ 	'title': title,
									'image_src': img_src,
									'link': link,
									'guid': media_item.id,
									'date': rfc822( media_item.created_time ) } )
			
			description = ( 'Instagram feed for %s' % user.username )
			self_link = self.request.url
			build_date = rfc822( datetime.utcnow() )
			template_data = {
				'title' : description,
				'self_link': self_link,
				'description': description,
				'build_date': build_date,
				'items': items
			}
			
			template = SFCommon.get_jinja_environment().get_template('feed.rss')
        	self.response.headers["Content-Type"] = "application/rss+xml"
        	self.response.out.write(template.render(template_data))
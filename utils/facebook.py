import requests as r
from requests import Session
from requests.exceptions import HTTPError
from lxml import html, etree

""" Hacky little class to authenticate as the tinder app """
class FacebookClient():


	def __init__(self):
		self.session = Session()

		self.token = ''

		self.headers = {
			'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; XT1562 Build/LPD23.118-10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36'
		}

		self.session.headers.update(self.headers)

	def authenticate(self, username, password):
		response = self.session.post(
			'http://m.facebook.com/login.php',
			data={
			'email': username,
			'pass': password,
			}
		)

		response.raise_for_status()

		title = html.fromstring(response.content).xpath('//title/text()')[0]

		if title != 'Facebook':
			raise HTTPError(403, 'Unauthorised. Failed to login to Facebook')

		return self		

			

	def get_oauth_token(self, tinderClient=None):
		tinder_oauth = """https://www.facebook.com/dialog/oauth?client_id=464891386855067&redirect_uri=https://www.facebook.com/connect/login_success.html&scope=basic_info,email,public_profile,user_about_me,user_activities,user_birthday,user_education_history,user_friends,user_interests,user_likes,user_location,user_photos,user_relationship_details&response_type=token"""

		response = self.session.get(tinder_oauth)

		if 'Success' in response.content:
			print "Got OAuth Token"
			self.token = response.history[1].headers['location'].split('#access_token=')[1].split('&expires')[0]	
		else:	
			print 'Could not get OAuth Token'
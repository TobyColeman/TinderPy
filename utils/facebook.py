import requests as r
from requests import Session
from lxml import html, etree

""" Hacky little class to authenticate as the tinder app """
class FacebookClient():


	def __init__(self, username=None, password=None):
		self.session = Session()
		self.auth_token = ''

		self.username = username
		self.password = password

		self.headers = {
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'
		}

		self.session.headers.update(self.headers)


	def authenticate(self):

		payload = self.make_payload()

		response = self.session.post(
			'https://www.facebook.com/login.php?login_attempt=1',
			data=payload)

		if 'Redirecting...' in response.content:
			print 'Successfully logged into Facebook!'
			return True;
		
		print 'Could not log into Facebook.'
		return False



	def make_payload(self):
		payload = {
			'email': self.username,
			'pass': self.password,
			'persistent': 1,
			'default_persistent':1
		}

		# get hidden form fields
		response = self.session.get('https://facebook.com')
		tree = html.fromstring(response.content)
		form = tree.xpath('//form[@id="login_form"]')[0]

		# add them to the post payload
		payload['lsd'] = form.xpath('input[@name="lsd"]/@value')[0]
		payload['lgnrnd'] =  form.xpath('input[@name="lgnrnd"]/@value')[0]
		payload['lgnjs'] =  form.xpath('input[@name="lgnjs"]/@value')[0]

		return payload


	def get_token(self):
		tinder_oauth = """https://www.facebook.com/dialog/oauth?client_id=464891386855067&redirect_uri=https://www.facebook.com/connect/login_success.html&scope=basic_info,email,public_profile,user_about_me,user_activities,user_birthday,user_education_history,user_friends,user_interests,user_likes,user_location,user_photos,user_relationship_details&response_type=token"""

		response = self.session.get(tinder_oauth)

		if 'Success' in response.content:
			print "Fetched OAuth Token"
			return response.history[0].headers['location'].split('#access_token=')[1].split('&expires')[0]	
		print 'Could not get OAuth Token'
		return None
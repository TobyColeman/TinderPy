import requests as r
from requests import Session
from requests.exceptions import HTTPError


class FacebookClient:
	""" Grabs oauth token and facebook id needed to authenticate with tinder """
	def __init__(self):
		self.session = Session()
		self.token = ''
		self.fbid = ''
		self.headers = {
			'User-Agent': 'Mozilla/5.0 (Linux; U; en-gb; KFTHWI Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Silk/3.16 Safari/535.19'
		}
		self.session.headers.update(self.headers)

	def authorise(self, email, password):
		login_endpoint = 'https://m.facebook.com/login/?api_key=464891386855067&auth_token=fd321ee3f34591e7243559f561b17414&skip_api_login=1&signed_next=1&next=https%3A%2F%2Fm.facebook.com%2Fv2.6%2Fdialog%2Foauth%3Fredirect_uri%3Dfb464891386855067%253A%252F%252Fauthorize%252F%26scope%3Duser_birthday%252Cuser_photos%252Cuser_education_history%252Cemail%252Cuser_relationship_details%252Cuser_friends%252Cuser_work_history%252Cuser_likes%26response_type%3Dtoken%252Csigned_request%26client_id%3D464891386855067%26ret%3Dlogin%26logger_id%3Dd915f033-b98d-404a-beaa-79ce6f8301de&refsrc=https%3A%2F%2Fm.facebook.com%2Flogin.php&app_id=464891386855067&lwv=100'
		confirm_endpoint = 'https://m.facebook.com/v2.6/dialog/oauth/confirm'

		login_response = self.session.post(login_endpoint, { 'email': email, 'pass': password })
		login_response.raise_for_status()

		if 'Set-Cookie' not in login_response.headers:
			raise HTTPError(403, 'Failed to login to Facebook. Is your email and password correct?')

		confirm_response = self.session.post(
			confirm_endpoint,
			data = {
				'fb_dtsg': self._get_fb_dtsg(login_response.text),
				'from_post': '1',
				'app_id': '464891386855067',
				'redirect_uri': 'fb464891386855067://authorize/',
				'display': 'touch',
				'sheet_name': 'initial',
				'return_format': 'signed_request,access_token',
				'ref': 'Default',
				'__CONFIRM__': 'OK'
			}
		)
		confirm_response.raise_for_status()

		self.fbid = self._get_fbid_from_cookies()
		self.token = self._parse_token(confirm_response.text)

		return { 'fbid': self.fbid, 'token': self.token }

	def _get_fbid_from_cookies(self):
		return self.session.cookies.get('c_user')

	def _get_fb_dtsg(self, response_content):
		return response_content.split('fb_dtsg" value=')[1].split(' ')[0].strip('"')

	def _parse_token(self, token_string):
		return token_string.split('access_token=')[1].split('&')[0]

import requests as r
from requests import Session
import json

class TinderClient():

	def __init__(self):

		# tinder api 
		self.TINDER_HOST = 'https://api.gotinder.com'

		# headers needed 
		self.headers = {
	        'User-Agent' : 'Tinder Android Version 4.1.2',
	        'os_version' : '16',
	        'X-Auth-Token': ''
		}

		# user's session
		self.session = Session()
		self.session.headers.update(self.headers)


	def authenticate(self, fb_token):

		payload = {
			'facebook_token': fb_token
		}

		response = self.session.post(
					self.endpoint('auth'), 
					data=payload,
					headers=self.headers)

		if response.status_code == 200:
			data = json.loads(response.content)
			self.headers['X-Auth-Token'] = data['token']
			self.session.headers.update(self.headers)
			print "Logged into Tinder!"
			self.get_meta()
			return data
		print "Could not log into Tinder."
		return False

	def get_updates(self):
		response = self.session.post(self.endpoint('updates'))
		data = json.loads(response.content)

		return data

	def get_recs(self):
		response = self.session.post(self.endpoint('/user/recs'))
		data = json.loads(response.content)

		return data

	def get_meta(self):
		response = self.session.get(self.endpoint('meta'))
		data = json.loads(response.content)


	def update_location(self, latitude, longitude):
		payload = {
			'lat': latitude,
			'lon': longitude
		}
		response = self.session.post(self.endpoint('user/ping'),
				data=payload)


	def swipe(self, direction, id):
		if direction == 'y':
			endpoint = 'like/{0}'.format(id)
		elif direction == 'n':
			endpoint = 'pass/{0}'.format(id)

		response = self.session.get(self.endpoint(endpoint))
		data = json.loads(response.content)

		return data

	def message(self, message, m_id):

		payload = {
			'message': message
		}

		response = self.session.post(
				   self.endpoint('user/matches/{0}'.format(m_id),
				   data=payload))

		if response.status_code == 200:
			data = json.loads(response.content)
			return data
		return False

	def update_profile(self, distance=None, age_max=None, 
					   age_min=None, gender=None, 
					   discoverable=None):
		
		payload = {
			'distance_filter': distance,
			'age_filter_max': age_max,
			'age_filter_min': age_min,
			'gender_filter': gender,
			'discoverable': discoverable
		}

		response = self.session.post(self.endpoint('profile'),
				   data=payload)

		if response.status_code == 200:
			data = json.loads(response.content)
			return json.dumps(data)
		return False

	def endpoint(self, endpoint):
		return self.TINDER_HOST + "/" + endpoint

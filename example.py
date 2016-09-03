from utils import FacebookClient
from tinder import TinderClient

# create Facebook client
facebook = FacebookClient()

# create Tinder Client
tinder_client = TinderClient()

# authenticate with Facebook
fb_data = facebook.authorise('email', 'password')

#authenticate with the token from facebook
tinder_client.authenticate(fb_data['token'], fb_data['fbid'])

# get recommendations (the deck you'll be swiping through)
tinder_client.get_recs()

# get any new messages, matches etc..
tinder_client.get_updates()

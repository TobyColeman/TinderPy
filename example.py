from utils.facebook import FacebookClient
from tinder import TinderClient


# create Facebook client
facebook_client = FacebookClient()

# create Tinder Client
tinder_client = TinderClient()

# authenticate with Facebook and get oauth token
facebook_client.authenticate('email', 'password').get_oauth_token()

#authenticate with the token from facebook
tinder_client.authenticate(facebook_client.token)

# get recommendations (the deck you'll be swiping through)
tinder_client.get_recs()

# get any new messages, matches etc..
tinder_client.get_updates()



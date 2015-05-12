from utils.facebook import FacebookClient
from tinder import TinderClient


# authenticate with facebook and get oauth token needed for tinder login
F = FacebookClient('email', 'password')
F.authenticate()
token = F.get_token()

# create a tinder client
T = TinderClient()
# authenticate with the token from facebook
T.authenticate(token)

# get recommendations (the deck you'll be swiping through)
T.get_recs()

# get any new messages, matches etc..
T.get_updates()



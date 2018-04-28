import tweepy
from docs.conf import consumer_key, consumer_secret, access_token_secret, access_token
from time import sleep

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# For Secured Connection
auth.secure = True
api = tweepy.API(auth)

print(str(api.get_user(screen_name='@maniparas')))
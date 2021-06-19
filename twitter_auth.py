#Authentication for Twitter API access, using tweepy package
import tweepy

def get_api(consumer_key, consumer_secret, access_key, access_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, retry_count=10, retry_delay=10, retry_errors=set([104, 503]))
    return api
    
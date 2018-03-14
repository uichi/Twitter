mport tweepy

CONSUMER_KEY    = ""
CONSUMER_SECRET = ""
ACCESS_KEY      = ""
ACCESS_SECRET   = ""

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

tweets = api.search(q='ホーキング博士', count=10)
for tweet in tweets:
    print(tweet.text, "/n")

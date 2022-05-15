import os 
import tweepy as tw
import pandas as pd 

cd = os.path.dirname(os.path.abspath('1_data_gathering.py'))

api_key = #####
api_secret = #####
access_token = #####
access_token_secret = #####

# authentication
auth = tw.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)

api = tw.API(auth)

class Linstener(tw.Stream):

    tweets = []
    limit = 1000

    def on_status(self, status):
        self.tweets.append(status)

        if len(self.tweets) == self.limit:
            self.disconnect()

stream_tweet = Linstener(api_key, api_secret, access_token, access_token_secret)

# stream by keywords
keywords = ["#meme"]
stream_tweet.filter(track = keywords)

# create DataFrame
columns = ['User', 'Tweet', 'Date', 'Language', 'Hashtags', 'Image']
data = []

for tweet in stream_tweet.tweets: 
    if 'media' in tweet.entities: 
        for image in tweet.entities['media']:
            if not tweet.truncated: 
                data.append([tweet.user.screen_name, tweet.text, tweet.user.created_at, tweet.lang, tweet.entities['hashtags'], image['media_url']])
            else: 
                data.append([tweet.user.screen_name, tweet.extended_tweet['full_text'], tweet.user.created_at, tweet.lang, tweet.entities['hashtags'], 
                image['media_url']])

df = pd.DataFrame(data, columns = columns)
df.to_csv('data/df_meme_4.csv', index = False)

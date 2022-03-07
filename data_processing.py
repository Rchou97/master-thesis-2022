import os 
import tweepy as tw
import pandas as pd 

os.chdir("C:/Users/richa/OneDrive/Documenten/GitHub/master_thesis_2022/data") # created folder to save the meme information from searchtweets

api_key = 'GeXlknuvqxMFPG3UjK1b6qeK0'
api_secret = 'jwe70Ch2h8FzmFkKVnLjhwFRPCHBHNP92iM5240aZuuosk8JZg'
access_token = '1496989590716100612-pD4d0gHA8tPdyah9DL3sUNxRDA45Oc'
access_token_secret = 'cVk19f8Xu8LPkALuSwRxfFAFJMOgiD4fea6YnJhGK2ybR'

# authentication
auth = tw.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)

api = tw.API(auth)


class Linstener(tw.Stream):

    tweets = []
    limit = 500

    def on_status(self, status):
        self.tweets.append(status)
        # print(status.user.screen_name + ": " + status.text)

        if len(self.tweets) == self.limit:
            self.disconnect()



stream_tweet = Linstener(api_key, api_secret, access_token, access_token_secret)

# stream by keywords
keywords = ['2022', '#Memes']


stream_tweet.filter(track = keywords)

# create DataFrame
columns = ['User', 'Tweet', 'Date']
data = []

for tweet in stream_tweet.tweets:
    if not tweet.truncated:
        data.append([tweet.user.screen_name, tweet.text, tweet.])
    else:
        data.append([tweet.user.screen_name, tweet.extended_tweet['full_text'], tweet.Date])

df = pd.DataFrame(data, columns = columns)
df
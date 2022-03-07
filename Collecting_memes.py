# -*- coding: utf-8 -*-
from collections import defaultdict
from searchtweets import ResultStream, gen_rule_payload, load_credentials
from searchtweets import collect_results
import tweepy
import searchtweets
import pandas as pd
import random
import math
import json
import csv
import yaml
import os
import glob

os.chdir("C:/Users/richa/OneDrive/Documenten/GitHub/master_thesis_2022/data") # created folder to save the meme information from searchtweets


# searchtweet Auth 2.0

config = dict(
    search_tweets_api = dict(
        account_type = 'premium',
        endpoint = 'https://api.twitter.com/1.1/tweets/search/(type_premium_option)/(type_env_name).json', # change depends on  30-day Search and Full Archive Search: https://api.twitter.com/1.1/tweets/search/(30day or fullarchive)/(enviroment_name).json'
        consumer_key = 'paste_Consumer_key', 
        consumer_secret = 'paste_consumer_secret'
    )
)


with open('twitter_keys_30day.yaml', 'w') as config_file:
    yaml.dump(config, config_file, default_flow_style=False)


premium_search_args = load_credentials("twitter_keys_30day.yaml",
                                       yaml_key="search_tweets_api",
                                       env_overwrite=False)
print(premium_search_args)

#Tweepy authentication
consumer_key = "paste_Consumer_key"
consumer_secret = "paste_consumer_secret"
access_token = "paste_access_token"
access_token_secret = "paste_access_token_secret"


# Creating the authentication object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# Setting your access token and secret
auth.set_access_token(access_token, access_token_secret)

# Creating the API object while passing in auth information
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

#Search tweet information filter by keywords and removing retweets and replies
search_words_array = ["write here the keyword -RT -replies"]

for i in range(0, len(search_words_array)):
  rule = gen_rule_payload(search_words_array[i])

  tweets = collect_results(rule, 
                           max_results= 50,       
                           result_stream_args=premium_search_args)
  

def extract_early_adopters(tweet_object):
  early_adopters = [{'meme' : i, 'created_at_seconds' : tweet.created_at_seconds, 'user_id' : tweet.user_id} for i in search_words_array for tweet in tweet_object]
   
  df = pd.DataFrame(early_adopters)
  return df

data = extract_early_adopters(tweets)
data.to_excel(r'filename.xlsx')

#Growth Rate Features
print(f"number of early adopters: {len(set(data['user_id']))}")
print(f"number of early tweets: {len(data['user_id'])}")


time = list(data['created_at_seconds'])
#avarage duartion time
dif_cons_time = abs(time[0]-time[-1])
dif_cons_time


#difference between consecutive tweets
dif_cons_time = time[0]-time[-1] 
avg_time = dif_cons_time/len(time)-1
print(f"avg of duration time: {int(round(avg_time,0))}")


#coefficient of variation
for i in range(len(time)-1):
  sd_time = math.sqrt((dif_cons_time - avg_time)**2/(len(time)-2))

cv_time = sd_time/avg_time
print(f"CV of step time: {round(cv_time,2)}")

early_adopters = random.sample(data['user_id'], k=5)
early_adopters

users_follower = [] # list of every followers from early adopters 
follower_list = [] # list of pairs of users (early_apdoter, follower)

for usr in early_adopters:
  try:
    for user in tweepy.Cursor(api.followers, user_id = usr).items(3):
      if user.id not in early_adopters:
        users_follower.append(user.id_str)
        follower_list.append((usr,user.id_str))
  except:
    continue


users_follower_S1 = random.choices(users_follower, k=3) # sample of user from the first surface follower_list_search
follower_list_1 = []  #list of pair of followers of followers 
s2_follower_list = [] # list of pairs of users (early_apdoter, follower) 

for usr_s1 in users_follower_S1:
  try:
    for user in tweepy.Cursor(api.followers, user_id = usr_s1).items(3):
      if user.id_str not in follower_list and usr_s1 not in early_adopters:
        follower_list_1.append(user.id_str)
        s2_follower_list.append((usr_s1, user.id_str))
  except:
    continue


users_follower_S2 = random.choices(follower_list_1, k=3) # Repeat the same process above but for the second surface 
follower_list_2 = []
s3_follower_list = [] 

for usr_s2 in users_follower_S2:
  try:
    for user in tweepy.Cursor(api.followers, user_id = usr_s2).items(3):
      if user.id_str not in follower_list and usr_s2 not in early_adopters:
        follower_list_2.append(user.id_str)
        s3_follower_list.append((usr_s2, user.id_str))
  except:
    continue


users_follower_S3 = random.choices(follower_list_2, k=3) # Repeat the same process above but for the second surface 
follower_list_3 = []
s4_follower_list = [] 

for usr_s3 in users_follower_S3:
  try:
    for user in tweepy.Cursor(api.followers, user_id = usr_s3).items(3):
      if user.id_str not in follower_list and usr_s3 not in early_adopters:
        follower_list_3.append(user.id_str)
        s4_follower_list.append((usr_s3, user.id_str))
  except:
    continue

pair_users = follower_list + s2_follower_list + s3_follower_list + s4_follower_list

#save the pair_user gathered in four surfaces.
with open('filename.json', 'w') as f:
    json.dump(pair_users,f)

#merge all the pairs_user files
result = []
for f in glob.glob("*.json"):
  with open(f, ) as infile:
      result.append(json.load(infile))

with open("merged_file.json", "wb") as outfile:
     json.dump(result, outfile)
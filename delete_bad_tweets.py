
import os
import json
import re
import pandas as pd
import time


# get df of all tweets ever

ls = []
i = 0
path = 'tweets2/tweet.js'
tweet_lists = []

with open(path) as data_file:
    data_str = data_file.read()

    first_data_line = re.match(r'window.YTD.tweet.part0 =', data_str).group(0)
    data_str = re.sub(first_data_line, '', data_str)
    data = json.loads(data_str)

    i = 0
    while i < len(data):
        format_tweets = [data[i]['id_str'], data[i]['full_text'],str(data[i]['id']), str(data[i]['created_at'])]
        tweet_lists.append(format_tweets)
        i = i + 1

tweets_df = pd.DataFrame( tweet_lists, columns=['id_str','text','id','created_at'])


#get index of bad tweets
from bad_words import must_remove
bad = []
for word in must_remove:
    my_regex = r"\b" + word + r"\b"

    x = tweets_df.index[tweets_df.text.str.contains(my_regex, case=False)].tolist()
    for num in x:
        bad.append(num)


#get the id of the bad tweets
bad_tweet_id = []
for num in bad:
    print(tweets_df.iloc[num]['text'])
    bad_tweet_id.append(tweets_df.iloc[num]['id'])


bad_tweet_df = tweets_df.ix[x]

##### Automate Deletion

import tweepy
import auth_info
from tweepy import OAuthHandler

###sign into twitter

consumer_key = auth_info.ckey
consumer_secret = auth_info.csecret
access_token = auth_info.atoken
access_secret = auth_info.asecret

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)


#see who is signed in
user = api.me()
print('Name: ' + user.name)
print('Location: ' + user.location)
print('Friends: ' + str(user.friends_count))


# delete the bad tweets
for bad_tweet in bad_tweet_id:
    try:
        print('Deleting tweet ID: %s ' % bad_tweet)
        api.destroy_status(bad_tweet)
        time.sleep(5)
    except:
        print('ID: %s  not found/error deleting' % bad_tweet)
        time.sleep(5)

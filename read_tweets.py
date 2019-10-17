import pandas as pd
import re
import json
from datetime import datetime

def get_date(s):
    try:

        date = s.replace('+0000 ','')
        date = (datetime.strptime(date, '%a %b %d %M:%S:%f %Y')).strftime('%m/%d/%Y')
    except:
        date = 'None'
    return date



def tweets_to_df(file):
    # get df of all tweets ever
    ls = []
    i = 0
    path = file #'tweets2/tweet.js'
    tweet_lists = []

    with open(path) as data_file:
        data_str = data_file.read()

        first_data_line = re.match(r'window.YTD.tweet.part0 =', data_str).group(0)
        data_str = re.sub(first_data_line, '', data_str)
        data = json.loads(data_str)

        i = 0
        while i < len(data):
            format_tweets = [data[i]['id_str'], data[i]['full_text'], \
                             str(data[i]['id']), str(data[i]['created_at']),
                             str(data[i]['favorite_count']), str(data[i]['retweet_count'])]
            tweet_lists.append(format_tweets)
            i = i + 1

    tweets_df = pd.DataFrame(tweet_lists, columns=['id_str', 'text', 'id', 'created_at', 'favorites', 'retweets'])
    tweets_df['date'] = tweets_df['created_at'].apply(get_date)


    return tweets_df


file = tweets_to_df('tweets2/tweet.js')



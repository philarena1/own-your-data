import time
from read_tweets import tweets_to_df
import tweepy
import auth_info
from tweepy import OAuthHandler

def main():

    tweets_df = tweets_to_df('tweets2/tweet.js')

    start_date = '2009-01-01'
    end_date = '2013-01-02'
    tweet_date = (tweets_df['date'] > start_date) & (tweets_df['date'] <= end_date)

    bad = tweets_df.loc[tweet_date]

    #get the id of the bad tweets
    bad_tweet_id = []
    for index, row in bad.iterrows():
        print(tweets_df.iloc[index]['text'])
        bad_tweet_id.append(tweets_df.iloc[index]['id'])


    ##### Automate Deletion

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


    deletion = input('do you wnat to delete these? \ny or n')
    # delete the bad tweets
    if deletion == 'y':
        for bad_tweet in bad_tweet_id:
            try:
                print('Deleting tweet ID: %s ' % bad_tweet)
                api.destroy_status(bad_tweet)
                time.sleep(5)
            except:
                print('ID: %s  not found/error deleting' % bad_tweet)
                time.sleep(5)


if __name__ == '__main__':
    main()
import time
from read_tweets import tweets_to_df
import tweepy
import auth_info
from tweepy import OAuthHandler

def main():

    tweets_df = tweets_to_df('tweets2/tweet.js')

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


    deletion = input('do you wnat to delete these?')
    # delete the bad tweets
    if deletion == 'yes':
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
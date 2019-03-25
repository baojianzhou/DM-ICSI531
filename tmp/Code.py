# -*- coding: utf-8 -*-

import twitter
import json
import pandas as pd
import os

def twitter_setup():
    Consumer_key = 'VhCAlAT8IXsXdC5ShCSja33SC'
    Consumer_secret = 'H18DIfFBMBGo2lUvkXbQN9YDMoyeUOqMblXhFoEJibeAED3rr8'
    Access_token = '1092499632284991488-7RqorqCE77vuTNFIlTv8NCsEd9eKTX'
    Access_token_secret = '7l9BQ4lkL307xEuKA4rdHrCcbKZnkTdjEFa7rVWiCPyMW'
    api = twitter.Api(Consumer_key, Consumer_secret, Access_token, Access_token_secret)
    return api

def M_dash():
    myAPI = twitter_setup()
    tweets = myAPI.GetSearch(term="road OR highway OR congestion OR crash OR wreck OR collision OR street OR lane OR traffic OR accident", geocode=[37.781157, -122.398720, "1mi"],count=200)
    print(len(tweets))
    text = []
    tweet_id = []
    user_id = []
    matching = []
    search = ('road','highway','congestion','crash','wreck','collision','street','lane','traffic','accident')
    for tweet in tweets:
        tweet = json.loads(str(tweet))
        text.append(tweet['text'])
        tweet_id.append(tweet['id'])
        user_id.append((tweet['user']['id']))
        if any(s in tweet['text'].lower() for s in search):
            matching.append(1)
        else:
            matching.append(0)
    df = pd.DataFrame(data={"tweet_id": tweet_id, "user_id": user_id, "tweet": text, "matching": matching})
    df["user_id"] = pd.to_numeric(df["user_id"])
    df["tweet_id"] = pd.to_numeric(df["tweet_id"])
    df["matching"] = pd.to_numeric(df["matching"])
    df.to_csv(os.getcwd()+"/M.csv", header=True,mode = 'w', index=False, encoding='utf-8')
    print(df)

    user_tweets = []
    user_id2 = []
    tweet_id2 = []
    matching2 = []
    for id in user_id:
        utweets = myAPI.GetUserTimeline(user_id=id,count=5,max_id=None)
        for tweet in utweets:
            tweet = json.loads(str(tweet))
            user_tweets.append(tweet['text'])
            user_id2.append(tweet['user']['id'])
            tweet_id2.append(tweet['id'])
            if any(s in tweet['text'].lower() for s in search):
                matching2.append(1)
            else:
                matching2.append(0)
    df2 = pd.DataFrame(data={"tweet_id": tweet_id2, "user_id": user_id2, "tweet": user_tweets,  "matching": matching2})
    df2["user_id"] = pd.to_numeric(df2["user_id"])
    df2["tweet_id"] = pd.to_numeric(df2["tweet_id"])
    df2["matching"] = pd.to_numeric(df2["matching"])
    df2.to_csv(os.getcwd() + "/D_dash.csv", header=True,mode = 'w', index=False, encoding='utf-8')
    print(df2)
    count = 0

    for t1 in tweet_id2:
        for t2 in tweet_id:
           if t1 == t2:
               count = count+1

    intersected_df = pd.merge(df, df2, how='inner')
    intersected_df.to_csv(os.getcwd() + "/M_dash.csv", header=True, mode='w', index=False, encoding='utf-8')

    print(intersected_df)

    print('tweets in D_dash and M_dash {}'.format(count))
    print('Matching tweets in M_dash = {}'.format(sum(matching)))
    print('Matching tweets in D_dash = {}'.format(sum(matching2)))

def main():
    M_dash()

if __name__ == '__main__':
    main()
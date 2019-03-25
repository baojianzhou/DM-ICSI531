# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 15:47:47 2014

@author: Feng Chen
"""

import twitter, sys, json

reload(sys)
sys.setdefaultencoding("utf-8")

myApi = twitter.Api(consumer_key='PeH7lROp4ihy4QyK87FZg', \
                    consumer_secret='1BdUkBd9cQK6JcJPll7CkDPbfWEiOyBqqL2KKwT3Og', \
                    access_token_key='1683902912-j3558MXwXJ3uHIuZw8eRfolbEGrzN1zQO6UThc7', \
                    access_token_secret='e286LQQTtkPhzmsEMnq679m7seqH4ofTDqeArDEgtXw')


def print_info(tweet):
    print '***************************'
    print 'Tweet ID: ', tweet['id']
    print 'Post Time: ', tweet['created_at']
    print 'User Name: ', tweet['user']['screen_name']
    try:
        print 'Tweet Text: ', tweet['text']
    except:
        pass


def rest_query_ex1():
    geo = [37.781157, -122.398720, "1mi"]
    raw_tweets = myApi.GetSearch(term="iphone", geocode=geo)

    for raw_tweet in raw_tweets:
        tweet = json.loads(str(raw_tweet))
        print_info(tweet)
    print len(raw_tweets)


def rest_query_ex2():
    query = 'playstation'
    geo = [37.781157, -122.398720, "1mi"]  # City of Albany
    raw_tweets = myApi.GetSearch(query, geo)
    for raw_tweet in raw_tweets:
        #        print raw_tweet
        tweet = json.loads(str(raw_tweet))
        print_info(tweet)


def rest_query_ex3():
    query = 'road OR highway OR street OR lane OR traffic OR car OR vehicle OR bus'
    geo = ('42.6525', '-73.7572', '150mi')  # City of Albany
    MAX_ID = None
    for it in range(2):  # Retrieve up to 200 tweets
        tweets = [json.loads(str(raw_tweet)) for raw_tweet \
                  in myApi.GetSearch(query, geo, count=100, max_id=MAX_ID, result_type='recent')]
        if tweets:
            MAX_ID = tweets[-1]['id']
            print MAX_ID, len(tweets)


def main():
    # print "\n\n\n************ rest_query_ex1() ****************\n"
    # rest_query_ex1()

    print "\n\n\n************ rest_query_ex2() ****************\n"
    rest_query_ex1()

    # print "\n\n\n************ rest_query_ex3() ****************\n"
    # rest_query_ex3()
    # pass


if __name__ == '__main__':
    main()

"""
Without filtering on location, retrieve tweets that contain the phrase 'road accident'. 
Note that if the query is 'road accident' instead of '"road accident"', then the 
returned queries will match both 'road' and 'accident' but not the phase "road accident"
"""
"""
Retrieve tweets that are related to traffic congestions in the city of Albany 
"""
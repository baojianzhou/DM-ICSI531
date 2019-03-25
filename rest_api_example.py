# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 15:47:47 2014

Updated at Sun. Feb 24 --:--:-- 2019

@author: Feng Chen, Baojian Zhou
"""
import json
import twitter

# TODO You need to register a Twitter developer account and go to https://apps.twitter.com to create an app
consumer_api_key = 'kr7l0LXZBRcnVaQI5412v6Yse'  # replace your own key here
consumer_api_secret = '7A7p9iE68zc3a3emvVEcd9kGRdgHUsrqh4OWx9qkJnC1SsMJ4a'  # replace your own key secret here
access_token_key = '2784122806-JkJKznO9BIEqxIFut7VAmLXDmamRdX6PfYnlixP'  # replace your own access token here
access_token_secret = '8DvNK1c6vdAV3eOmADGnUjxodIwHitVkQao7N2nsKK7U6'  # replace your own access secret here.


myApi = twitter.Api(consumer_key=consumer_api_key, consumer_secret=consumer_api_secret,
                    access_token_key=access_token_key, access_token_secret=access_token_secret)


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
    geo = [37.781157, -122.398720, "10mi"]
    raw_tweets = myApi.GetSearch(term="iphone", geocode=geo)

    for raw_tweet in raw_tweets:
        tweet = json.loads(str(raw_tweet))
        print_info(tweet)
    print len(raw_tweets)


def rest_query_ex2():
    query = u'road traffic car'
    geo = [37.781157, -122.398720, u"10mi"]  # City of Albany
    raw_tweets = myApi.GetSearch(term=query, geocode=geo)
    for raw_tweet in raw_tweets:
        #        print raw_tweet
        tweet = json.loads(str(raw_tweet))
        print_info(tweet)


def rest_query_ex3():
    query = 'road OR highway OR street OR lane OR traffic OR car OR vehicle OR bus'
    geo = ('40.730610', '-73.935242', '150mi')  # New York City
    max_id = None
    for it in range(2):  # Retrieve up to 200 tweets
        tweets = [json.loads(str(raw_tweet)) for raw_tweet
                  in myApi.GetSearch(term=query, geocode=geo, count=100, max_id=max_id, result_type='recent')]
        if tweets:
            for tweet in tweets:
                print(tweet)
            max_id = tweets[-1]['id']
            print max_id, len(tweets)


def main():
    print "\n\n\n************ rest_query_ex1() ****************\n"
    rest_query_ex1()
    print "\n\n\n************ rest_query_ex2() ****************\n"
    rest_query_ex2()
    print "\n\n\n************ rest_query_ex3() ****************\n"
    rest_query_ex3()


"""
Without filtering on location, retrieve tweets that contain the phrase 'road accident'. 
Note that if the query is 'road accident' instead of '"road accident"', then the 
returned queries will match both 'road' and 'accident' but not the phase "road accident"
"""
"""
Retrieve tweets that are related to traffic congestion in the city of Albany 
"""

if __name__ == '__main__':
    main()

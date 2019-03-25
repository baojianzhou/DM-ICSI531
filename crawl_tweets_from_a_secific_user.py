# -*- coding: utf-8 -*-
"""
@author: Huixian
"""
import sys, twitter, operator
from dateutil.parser import parse
import json
import os

out_folder = ""

list_users = ['@st_louis_news']
api = twitter.Api(consumer_key='PeH7lROp4ihy4QyK87FZg',
                  consumer_secret='1BdUkBd9cQK6JcJPll7CkDPbfWEiOyBqqL2KKwT3Og',
                  access_token_key='1683902912-j3558MXwXJ3uHIuZw8eRfolbEGrzN1zQO6UThc7',
                  access_token_secret='e286LQQTtkPhzmsEMnq679m7seqH4ofTDqeArDEgtXw')


def fetch_historical(user):
    """
    fetch all tweets of a single user
    :param user:
    :return:
    """
    data = {}
    max_id = None
    total = 0
    while True:
        statuses = api.GetUserTimeline(screen_name=user, count=200, max_id=max_id)
        newCount = ignCount = 0
        for s in statuses:
            if s.id in data:
                ignCount += 1
            else:
                data[s.id] = s
                newCount += 1
        total += newCount
        print >> sys.stderr, "Fetched %d/%d/%d new/old/total." % (
            newCount, ignCount, total)
        if newCount == 0:
            break
        max_id = min([s.id for s in statuses]) - 1
    return data.values()


"""
fetch tweets whose id is bigger than specific id
"""


def fetch_today(user):
    data = {}
    max_id = None
    total = 0
    last_id = get_last_id(user)
    while True:
        statuses = api.GetUserTimeline(screen_name=user, count=200, max_id=max_id, since_id=last_id)
        newCount = ignCount = 0
        for s in statuses:
            if s.id in data:
                ignCount += 1
            else:
                data[s.id] = s
                newCount += 1
        total += newCount
        print >> sys.stderr, "Fetched %d/%d/%d new/old/total." % (
            newCount, ignCount, total)
        if newCount == 0:
            break
        max_id = min([s.id for s in statuses]) - 1
    return data.values()


def get_last_id(user):
    fname = '%s.txt' % user
    fname = os.path.join(out_folder, fname)
    f = open(fname, 'r')
    last_line = f.readlines()[-1]
    tweet = json.loads(last_line)
    f.close()
    return tweet['id']


def txtPrint(user, tweets, out_folder):
    for t in tweets:
        t.pdate = parse(t.created_at)
        print json.loads(str(t))['text']
    key = operator.attrgetter('pdate')
    tweets = sorted(tweets, key=key)
    keytweets = [json.loads(str(rawtweet)) for rawtweet in tweets]
    fname = '%s.txt' % user
    fname = os.path.join(out_folder, fname)
    f = open(fname, 'a+')
    for tweet in keytweets:
        f.write(json.dumps(tweet) + '\n')
    f.close()


def crawl_users_historical_tweets(list_users, out_folder):
    for user in list_users:
        data = fetch_historical(user)
        txtPrint(user, data, out_folder)


def crawl_most_recent_tweets(list_users, out_folder):
    for user in list_users:
        data = fetch_today(user)
        txtPrint(user, data, out_folder)


def main():
    crawl_users_historical_tweets(list_users, out_folder)

    crawl_most_recent_tweets(list_users, out_folder)


if __name__ == '__main__':
    main()

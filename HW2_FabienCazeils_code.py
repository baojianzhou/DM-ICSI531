import re
import tweepy
import datetime
import json
import os
from pattern.en import sentiment
import datetime
import sys, twitter, operator
from dateutil.parser import parse

# stream.filter(locations=[-73.859915,42.630355,-73.735632,42.693976 ]) # City of

if False:
    OAuth = tweepy.OAuthHandler('GHzCdYMAs2fy1VjsGcP5rwYiG', 'aT3Ti5OFVZZSDtu4Ymp1qMbWZ31TaJFtULLSFyo6xYXSS1gKu7')
    OAuth.set_access_token('2784122806-LfJbvTHuS5g2cK7mUTUfKIzLlSWt1mqXq7sQYxL',
                       'eIqqhDzhDNe9uTeKmzRBcExFI7ALa0MYFx7ufv1XF7Xkl')

OAuth = tweepy.OAuthHandler('kr7l0LXZBRcnVaQI5412v6Yse', '7A7p9iE68zc3a3emvVEcd9kGRdgHUsrqh4OWx9qkJnC1SsMJ4a')
OAuth.set_access_token('2784122806-JkJKznO9BIEqxIFut7VAmLXDmamRdX6PfYnlixP',
                           '8DvNK1c6vdAV3eOmADGnUjxodIwHitVkQao7N2nsKK7U6')

if False:
    api = twitter.Api(consumer_key='GHzCdYMAs2fy1VjsGcP5rwYiG',
                      consumer_secret='aT3Ti5OFVZZSDtu4Ymp1qMbWZ31TaJFtULLSFyo6xYXSS1gKu7',
                      access_token_key='2784122806-LfJbvTHuS5g2cK7mUTUfKIzLlSWt1mqXq7sQYxL',
                      access_token_secret='eIqqhDzhDNe9uTeKmzRBcExFI7ALa0MYFx7ufv1XF7Xkl')
    # print jdata
    AandM = classifyThem_M_tweets(output_file, output_folder_date)
    tw_dict = timelineGetter(AandM['U'], output_folder_date)
    BCDN_dicts = n_or_d(tw_dict, output_folder_date, self.things)
    print"api recall: ", AandM['sizeM'], "\\", BCDN_dicts['sizeN'], "\nquality precision: ", AandM['sizeA'], "\\", \
        AandM['sizeM'], "\nquality recall: ", AandM['sizeA'], "\\", (AandM['sizeA'] + BCDN_dicts['sizeC'])


class StreamListener(tweepy.StreamListener):
    things = ['nutrition', 'health', 'vegan', 'daily dozen', 'whole foods plant based']

    streamed_usr_ids = []

    def on_data(self, raw_data):
        # on_error(self)
        print('test on data ....')
        output_folder_date = 'data/{0}'.format(datetime.datetime.now().strftime('%Y_%m_%d'))

        if not os.path.exists(output_folder_date):
            os.makedirs(output_folder_date)

        output_file = output_folder_date + '/data.txt'
        try:
            jdata = json.loads(str(raw_data))
            print jdata['text']
            f = open(output_file, 'a+')
            f.write(json.dumps(jdata) + '\n')
            f.close()
        except:
            print 'Data writting exception.'

    def on_error(self, status):

        if status == 304:
            print"304: There was no new data to return"
        elif status == 401:
            print"401: Missing or incorrect authentication credentials"
        elif status == 403:
            print"403: The request is understood, but it has been refused or access is not allowed"
        elif status == 404:
            print"404:Not Found"
        elif status == 406:
            print"406: Invalid format is specified in the request"
        elif status == 420:
            print"420: Rate limit reached"
        elif status == 429:
            print"429: Too Many Requests"
        # print(status)
        return False


# def classifyThem_M_tweets(the_data, whereToPutIt):

def classifyThem_M_tweets(inputfile, destination_dir):
    streamed_usr_ids = []
    cnt = 0

    tweets_in_A = []
    tweets_in_M = []
    Aoutput_file = destination_dir + "/pos_tweets_inM.txt"
    Moutput_file = destination_dir + "/tweets_inM.txt"
    user_id_file = destination_dir + "/userppl.txt"

    print Aoutput_file
    print Moutput_file

    with open(inputfile, 'r') as f:

        for tweet in f:
            tw = json.loads(tweet)
            cnt += 1

            # if any(s in tw["text"] for s in ['nutrition', 'fitness', 'health']):
            print sentiment(tw["text"], threshold=0.1)
            if sentiment(tw["text"], threshold=0.1)[0] > 0:
                # print"p"
                streamed_usr_ids.append(tw["user"]["id"])
                tupl = "({0},T,T)".format(tw["id"])
                tweets_in_A.append(tupl)
                tweets_in_M.append(tupl)
            else:
                # print"n"
                streamed_usr_ids.append(tw["user"]["id"])
                tupl = "({0},T,F)".format(tw["id"])
                tweets_in_M.append(tupl)
    print "tweets_in_A: ", len(tweets_in_A), "\n", "tweets_in_M: ", len(tweets_in_M), "\n streamed_usr_ids:", len(
        streamed_usr_ids), "\n TOTAL:", cnt

    with open(Aoutput_file, "a+") as A, open(Moutput_file, "a+") as M:
        A.write(json.dumps(str(tweets_in_A)))
        M.write(json.dumps(str(tweets_in_M)))

    # ret_files={'A':Aoutput_file, 'M':Moutput_file}

    sizeA = len(tweets_in_A)
    sizeM = len(tweets_in_M)

    return {'A': Aoutput_file, 'M': Moutput_file, 'U': user_id_file, 'sizeA': sizeA, 'sizeM': sizeM}


#########


def timelineGetter(userID_file, destination_dir):
    output_file = destination_dir + "/User_timeline_tweets"
    tweet_dict = {}

    with open(userID_file, "r") as inpt, open(output_file, "a+") as outp:
        for pers_id in json.load(inpt):
            #			tweets=twitter.Api.GetUserTimeline(user_id=pers_id, count=200)
            tweets = api.GetUserTimeline(user_id=pers_id, count=200)
            for tw in tweets:
                if tw not in tweet_dict:
                    tweet_dict[tw.id] = tw
        json.dump(tweet_dict, outp)
    return tweet_dict


def n_or_d(dict_from_timeline, destination_dir, things):
    output_N = destination_dir + "/setN"
    output_B = destination_dir + "/setB"
    output_D = destination_dir + "/setD"
    output_C = destination_dir + "/setC"

    tweets_in_B = []
    tweets_in_N = []
    tweets_in_C = []
    tweets_in_D = []

    with open(output_N, "a+") as N, open(output_B, "a+") as B, open(output_D, "a+") as D, open(output_C, "a+") as C:
        for val in dict_from_timeline.values():
            if sentiment(val["text"], threshold=0.1)[0] > 0:
                if any(query_word in val["text"] for query_word in things):
                    tupl = "({0},T,T)".format(val["id"])
                    tweets_in_B.append(tupl)
                    tweets_in_N.append(tupl)
                    tweets_in_C.append(tupl)
                    tweets_in_D.append(tupl)
                else:
                    tupl = "({0},F,T)".format(val["id"])
                    tweets_in_C.append(tupl)
                    tweets_in_D.append(tupl)

            else:
                if any(query_word in val["text"] for query_word in things):
                    tupl = "({0},T,F)".format(val["id"])
                    tweets_in_N.append(tupl)
                    tweets_in_D.append(tupl)
                else:
                    tupl = "({0},F,F)".format(val["id"])
                    tweets_in_D.append(tupl)
        B.write(json.dumps(str(tweets_in_B)))
        C.write(json.dumps(str(tweets_in_C)))
        N.write(json.dumps(str(tweets_in_N)))
        D.write(json.dumps(str(tweets_in_D)))

    sizeB = len(tweets_in_B)
    sizeN = len(tweets_in_N)
    sizeC = len(tweets_in_C)
    sizeD = len(tweets_in_D)
    return {'N': output_N, 'B': output_B, 'D': output_D, 'C': output_C, 'sizeB': sizeB, 'sizeN': sizeN, 'sizeC': sizeC,
            'sizeD': sizeD}


def main():
    things = ['nutrition', 'health', 'vegan', 'daily', 'dozen', 'whole', 'foods', 'plant', 'based']
    things2 = ['nutrition', 'fitness', 'health']
    while True:
        sl = StreamListener()
        stream = tweepy.Stream(OAuth, sl)
        try:
            # stream.filter(track=things2, locations=[-73.859915,42.630355,-73.735632,42.693976 ])
            # 40.730610,-73.935242, 40.761407, -73.980049
            stream.filter(track=things, locations=[-73.980049, 40.730610, -73.935242, 40.761407, ])
        except:
            print 'Something went wrong. Have you tried turning you computer off and back on?'


if __name__ == '__main__':
    main()

# (40.730610,-73.935242, 40.761407, -73.980049)


# stream.filter(track=things,locations=[-73.859915,42.630355,-73.735632,42.693976 ])

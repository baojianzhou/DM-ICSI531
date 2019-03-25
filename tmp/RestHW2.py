import re
import tweepy
import datetime
import json
import os
from pattern.en import sentiment
import datetime
import sys, twitter, operator
from dateutil.parser import parse




api = twitter.Api(consumer_key='GHzCdYMAs2fy1VjsGcP5rwYiG',
                      consumer_secret='aT3Ti5OFVZZSDtu4Ymp1qMbWZ31TaJFtULLSFyo6xYXSS1gKu7',
                      access_token_key='2784122806-LfJbvTHuS5g2cK7mUTUfKIzLlSWt1mqXq7sQYxL',
                      access_token_secret='eIqqhDzhDNe9uTeKmzRBcExFI7ALa0MYFx7ufv1XF7Xkl')


'''
changer ex2
mettre dans des fichier
passer fichier aux foncction en dessous
'''



def rest_query_for_M():
    output_folder_date = 'data/{0}'.format(datetime.datetime.now().strftime('%Y_%m_%d'))

    if not os.path.exists(output_folder_date):
        os.makedirs(output_folder_date)

    output_file = output_folder_date + '/data.txt'

    with open(output_file, 'a+') as f:

        query = "vegan OR health OR diet"
        geo = [40.730610, -73.935242, "5mi"] # City of NY
        for i in range(2):
            raw_tweets = api.GetSearch(term=query, geocode=geo, count=50)
            for tw in raw_tweets:
                #        print raw_tweet
                tweet = json.loads(str(tw))
                #print_info(tweet)
                json.dump(tweet, f)
    return {'f': output_file, 'dir': output_folder_date}

#40.730610,-73.935242



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
                twee=json.loads(tw)
                if twee not in tweet_dict:
                    tweet_dict[twee['id']] = twee
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
    query_words=['vegan', 'health', 'diet']
    m_query=rest_query_for_M()
    a_and_m=classifyThem_M_tweets(m_query['f'], m_query['dir'])
    d_query=timelineGetter(a_and_m["U"], m_query['dir'])
    b_n_d_csets=n_or_d(d_query,  m_query['dir'], query_words)

    print"api recall: ", a_and_m['sizeM'], "\\", b_n_d_csets['sizeN'], "\nquality precision: ", a_and_m['sizeA'], "\\", \
        a_and_m['sizeM'], "\nquality recall: ", a_and_m['sizeA'], "\\", (a_and_m['sizeA'] + b_n_d_csets['sizeC'])

if __name__ == '__main__':
    main()

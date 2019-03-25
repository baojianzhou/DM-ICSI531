'''
 This codes crawls the tweets in SanFrancisco area from Twitter.

 Jan 11, 2014
 Feng Chen
'''

import tweepy  # twitter api module - python version
import datetime  # python datetime module
import json  # python json module
import os  # python os module, used for creating folders

OAuth = tweepy.OAuthHandler('PeH7lROp4ihy4QyK87FZg', '1BdUkBd9cQK6JcJPll7CkDPbfWEiOyBqqL2KKwT3Og')
OAuth.set_access_token('1683902912-j3558MXwXJ3uHIuZw8eRfolbEGrzN1zQO6UThc7',
                       'e286LQQTtkPhzmsEMnq679m7seqH4ofTDqeArDEgtXw')


class StreamListener(tweepy.StreamListener):
    def on_data(self, raw_data):
        output_folder_date = 'data/{0}'.format(datetime.datetime.now().strftime('%Y_%m_%d'))
        if not os.path.exists(output_folder_date): os.makedirs(output_folder_date)
        output_file = output_folder_date + '/WashingtonDC.txt'
        try:
            jdata = json.loads(str(raw_data))
            print jdata['text']
            f = open(output_file, 'a+')
            f.write(json.dumps(jdata) + '\n')
            f.close()
        except:
            print 'Data writting exception.'


def main():
    try:
        sl = StreamListener()
        stream = tweepy.Stream(OAuth, sl)
        stream.filter(locations=[-73.859915, 42.630355, -73.735632, 42.693976])  # City of Albany
    except:
        print 'Exception occur!'


if __name__ == '__main__':
    main()

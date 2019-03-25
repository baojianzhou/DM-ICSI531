'''
 This codes crawls the tweets in SanFrancisco area from Twitter.

 Jan 11, 2014 / updated at: Feb. 24. 2019
 Feng Chen, Baojian Zhou
'''

import tweepy  # twitter api module - python version
import datetime  # python datetime module
import json  # python json module
import os  # python os module, used for creating folders

# TODO You need to register a Twitter developer account and go to https://apps.twitter.com to create an app
OAuth = tweepy.OAuthHandler('kr7l0LXZBRcnVaQI5412v6Yse', '7A7p9iE68zc3a3emvVEcd9kGRdgHUsrqh4OWx9qkJnC1SsMJ4a')
OAuth.set_access_token('2784122806-JkJKznO9BIEqxIFut7VAmLXDmamRdX6PfYnlixP',
                       '8DvNK1c6vdAV3eOmADGnUjxodIwHitVkQao7N2nsKK7U6')


class StreamListener(tweepy.StreamListener):
    def on_data(self, raw_data):
        output_folder_date = 'data/{0}'.format(datetime.datetime.now().strftime('%Y_%m_%d'))
        if not os.path.exists(output_folder_date): os.makedirs(output_folder_date)
        output_file = output_folder_date + '/data.txt'
        try:
            jdata = json.loads(str(raw_data))
            print jdata['text']
            f = open(output_file, 'a+')
            f.write(json.dumps(jdata) + '\n')
            f.close()
        except:
            print 'Data writting exception.'


def main():
    while True:
        sl = StreamListener()
        stream = tweepy.Stream(OAuth, sl)
        try:
            stream.filter(track=['nutrition', 'fitness', 'health'])
        except:
            print 'Exception occur!'


if __name__ == '__main__':
    main()
# tweetfind.py

import json
import urllib2
import oauth2
import time
from datetime import datetime, timedelta

# Secret keys for twitter authorization
consumer_key = "2NMTm5v6eBfjtDSjfgCSnQ"
consumer_secret = "9TKDdOJtIexc88zpJCFFoi1HojtcLXSG8lwp3qkrE"
access_key = "364678738-5M9uhkAtVgLoyCiSN3eg4ZvMe85KXShy6TgyWOQB"
access_secret = "tfigAqZQ4eYLN1rqoKvtcORS4i2KDCer34VejgQhM"


class Finder:

    def __init__(self, consumer_key, consumer_secret, access_key,
                 access_secret):
        self.json_tweets = []
        self.search_options = "&rpp=100"
        self.page_index = 1

        self._debug_level = 0;

        # setup oauth stuff
        self.oauth_token = oauth2.Token(key = access_key,
                                        secret = access_secret)
        self.oauth_consumer = oauth2.Consumer(key = consumer_key,
                                              secret = consumer_secret)
        self.signature_method_hmac_sha1 = oauth2.SignatureMethod_HMAC_SHA1()

        # setup http stuff
        self.http_handler = urllib2.HTTPHandler(debuglevel = self._debug_level)
        self.https_handler = urllib2.HTTPSHandler(debuglevel = \
                                                  self._debug_level)
        self.http_method = "GET"
        

    def find_tweets(self, search_string):
        tweets = []
        json_response = self._get_json_tweets(search_string)
        self.json_tweets = [json_response["results"]]
        for tweet in json_response["results"]:
            tweets.append(tweet)
        while (json_response["results"] != []):
            time.sleep(1)
            self.page_index += 1
            json_response = self._get_json_tweets(search_string)
            self.json_tweets.append(json_response["results"])
            for tweet in json_response["results"]:
                tweets.append(tweet)
            if (self.page_index > 100):
                break
        self.json_tweets.pop(-1)
        self.page_index = 1
        for i in range(len(tweets)):
            self._format_tweet(tweets[i])
        return tweets


    def find_users(self, search_string):
        users = []
        json_response = self._get_json_users(search_string)
        print(json_response[0].keys())
        self.json_users = json_response
        while (json_response != []):
            time.sleep(1)
            self.page_index += 1
            json_response = self._get_json_users(search_string)
            self.json_users += json_response
            if (self.page_index > 100):
                break
        self.page_index = 1
        return self.json_users

    def _twitter_req(self, url, method, parameters):
        req = oauth2.Request.from_consumer_and_token(self.oauth_consumer,
                                                     token = self.oauth_token,
                                                     http_method = \
                                                     self.http_method,
                                                     http_url = url,
                                                     parameters = parameters)
        req.sign_request(self.signature_method_hmac_sha1, self.oauth_consumer,
                         self.oauth_token)
        headers = req.to_header()

        if (self.http_method == "POST"):
            encoded_post_data = req.to_postdata()
        else:
            encoded_post_data = None
            url = req.to_url()

        opener = urllib2.OpenerDirector()
        opener.add_handler(self.http_handler)
        opener.add_handler(self.https_handler)

        response = opener.open(url, encoded_post_data)

        return response

        
    def _get_json_tweets(self, search_string):
        response = self._twitter_req("http://search.twitter.com/search.json?q=" +
                                     search_string + self.search_options +
                                     "&page=" + str(self.page_index), "GET",
                                     [])
        return json.load(response)


    def _get_json_users(self, search_string):
        response = self._twitter_req("https://api.twitter.com/1/users/search.json?q=" +
                                     search_string + self.search_options +
                                     "&page=" + str(self.page_index), "GET",
                                     [])
        return json.load(response)


    def _format_tweet(self, tweet):
        tweet["created_at"] = datetime.now().\
                              strptime(tweet["created_at"],
                                       '%a, %d %B %Y %H:%M:%S +0000')

if __name__ == '__main__':
    finder = Finder(consumer_key, consumer_secret, access_key, access_secret)
    search_string = "\"get dressed\" OR dressed OR \"put on clothes\" take OR takes \"so long\" OR forever"
    my_tweets = finder.find_tweets(search_string)

    time_diff = my_tweets[0]["created_at"]-my_tweets[-1]["created_at"]
    tweet_frequency = len(my_tweets)/time_diff.days
    print("Search string: " + search_string)
    print("Tweets per day: " + str(tweet_frequency) + "\n")

    user_list = [tweet["from_user"] for tweet in my_tweets]


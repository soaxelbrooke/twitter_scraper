# userfind.py
"""
This module is a tool for identifying Twitter users that match at least one
identifier.
"""
import tweetfind


# Secret keys for twitter authorization
consumer_key = "2NMTm5v6eBfjtDSjfgCSnQ"
consumer_secret = "9TKDdOJtIexc88zpJCFFoi1HojtcLXSG8lwp3qkrE"
access_key = "364678738-5M9uhkAtVgLoyCiSN3eg4ZvMe85KXShy6TgyWOQB"
access_secret = "tfigAqZQ4eYLN1rqoKvtcORS4i2KDCer34VejgQhM"


class UserFinder:

    def __init__(self, identifier_list):
        self.identifiers = identifier_list
        self.search_options = ''

    def find_users(self):
        finder = tweetfind.TweetFinder(consumer_key, consumer_secret, access_key, access_secret)

        finder.search_options += self.search_options
        user_dict = {}
#        for identifier in self.identifiers:
        identifier = self.identifiers[2]
        users = [u[u'id'] for u in finder.find_tweets(identifier)]
        
        for user in users:
            if user in user_dict.keys():
                user_dict[user].append(identifier)

            else:
                user_dict[user] = [identifier]

        return user_dict

    def set_search_options(search_options):
        self.search_options


print("Starting scrape..?")
if __name__ == "__main__":
    print("Starting scrape...")
    
    identifier_list = ['love buying OR "shopping for" clothes',
#                       '"john varvados" OR "seven for all mankind" OR levis OR chanel OR "gucci" OR "american apparel"',
                       'selfie',
                       'drinking OR drunk OR "hung over"',
                       'vintage',
                       'need OR love coffee']
    
    uf = UserFinder(identifier_list)
    users = uf.find_users()
    
    user_weights = {}
    for user in users:
        if len(users[user]) in user_weights:
            user_weights[len(users[user])] += 1

        else:
            user_weights[len(users[user])] = 1

    print("Complete!")
    print(user_weights)

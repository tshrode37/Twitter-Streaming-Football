import os
import tweepy

from tweepy import OAuthHandler 
from tweepy import Stream
from tweepy import StreamListener
from tweepy import API

from pymongo import MongoClient
import json

#create connection to MongoDB

client = MongoClient()
db = client['Superbowl_2021']
coll = db['Superbowl_post_game_tweets']

#Variables that contains the user credentials to access Twitter API (obtained from Twitter API)

c_key = os.environ.get('tw_consumer_key')
c_sec = os.environ.get('tw_consumer_secret')
atk = os.environ.get('tw_access_token')
ats = os.environ.get('tw_access_token_secret')

#create a class called MyListener that will listen for tweets from StreamListener
#then, we create UDF's to handle data and errors

class MyListener(StreamListener): 

    def on_data(self, data):
        msg = json.loads(data) # Create a message from json file
        if "text" in msg: 
            tweet = msg["text"]
            hashtags = msg["entities"]["hashtags"] 
            created = msg["created_at"]
            username = msg["user"]["screen_name"]
            retweeted = msg["retweeted"]
            user_tz = msg["user"]["time_zone"]
            user_location = msg["user"]["location"]
        #print(tweet.encode('utf-8')) # Print the message and UTF-8 coding will eliminate emojis
    
            coll.insert_one({'Date': created,
                    'User': username,
                    'Tweet': tweet,
                    'Retweeted': retweeted,
                    'Hashtags': hashtags,
                    'Time Zone': user_tz,
                    'Location': user_location}) #add collected data field to MongoDB
        return True

    def on_error(self, status):
        print(status.text)
        return True

#complete authorization and connect to Twitter Streaming API

if __name__ == '__main__':    
    listener = MyListener()
    
    auth = OAuthHandler(c_key, c_sec)
    auth.set_access_token(atk, ats)
    api = API(auth)

    twitterstream = Stream(auth=api.auth, listener=listener, tweet_mode="extended") 
    

    postgame_tags = ["Tom Brady", "Buccaneers", "Tampa Bay Buccaneers", "Superbowl",
           "Bucs", "SuperbowlLV", "Patrick Mahomes", "Kansas City Chiefs", 
                    "ChiefsKingdom", "BucsVsChiefs", "Chiefs"] #Winner of Game 1 and Game 2
    
    twitterstream.filter(track=postgame_tags, languages=["en"]) 




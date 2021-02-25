# Sentiment analysis and clustering football tweets obtained by live streaming twitter data
Data Science Practicum I Project - Using Sentiment Analysis and Clustering to Determine Superbowl Fan "Favorite"

## Summary

For this project, we will be creating a pipeline that live stream tweets with particular keywords relating to the teams that played in the NFL Conference Championships on 1/24/2021. The goal is to collect tweets during each NFL Conference Championship game (Kansas City vs Buffalo Bills, Tampa Bay Buccaneers vs Green Bay Packers) and after both  games have been completed. For this project, `game tweets` will refer to the tweets that were collected during each game, and `post-game tweets` will refer to the tweets collected after both games were completed Using this data, we seek to use sentiment analysis and text clustering to estimate the NFL team that is favored to win the Superbowl based on fans' analysis/comments/feelings. There are many aspects of sport games that cannot be captured by a box score such as a quarterback who can strategically mislead a defender to free up his receiver or a receiver who can look down-field and adjust his route accordingly. These are examples of nontraditional data points that currently cannot be accounted for in structured data. However, this can all be seen by coaches, scouts, fans, etc. and many of these analyses/observations can be found on social media platforms.

**ADD SUMMARY OF FINDINGS HERE**

### Data

The data will be collected by creating a pipeline to live stream tweets that contain tag words relate to each team playing in the NFL Conference Championship game. For example, during the Tampa Bay Buccaneers versus Green Bay Packers game, the following tag words were used to collect tweets:

  ```
  "Tom Brady", "Aaron Rodgers", "Buccaneers", "GoPackGo", "TBvsGB", "Green Bay Packers", "Tampa Bay Buccaneers", "Superbowl",  "Bucs", "Packers", "NFC Championship", "SuperbowlLV", "NFLPlayoffs"
  ```
These tag words were chosen based off a simple search on twitter, which helped in identifying the most popular tag words used for each team. The tag words for the post-game tweets were chosen after both championship games were completed. Ultimately, we were able to collect ~190,000 game tweets and ~80,000 post-game tweets.

## Methodology

Anaconda version 4.8.3 and MongoDB 4.2.3 Community was used to complete this project. Anaconda allowed us to utilize Jupyter Notebooks, which used Python version 3.7.4. Jupyter was used to create the python scripts and analyze the data. The following packages were used in this project:

### Tools and Libraries

- Tweet Streaming in Python
  - `import os`: Allows Python to obtain API credentials from operating system
  - `import tweepy`: Access Twitter API
  - `from tweepy import OAuthHandler`: Create OAuthHandler instance for authenticatation of API credentials
  - `from tweepy import Stream`: Create Stream object
  - `from tweepy import StreamListener`: Create StreamListener class that listens to tweets
  - `from tweepy import API`: Class that creates a wrapper for the API provided by Twitter
  - `from pymongo import MongoClient`: Creates MongoDB connection
  - `import json`: Converts JSON string to Python dictionary

- Analyzing Tweets in Python
  - `import pandas as pd`: Creates pandas dataframe
  - `from pymongo import MongoClient`: Creates MongoDB connection and loads data from MongoDB
  - `from pprint import pprint`: Print data from MongoDB
  - `import re`: Used to remove emojis, weblinks, usernames, extra whitespace, and any other unnecessary characters
  - `import spacy`: Used for Natural Language Processing
  - `import string`: Removes punctuation and digits
  - `import time`: Counts the number of seconds that have passed 
  - `from collections import defaultdict`: Creates dict to hold more than 1 value per key
  - `import textblob`: Sentiment analysis
  - `import matplotlib.pyplot as plt`: Generates images
  - `from wordcloud import WordCloud`: Creates Word Cloud image
  - `import seaborn as sns`: Generates bar plots
  - `import nltk`: Load nltk's English stopword list
  - `from nltk import FreqDist`: Count top frequent occuring words
  - `import numpy as np`: Handles large, multi-dimensional arrays and matrices
  - `from sklearn.cluster import DBSCAN`: Creates Density-Based Spatial Clustering of Applications with Noise clusters
  - `from sklearn.feature_extraction.text import TfidfVectorizer`: Create TD-IDF features 

## Phase I - Data Collection

### Step 1: Create Tweet Streaming Scripts

The .py scripts `game1_twitter_streaming.py`, `game2_twitter_streaming.py`, and `postgame_twitter_stream.py` were created. First, a connection to MongoDB needs to be established to store the collected data. 

```python
#create connection to MongoDB

client = MongoClient()
db = client['Superbowl_2021']
coll = db['Superbowl_tweets']
```

Now, the credentials obtained from the Twitter API need to be entered and stored in variables to be used later. The `os` module to is used to access the Twitter API credentials from the environment variables.

```python
#create variables that contains the user credentials to access Twitter API 

c_key = os.environ.get('tw_consumer_key')
c_sec = os.environ.get('tw_consumer_secret')
atk = os.environ.get('tw_access_token')
ats = os.environ.get('tw_access_token_secret')
```
Next, create a class called `MyListener` that will listen for tweets from Tweepy's StreamListener.

```python
class MyListener(StreamListener)
```

Then, we create a user defined function that handles our data. Below, we parse a valid JSON string and convert it into a Python dictionary, which allows us to collect information such as the tweet, hashtags, date tweet was created, the username of tweet creator, whether the tweet was retweeted or not, user timezone, and user location. Finally, the collected information is inserted into MongoDB.

```python
   def on_data(self, data):
        msg = json.loads(data) # Create a message from json file
        if "text" in msg: #[5]
            tweet = msg["text"]
            hashtags = msg["entities"]["hashtags"] 
            created = msg["created_at"]
            username = msg["user"]["screen_name"]
            retweeted = msg["retweeted"]
            user_tz = msg["user"]["time_zone"]
            user_location = msg["user"]["location"]
    
        coll.insert_one({'Date': created,
                    'User': username,
                    'Tweet': tweet,
                    'Retweeted': retweeted,
                    'Hashtags': hashtags,
                    'Time Zone': user_tz,
                    'Location': user_location}) #add collected data field to MongoDB
        return True
```

We then create a second function to handles errors, which can arise due to Twitter's streaming API rate limits.

```python
def on_error(self, status):
        print(status.text)
        return True
```

Finally, we set up our authentication using our Twitter credentials defined above, and initialize our stream using the StreamListener class defined above. Using the stream, we specify the tags we want to use to filter tweets. 

```python
if __name__ == '__main__':    
    listener = MyListener()
    
    auth = OAuthHandler(c_key, c_sec)
    auth.set_access_token(atk, ats)
    api = API(auth)

    twitterstream = Stream(auth=api.auth, listener=listener, tweet_mode="extended") 
    
    game_1_tags = ["Tom Brady", "Aaron Rodgers", "Buccaneers", "GoPackGo",
           "TBvsGB", "Green Bay Packers", "Tampa Bay Buccaneers", "Superbowl",
           "Bucs", "Packers", "NFC Championship", "SuperbowlLV", "NFLPlayoffs"] #Green Bay Packers, Tampa Bay Buccaneers 

    twitterstream.filter(track=game_1_tags, languages=["en"]) 
```

At this point, we have completed the authentication and can now live stream tweets. 


### Step 2: Live Stream Tweets

The .py scripts can be run from your terminal using the command `<file_name>.py`. Ensure that you are using the proper working directory to run file. To stop the program, press `Ctrl-C`, or `Cmd-C`. 

The .py scripts were ran as follows:

1. `game1_twitter_streaming.py`: Tampa Bay Buccaneers vs Greenbay Packers; stream from beginning of game to end of Game 1 
2. `game2_twitter_streaming.py`: Kansas City Chiefs vs Buffalo Bills; ; stream from beginning of game to end of Game 2 
3. `postgame_twitter_stream.py`: Use tag words for Tampa Bay Buccaneers and Kansas City Chiefs (winner of Game 1 and Game 2); stream from end of Game 2 and end when appropriate number of tweets are collected

## Phase II - Sentiment Analysis


### Step 1: Clean Tweets


### Step 2: Filter Tweets


### Step 3: Sentiment Analysis


### Step 4: Data Visualization


## Phase III - Text Clustering 


## Conclusion

## Resources
1. https://docs.tweepy.org/en/v3.5.0/streaming_how_to.html
2. https://gist.github.com/ctufts/e38e0588bf6d8f32e99d
3. http://adilmoujahid.com/posts/2014/07/twitter-analytics/
4. https://www.storybench.org/how-to-collect-tweets-from-the-twitter-streaming-api-using-python/


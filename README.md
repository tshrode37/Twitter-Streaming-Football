# Sentiment analysis and clustering football tweets obtained by live streaming twitter data
Data Science Practicum I Project - Using Sentiment Analysis and Clustering to Determine Superbowl Fan "Favorite"

## Summary

For this project, we will be creating a pipeline that live stream tweets with particular keywords relating to the teams that played in the NFL Conference Championships on 1/24/2021. The goal is to collect tweets during each NFL Conference Championship game (Kansas City vs Buffalo Bills, Tampa Bay Buccaneers vs Green Bay Packers) and after both  games have been completed. For this project, *game tweets* will refer to the tweets that were collected during each game, and *post-game tweets* will refer to the tweets collected after both games were completed Using this data, we seek to use sentiment analysis and text clustering to estimate the NFL team that is favored to win the Superbowl based on fans' analysis/comments/feelings. There are many aspects of sport games that cannot be captured by a box score such as a quarterback who can strategically mislead a defender to free up his receiver or a receiver who can look down-field and adjust his route accordingly. These are examples of nontraditional data points that currently cannot be accounted for in structured data. However, this can all be seen by coaches, scouts, fans, etc. and many of these analyses/observations can be found on social media platforms.

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

The .py scripts can be run from your terminal using the command `<file_name>.py`. Ensure that you are using the proper working directory to run file. To stop the program, press `Ctrl-C` in Windows. 

The .py scripts were ran as follows:

1. `game1_twitter_streaming.py`: Tampa Bay Buccaneers vs Greenbay Packers; stream from beginning of game to end of Game 1 
2. `game2_twitter_streaming.py`: Kansas City Chiefs vs Buffalo Bills; ; stream from beginning of game to end of Game 2 
3. `postgame_twitter_stream.py`: Use tag words for Tampa Bay Buccaneers and Kansas City Chiefs (winner of Game 1 and Game 2); stream from end of Game 2 and end when appropriate number of tweets are collected

To ensure that our data was written to MongoDB, we need to open Jupyter Notebook using the command `jupyter notebook` in the Anaconda terminal. Then, we can use the following commands:

```python
#check that data was written to MongoDB
client = MongoClient()
db = client['Superbowl_2021']
tweets = db['Superbowl_tweets']

pprint(tweets.find_one())
```

Using the `pandas` module, we can load the MongoDB data into Python and store the data in a pandas dataframe, as seen in the `game_tweets_df.jpg` file located in the Images file. 


## Phase II - Sentiment Analysis

Polarity - a measure of the negativity, the neutralness, or the positivity of the text

### Step 1: Clean Tweets
To perform sentiment analysis on our football tweets, we need to apply a few basic text cleaning techniques such as removing emoji's, punctuation, weblinks, usernames, hashtags, extra whitespace, and any unnecessary characters. The function used to remove most of the emoji's in our tweets can be found below.


```python
def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)
```

Then, we applied the `ReGex` module to further clean our tweets.

```python
no_html_tweets = no_emoji.apply(lambda x: re.sub('http://\S+', '', x)) #remove http://
no_html_tweets = no_html_tweets.apply(lambda x: re.sub('https://\S+', '', x)) #remove https://
no_html_tweets = no_html_tweets.apply(lambda x: re.sub('@\S+', '', x)) #remove @usernames
no_html_tweets = no_html_tweets.apply(lambda x: re.sub('#\S+', '', x)) #remove #hashtags
no_html_tweets = no_html_tweets.apply(lambda x: re.sub('\s\s+', ' ', x)) #remove extra whitespace
no_html_tweets = no_html_tweets.apply(lambda x: re.sub('RT', '', x)) #Remove RT
no_html_tweets = no_html_tweets.apply(lambda x: re.sub('/\S+', '', x)) #remove /
```
Refer to the `before_and_after_cleaning_tweets.jpg` file in the Images folder to see the tweets before and after using the techniques described above. The cleaned tweets were then added to our original dataframe and the clean tweets were then used to drop duplicated tweets. 

### Step 2: Filter Tweets

For this project, not only did we perform sentiment analysis two different sets of data *game tweets* and *post game tweets*, we also subsetted each dataset into *game-like* tweets and *team* tweets.

1. Game-like tweets: These include tweets pertaining to actual game activity
    - For example: "Tom Brady finally puts the ball downfield and throws three straight incompletions."
2. Team tweets: The tweets are separated using specified key words that match a tweet to a team
    - For example (a Tampa Bay tweet): "Tom Brady is god.  Im a dummy" 

Tag words used to subset our dataset into game-like tweets include:

```
"redzone", "ball", "incompletion", "interception", "throw", 
        "catch", "downfield", "oline", "offensive", "defensive", 
       "offense", "defense", "blocking", "block", "win", "lose", "sack", "superbowl",
       "score", "home", "away", "goat", "1st", "2nd", "3rd", "4th", "down", "td", "int", "touchdown", 
        "root", "stop", "pass", "rush", "play", "Tom Brady", "Patrick Mahomes", "Bucs", "Buccaneers", 
          "Gronk", "Gronkowski", "Brady", "TB", "Antonio Brown", "Chiefs", "Kansas City",
          "Travis Kelce", "Kelce", "Mahomes", "KC", "tackle", "offsides", "end zone", "block", "fair", "catch", 
          "field goal", "fumble", "grounding", "neutral", "pocket", "safety", "turnover", "zone", "snap"
```

To obtain these tweets, we created a `multidict`, which is a word used in Python to refer to a dictionary where mapping a single key to multiple values is possible. The resulting dataframe can be seen using the `multidict_to_df_gametweets.jpg` file in the Images folder.

Tag words used to subset our dataset into Kansas City tweets include:

```
"Patrick Mahomes", "Chiefs", "Kansas City", "Travis Kelce", "Kelce", "Mahomes", "KC", 
"Tyrann Mathieu", "Tyrann", "Mathieu", "Tyreek Hill"
```

Tag words used to subset our dataset into Tampa Bay tweets include:

```
"Tom Brady", "Bucs", "Buccaneers", "Gronk", "Gronkowski", "Brady", "TB", "Antonio Brown",
             "Godwin"
```

The data needed above can be obtained by using a `for` loop.

### Step 3: Sentiment Analysis

The `textblob` module allows us to calculate polarity, subjectivity, and assessments.

* Polarity is a float within the range [-1.0, 1.0]; where 1 means positive statement and -1 means a negative statement
* Subjectivity is a float within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective; Subjective sentences generally refer to personal opinion, emotion or judgment whereas objective refers to factual information
* Assessments is a list of polarity and subjectivity scores for the assessed tokens

To create a dataframe that contains the above information, the function below was created. The function was then applied to our cleaned tweets (from Step 1 above) for our full dataset, the game-like tweets, Kansas City tweets, and Tampa Bay tweets. 

```python
def textblob_sentiments(text, sentiment_dict, keys_list, polarity_list, subj_list, assess_list):
    
# text is the tweets to be analyzed
# sentiment_dict is an empty dict 
# keys_list, polarity_list, subj_list, assess_list are empty lists

    print("Adding sentiments tuple to dictionary...")
    
    start = time.time()
    for r in range(0, len(text)):
        sentiment_dict[text[r]] = textblob.TextBlob(text[r]).sentiment_assessments #calculate sentiment assessments and add them to empty dictionary (tweet:sentiment assessments tuple)
    
    end = time.time()
    print('Process took', int(round(end - start)), 'seconds') #count number of seconds that it takes to process code above 
    
    print("Creating new dataframe...")
    
    for key, value in sentiment_dict.items():
        keys_list.append(key) #get tweets
        value_list = list(value) #get sentiment assessments in a list
        polarity_list.append(value_list[0]) #get polarity scores
        subj_list.append(value_list[1]) #get subjectivity scores
        assess_list.append(value_list[2]) #get assessments 
        
    print("Last step...")
    
    new_df = pd.DataFrame(zip(text, polarity_list, subj_list, assess_list), columns=['Tweet', 'Polarity', 'Subjectivity','Assessments']) #create new dataframe using lists above
    return(new_df)
```

As an example, to collect the sentiment assessments for our full dataset, we can use the code below:

```python
test_dict = {} #dictionary to calculate and contain sentment assessments
keys = [] #get keys (tweets) from test_dict
polarity = [] #get polarity scores
subjectivity = [] #get subjectivity scores
assessments = [] #get assessments

assessments_df = textblob_sentiments(clean_tweets_df["Clean Tweets"], test_dict, keys, polarity, subjectivity, assessments) #apply function above

assessments_df.head() #check to make sure data was collected correctly
```



### Step 4: Data Visualization

The polarity distribution plots for the dataset and the subsetted can be found in the Images folder:

* `full_polarity.png`: Polarity distribution for full dataset
* `game_polarity.png`: Polarity distribution for game-like data
* `chiefs_polarity.png`: Polarity distribution for Kansas City data
* `bucs_polarity.png`: Polarity distribution for Tampa Bay data

## Phase III - Text Clustering 


### Step 1: Clean Text using NLP


```python
# simple clean text function -- spacy lowercases, removes stopwords, lemmatizes
    #function from Text Analytics Week 5 Assignment
    
def clean_text(docs):
    # remove punctuation and numbers
    # I do this before lemmatizing, so things like "act's" turn into 'act' instead of 'act s'
    print('removing punctuation and digits')
    table = str.maketrans({key: None for key in string.punctuation + string.digits})
    clean_docs = [d.translate(table) for d in docs]
    
    print('spacy nlp...longest part')
    nlp_docs = [nlp(d) for d in clean_docs]
    
    # keep the word if it's a pronoun, otherwise use the lemma
    # otherwise spacy substitutes '-PRON-' for pronouns
    print('getting lemmas')
    lemmatized_docs = [[w.lemma_ if w.lemma_ != '-PRON-'
                           else w.lower_
                           for w in d]
                      for d in nlp_docs]
    
    # remove stopwords
    print('removing stopwords')
    lemmatized_docs = [[lemma for lemma in doc if lemma not in stopwords] for doc in lemmatized_docs] 

        #remove specific stop words
    
    # join tokens back into doc (string) because lemmatized_docs is a list
    clean_docs = [' '.join(l) for l in lemmatized_docs] #join tweets in a string
        
    return clean_docs
```

### Step 2: Data Visualization


Word clouds for the full dataset include:

* `full_lowpolarity_wordcloud.png`
* `full_toppolarity_wordcloud.png`
* `full_wordcloud.png`: Word cloud for full cleaned tweets 

Word clouds for the game-like data include:

* `team_lowpolarity_wordcloud.png`
* `team_toppolarity_wordcloud.png`
* `team_wordcloud.png`

Word clouds for the Kansas City tweets:

* `chiefs_lowpolarity_wordcloud.png`
* `chiefs_toppolarity_wordcloud.png`
* `chiefs_wordcloud.png`

Word clouds for the Tampa Bay tweets include: 

* `bucs_lowpolarity_wordcloud.png`
* `bucs_wordcloud.png`
* `bucs_toppolarity_wordcloud.png`



### Step 3: DBSCAN Clustering




## Resources
1. https://docs.tweepy.org/en/v3.5.0/streaming_how_to.html
2. https://gist.github.com/ctufts/e38e0588bf6d8f32e99d
3. http://adilmoujahid.com/posts/2014/07/twitter-analytics/
4. https://www.storybench.org/how-to-collect-tweets-from-the-twitter-streaming-api-using-python/
5. Remove emoji's: https://gist.github.com/slowkow/7a7f61f495e3dbb7e3d767f97bd7304b 
6. Reindex dataframe: https://stackoverflow.com/questions/28885073/reindexing-after-pandas-drop-duplicates
7. Multidict: https://medium.com/analytics-vidhya/mapping-keys-to-multiple-values-in-a-dictionary-b5022de9dd0e
8. Textblob: https://www.analyticsvidhya.com/blog/2018/02/natural-language-processing-for-beginners-using-textblob/

# Sentiment analysis and clustering football tweets obtained by live streaming twitter data
Data Science Practicum I Project - Using Sentiment Analysis and Clustering to Determine Superbowl Fan "Favorite"

## Summary

For this project, we will be creating a pipeline that live stream tweets with particular keywords relating to the teams that played in the NFL Conference Championships on January 24, 2021. The goal is to collect tweets during each NFL Conference Championship game (Kansas City vs Buffalo Bills, Tampa Bay Buccaneers vs Green Bay Packers) and after both  games have been completed. For this project, *game tweets* will refer to the tweets that were collected during each game, and *post-game tweets* will refer to the tweets collected after both games were completed Using this data, we seek to use sentiment analysis and text clustering to estimate the NFL team that is favored to win the Superbowl based on fans' analysis/comments/feelings. There are many aspects of sport games that cannot be captured by a box score such as a quarterback who can strategically mislead a defender to free up his receiver or a receiver who can look down-field and adjust his route accordingly. These are examples of nontraditional data points that currently cannot be accounted for in structured data. However, this can all be seen by coaches, scouts, fans, etc. and many of these analyses/observations can be found on social media platforms.


### Data

The data will be collected by creating a pipeline to live stream tweets that contain tag words that relate to each team playing in the NFL Conference Championship game. For example, during the Tampa Bay Buccaneers versus Green Bay Packers game, the following tag words were used to collect tweets:

  ```
  "Tom Brady", "Aaron Rodgers", "Buccaneers", "GoPackGo", "TBvsGB", "Green Bay Packers", "Tampa Bay Buccaneers", "Superbowl",  "Bucs", "Packers", "NFC Championship", "SuperbowlLV", "NFLPlayoffs"
  ```
These tag words were chosen based off a simple search on twitter, which helped in identifying the most popular tag words used for each team. The tag words for the post-game tweets were chosen after both championship games were completed. Ultimately, we were able to collect ~190,000 game tweets and ~80,000 post-game tweets. 

## Methodology

Anaconda version 4.8.3 and MongoDB 4.2.3 Community was used to complete this project. Anaconda allowed us to utilize Jupyter Notebooks, which used Python version 3.7.4. Jupyter was used to help create the python scripts and analyze the data. The following packages were used in this project:

### Tools and Libraries

- Tweet Streaming in Python
  - `import os`: Allows Python to obtain API credentials from operating system
  - `import tweepy`: Access Twitter API
  - `from tweepy import OAuthHandler`: Create OAuthHandler instance for authentication of API credentials
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
  - `from nltk import FreqDist`: Count top frequent occurring words
  - `import numpy as np`: Handles large, multi-dimensional arrays and matrices
  - `from sklearn.cluster import DBSCAN`: Creates Density-Based Spatial Clustering of Applications with Noise clusters
  - `from sklearn.feature_extraction.text import TfidfVectorizer`: Create TD-IDF features 
  - `from sklearn import metrics`: Clustering performance metrics

## Phase I - Data Collection

### Step 1: Create Tweet Streaming Scripts

The .py scripts `game1_twitter_streaming.py`, `game2_twitter_streaming.py`, and `postgame_twitter_stream.py` were created. To create the scripts, the first step is to establish a connection to MongoDB to store the collected data. 

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

Using the `pandas` module, we can load the MongoDB data into Python and store the data in a pandas dataframe, as seen in the `game_tweets_df.jpg` file located in the Images folder. We can also open MongoDB and view our data, as seen in `mongodb_superbowl_tweets.jpg`


## Phase II - Sentiment Analysis

### Step 1: Clean Tweets

The data collected for the game tweets and the post-game tweets were loaded into Jupyter Notebook directly from MongoDB, but can also be loaded from the `superbowl_2021_post_game_tweets.csv` and `superbowl_2021_game_tweets.csv` files. The `superbowl_2021_game_tweets.csv` is can be located in the `main` branch using the path: `OneDrive/Desktop/MSDS 692 Assignments & Readings/superbowl_2021_game_tweets.csv` and can be downloaded as a .txt file.

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
"redzone", "ball", "incompletion", "interception", "throw", "catch", "downfield", "oline", "offensive", "defensive", 
"offense", "defense", "blocking", "block", "win", "lose", "sack", "superbowl", "score", "home", "away", "goat", 
"1st", "2nd", "3rd", "4th", "down", "td", "int", "touchdown", "root", "stop", "pass", "rush", "play", "Tom Brady", 
"Patrick Mahomes", "Bucs", "Buccaneers", "Gronk", "Gronkowski", "Brady", "TB", "Antonio Brown", "Chiefs", "Kansas City",
Travis Kelce", "Kelce", "Mahomes", "KC", "tackle", offsides", "end zone", "block", "fair", "catch", "field goal",
"fumble", "grounding", "neutral", "pocket", "safety", "turnover", "zone", "snap"
```

To obtain these tweets, we created a `multidict`, which is a word used in Python to refer to a dictionary where mapping a single key to multiple values is possible. The resulting dataframe can be seen using the `multidict_to_df_gametweets.jpg` file in the Images folder.

Tag words used to subset our dataset into Kansas City tweets include:

```
"Patrick Mahomes", "Chiefs", "Kansas City", "Travis Kelce", "Kelce", "Mahomes", "KC", "Tyrann Mathieu", "Tyrann", "Mathieu", "Tyreek Hill"
```

Tag words used to subset our dataset into Tampa Bay tweets include:

```
"Tom Brady", "Bucs", "Buccaneers", "Gronk", "Gronkowski", "Brady", "TB", "Antonio Brown","Godwin"
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

Using the Natural Language Processing module `spaCy`, we can further clean our tweets by lowercasing words, removing stopwords, lemmatizing, and removing punctuation and digits. This can be done by applying a previously created function used in the Week 5 Assignment for MSDS 682: Text Analytics.

```python
nlp = spacy.load('en_core_web_lg')
stopwords = nltk.corpus.stopwords.words('english')

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
This function was applied to the full dataset, game-like tweets, Kansas City, and Tampa Bay tweets.

### Step 2: Data Visualization

Data visualization for the portion of the project included word clouds, which allow us to represent our text data in which the size of each word indicates its frequency or importance. For each sets of data, three word clouds were created:

1. Full cleaned tweets
2. Tweets with a polarity of 0.01 or greater
3. Tweets with a polarity of -0.01 or less

These visualization can be found in the Images folder. Word clouds for the full dataset include:

* `full_wordcloud.png`
* `full_toppolarity_wordcloud.png`
* `full_lowpolarity_wordcloud.png`

Word clouds for the game-like data include:

* `game_wordcloud.png`
* `game_toppolarity_wordcloud.png`
* `game_lowpolarity_wordcloud.png`

Word clouds for the Kansas City tweets:

* `chiefs_wordcloud.png`
* `chiefs_toppolarity_wordcloud.png`
* `chiefs_lowpolarity_wordcloud.png`

Word clouds for the Tampa Bay tweets include: 

* `bucs_wordcloud.png`
* `bucs_toppolarity_wordcloud.png`
* `bucs_lowpolarity_wordcloud.png`


### Step 3: DBSCAN Clustering

Clustering text documents are used to find commonalities or themes in our text. Using our clean tweets created above, we can import `TfidfVectorizer from sklearn` to convert the collection of raw documents to a matrix of TF-IDF features. After we import this module, we can create our vectorizer and then we can use the vectorizer to fit and transform our cleaned tweets. We will use the argument `min_df=10`so that we ignore terms that have a document frequency lower than 10.

```python
vectorizer = TfidfVectorizer(min_df=10) #min number of tweets (min doc freq)
features = vectorizer.fit_transform(clean_tweets) #cleaned tweets
type(features) 
features.shape #check dimensions of features

features = features.todense() #convert matrix to numpy dense matrix
```

Now that we have our features, we can create our DBSCAN model and fit the model. 

```python
model = DBSCAN(eps=0.5, min_samples=40, n_jobs= -1) # create a model
model.fit(features) # fit model
labels = model.labels_ # get model labels
```

The parameters used in our model above include:

1. `eps`: Epsilon; The maximum distance between two samples for one to be considered as in the neighborhood of the other
2. `min_samples`: Minimum number of Samples; The number of samples (or total weight) in a neighborhood for a point to be considered as a core point. This includes the point itself
3. `n_jobs`: The number of parallel jobs to run. None means 1 and -1 means using all processors

While there are other parameters than can be included in the model, the three mentioned above are the most important. 

```python
cluster_tweets = [] #tokenize words in each cluster and compute the counts for each token 

for i in range(0, no_clusters):
    cluster_tweets.append(nltk.FreqDist(nltk.tokenize.word_tokenize(' '.join(np.array(clean_tweets)[labels == i]))))

for i in range(0, len(cluster_tweets)):
    print('Cluster', i+1,'-', cluster_tweets[i].most_common(10), '\n') #most common words in each cluster
    
```

## Summary of Results

By live streaming tweets containing particular tag words, we were able to collect 270,988 total tweets combined between the *game tweets* and *postgame tweets*, which includes duplicate tweets. After removing duplicated tweets, the resulting total number of tweets is 155,943 combined between the *game tweets* and *postgame tweets*.

The results from the *game tweets* data, excluding duplicated tweets:

|       | Full Dataset  | Game-Like Dataset|   Kansas City Dataset   | Tampa Bay Dataset |
|  :---  |       :---:     |     :---:         |         :---:            |      :---:         |
|   Number of Tweets    |    125772  |      63598     |       13463     |       21022    |
|  Average Overall Sentiment |      0.06      |      0.08       |        0.12          |      0.08       |
|  Number of POS/NEUTRAL/NEG |      10520/110917/4335      |       6019/55687/1892       |       1358/11791/314         |     1796/18596/630        |
| Number of Clusters  |    36        |       9       |               NA   |         NA      |
| Number of Outliers  |    121135        |      63032       |               NA   |         NA      |
|  Silhouette Score |      -0.257      |        -0.067      |               NA   |         NA      |

Reviewing the table above, the average polarity score for the Kansas City tweets is greater than Tampa Bay, which suggests that fans favored Kansas City to win the Superbowl. After further analysis of frequent occurring words for the positive and negative tweets in each of our subsets, we find:

1. Full Dataset
  - The most frequent terms that arise for positive tweets include terms relating to the Tampa Bay Buccaneers
  - The most frequent terms that arise for negative tweets include terms relating to the Green Bay Packers and the Buffalo Bills
  - Most of the DBSCAN clusters suggest that Tampa Bay is favored to win the Superbowl and that Kansas City and Tampa Bay will be playing in the Superbowl
2. Game-Like Dataset
  - The most frequent terms that arise for positive tweets include terms relating to the Tampa Bay Buccaneers
  - The most frequent terms that arise for negative tweets include terms relating to the Green Bay Packers and the Buffalo Bills
  - Most of the DBSCAN clusters suggest that Tampa Bay is favored to win the Superbowl and that Kansas City and Tampa Bay will be playing in the Superbowl
3. Kansas City Dataset
  - The most frequent terms that arise for positive tweets include terms relating to the Tampa Bay Buccaneers
  - The most frequent terms that arise for negative tweets include terms relating to the Green Bay Packers and the Buffalo Bills
4. Tampa Bay Dataset
  - The most frequent terms that arise for positive tweets include terms relating to the Tampa Bay Buccaneers
  - The most frequent terms that arise for negative tweets include terms relating to the Green Bay Packers and the Buffalo Bills

These finding suggest that fans favored the Tampa Bay Buccaneers and the Kansas City Chiefs to play in the Superbowl, and wanted Tampa Bay to win. Refer to `Shrode_Practicum_GameTweets.ipynb` for more information.

The results from the *postgame tweets* data, excluding duplicated tweets:

|       | Full Dataset  | Game-Like Dataset|   Kansas City Dataset   | Tampa Bay Dataset |
|  :---  |       :---:     |     :---:         |         :---:            |      :---:         |
|   Number of Tweets    |    30171  |      17600     |       5136     |       9422    |
|  Average Overall Sentiment |      0.11      |      0.13       |          0.12         |      0.13       |
|  Number of POS, NEUTRAL, NEG |     3004/26364/803       |        1890/15270/440      |        498/4531/107            |     951/8208/263        |
| Number of Clusters  |     9       |         3     |               NA   |         NA      |
| Number of Outliers  |      29262      |     17428        |               NA   |         NA      |
|  Silhouette Score |       -0.253     |         -0.041     |               NA   |         NA      |

Reviewing the table above, the average polarity score for the Kansas City tweets is less than Tampa Bay, which suggests that fans favored Tampa Bay to win the Superbowl. After further analysis of frequent occurring words for the positive and negative tweets in each of our subsets, we find:

1. Full Dataset
  - The most frequent terms that arise for positive tweets include terms relating to the Tampa Bay Buccaneers
  - The most frequent terms that arise for negative tweets include terms relating to the Tampa Bay Buccaneers
  - Most of the DBSCAN clusters suggest that Tampa Bay is favored to win the Superbowl and that Kansas City and Tampa Bay will be playing in the Superbowl
2. Game-Like Dataset
  - The most frequent terms that arise for positive tweets include terms relating to the Tampa Bay Buccaneers and the Kansas City Chiefs
  - The most frequent terms that arise for negative tweets include terms relating to the Kansas City Chiefs
  - Most of the DBSCAN clusters suggest that Tampa Bay is favored to win the Superbowl and that Kansas City and Tampa Bay will be playing in the Superbowl
3. Kansas City Dataset
  - The most frequent terms that arise for positive tweets include terms relating to the Tampa Bay Buccaneers and the Kansas City Chiefs
  - The most frequent terms that arise for negative tweets include terms relating to the Kansas City Chiefs
4. Tampa Bay Dataset
  - The most frequent terms that arise for positive tweets include terms relating to the Tampa Bay Buccaneers
  - The most frequent terms that arise for negative tweets include terms relating to the Tampa Bay Buccaneers


These finding suggest that fans favored the Tampa Bay Buccaneers and the Kansas City Chiefs to play in the Superbowl, and wanted Tampa Bay to win. Refer to `Shrode_Practicum_PostGameTweets.ipynb` for more information.

## For the Future

Clustering can be a powerful tool, and if time allowed, further analysis and parameter tuning would have been included. Now, hyperparameter tuning is not available for DBSCAN clustering. Thus, we can use a loop to check different values for `eps` and `minpts` using the function below:

```python
eps = [0.2, 0.5, 0.75, 1.00]
minpts = [20, 25, 30, 40]

for x in eps:
    for y in minpts:
        model = DBSCAN(eps=x, min_samples=y, n_jobs= -1)
        model.fit(features)
        labels = model.labels_
        no_clusters = len(np.unique(labels)) #number of unique labels
        no_noise = np.sum(np.array(labels) == -1, axis=0)
        print('Epsilon (eps): %0.1f' % x)
        print('Minimum samples (minPts): %d' % y)
        print('Estimated no. of clusters: %d' % no_clusters)
        print('Estimated no. of noise points: %d' % no_noise)
        print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(features, labels))
        print('\n')
```
It should be noted that clustering may take longer for large amounts of features. Also, with more time, scatterplots of the DBSCAN clusters would have been included. Finally, with more tweaking, more text cleaning could be perfomered to remove more of the emoji's tweets and "correct" misspelled words. With these changes, we may obtain a better representation of clusters within our data.  

## Resources
1. Handling streaming errors: https://docs.tweepy.org/en/v3.5.0/streaming_how_to.html
2. Collect desired data fields: https://gist.github.com/ctufts/e38e0588bf6d8f32e99d
3. Running twitter stream in Terminal: http://adilmoujahid.com/posts/2014/07/twitter-analytics/
4. Initialize Tweepy Stream: https://www.storybench.org/how-to-collect-tweets-from-the-twitter-streaming-api-using-python/
5. Import data from MongoDB: https://stackoverflow.com/questions/16249736/how-to-import-data-from-mongodb-to-pandas
6. Remove emoji's: https://gist.github.com/slowkow/7a7f61f495e3dbb7e3d767f97bd7304b 
7. Reindex dataframe: https://stackoverflow.com/questions/28885073/reindexing-after-pandas-drop-duplicates
8. Multidict: https://medium.com/analytics-vidhya/mapping-keys-to-multiple-values-in-a-dictionary-b5022de9dd0e
9. Dictionary to Dataframe: https://datatofish.com/dictionary-to-dataframe/
10. Textblob: https://www.analyticsvidhya.com/blog/2018/02/natural-language-processing-for-beginners-using-textblob/
11. spaCy: https://spacy.io/
12. Word cloud: https://www.geeksforgeeks.org/generating-word-cloud-python/
13. DBSCAN model: https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html?highlight=dbscan
14. Estimate clusters and noise points: https://www.machinecurve.com/index.php/2020/12/09/performing-dbscan-clustering-with-python-and-scikit-learn/
15. Silhouette score: https://shritam.medium.com/how-dbscan-algorithm-works-2b5bef80fb3
16. TF-IDF: https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html

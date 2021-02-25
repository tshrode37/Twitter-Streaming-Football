# Sentiment analysis and text clustering on National Football tweets obtained by live streaming twitter data
Data Science Practicum I Project - Using Sentiment Analysis and Clustering to Determine Superbowl Fan "Favorite"

## Summary

For this project, we will be creating a pipeline that live stream tweets with particular keywords relating to the teams that played in the NFL Conference Championships on 1/24/2021. The goal is to collect tweets during each NFL Conference Championship game (Kansas City vs Buffalo Bills, Tampa Bay Buccaneers vs Green Bay Packers) and after both  games have been completed. For this project, `game tweets` will refer to the tweets that were collected during each game, and `post-game tweets` will refer to the tweets collected after both games were completed Using this data, we seek to use sentiment analysis and text clustering to estimate the NFL team that is favored to win the Superbowl based on fans' analysis/comments/feelings. There are many aspects of sport games that cannot be captured by a box score such as a quarterback who can strategically mislead a defender to free up his receiver or a receiver who can look down-field and adjust his route accordingly. These are examples of nontraditional data points that currently cannot be accounted for in structured data. However, this can all be seen by coaches, scouts, fans, etc. and many of these analyses/observations can be found on social media platforms.

**ADD SUMMARY OF PROJECT HERE**

### Data

The data will be collected by creating a pipeline to live stream tweets that contain tag words relate to each team playing in the NFL Conference Championship game. For example, during the Kansas City vs Buffalo Bills game, the following tag words were used to collect tweets:

  ```
  "Josh Allen", "Patrick Mahomes", "Buffalo Bills", "Kansas City Chiefs", "Superbowl", "ChiefsKingdom", "ChiefsvsBills", "AFC Championship", "SuperbowlLV", "BillsMafia", "NFLPlayoffs"
  ```
These tag words were chosen based off a simple search on twitter, which helped in identifying the most popular tag words used for each team. The tag words for the post-game tweets were chosen after both championship games were completed. Ultimately, we were able to collect ~190,000 game tweets and ~80,000 post-game tweets.

## Methodology


### Tools and Libraries

- Tweet Streaming in Python
  - import os
  - import tweepy
  - from tweepy import OAuthHandler 
  - from tweepy import Stream
  - from tweepy import StreamListener
  - from tweepy import API
  - from pymongo import MongoClient
  - import json

- Analyzing Tweets in Python
  - import pandas as pd #to create dataframe
  - from pymongo import MongoClient #load data from MongoDB
  - from pprint import pprint #print data from MongoDB
  - import re
  - import spacy
  - import nltk
  - import string #to remove punct and digits
  - import time #count the number of seconds that have passed
  - from collections import defaultdict #create dict to hold more than 1 value per key
  - import textblob #sentiment analysis
  - import matplotlib.pyplot as plt #generate a word cloud image and bar plots
  - from wordcloud import WordCloud
  - import seaborn as sns
  - from nltk import FreqDist #count top frequent words
  - import numpy as np
  - from sklearn.cluster import DBSCAN
  - from sklearn.feature_extraction.text import TfidfVectorizer #create TD-IDF features 


## Phase I - Collect Data

## Phase II - Sentiment Analysis

## Phase III - Text Clustering 


## Conclusion

## Resources
1. https://docs.tweepy.org/en/v3.5.0/streaming_how_to.html


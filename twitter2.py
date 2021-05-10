import tweepy
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import timeit
import os.path
import nltk
import string
import re

import twitter

from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize

api = twitter.api
stemmer = PorterStemmer()
#https://www.geeksforgeeks.org/text-preprocessing-in-python-set-1/
# stem words in the list of tokenised words
def stem_words(text):
    word_tokens = word_tokenize(text)
    stems = [stemmer.stem(word) for word in word_tokens]
    return stems
# remove punctuation
def remove_punctuation(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)
  

#https://fairyonice.github.io/extract-someones-tweet-using-tweepy.html
def run_word_scan(userID=50000):
    tweets = api.user_timeline(screen_name=userID, 
                           # 200 is the maximum allowed count
                           count=200,
                           include_rts = False,
                           # Necessary to keep full_text 
                           # otherwise only the first 140 words are extracted
                           tweet_mode = 'extended'
                           )
    all_tweets = []
    all_tweets.extend(tweets)
    oldest_id = tweets[-1].id
    while True:
        tweets = api.user_timeline(screen_name=userID, 
                           # 200 is the maximum allowed count
                           count=200,
                           include_rts = False,
                           max_id = oldest_id - 1,
                           # Necessary to keep full_text 
                           # otherwise only the first 140 words are extracted
                           tweet_mode = 'extended'
                           )
        if len(tweets) == 0:
            break
        oldest_id = tweets[-1].id
        all_tweets.extend(tweets)
        print('N of tweets downloaded till now {}'.format(len(all_tweets)))
    return all_tweets

def zipf_plot(userID=50000):
    tweets = run_word_scan(userID)
    for t in tweets:
        text = t.full_text
        text = remove_punctuation(text)
        text = stem_words(text)
        print(text)
    return None

zipf_plot(userID=281516)
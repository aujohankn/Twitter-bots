import tweepy
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import timeit
import os.path
import nltk
import string
import re
import langdetect as lang

from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize

auth = tweepy.OAuthHandler("hthiIooKXUK1nN13UAH49ZOs2", "gWnJTNB3xy9nOrAUjTqdiQCIe3WxvgzQUZTD4EVXWT5uw0X9ju")
auth.set_access_token("1363777368519753729-dgXhlOUFQMt9OMDwZJhScjfaXOxuuO", "1SRoyDU4RNdEFsIBTC4305V76yWFFrH0Br23TCmSzjfBh")

api = tweepy.API(auth, wait_on_rate_limit=True, retry_count=10, retry_delay=10, retry_errors=set([104, 503]))


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
  
def read_tweets(userID):
    df = pd.read_csv(r"C:\Users\johan\OneDrive - Aarhus universitet\UNI\3 år\bachelor\Ny mappe\Documents\Tweets\tweet" + str(userID) + ".csv")['tweet_text'].values.tolist()
    return df

def read_full_tweets(userID):
    df = pd.read_csv(r"C:\Users\johan\OneDrive - Aarhus universitet\UNI\3 år\bachelor\Ny mappe\Documents\Tweets\tweet" + str(userID) + ".csv").values.tolist()
    return df

def zipf_plot(data:list, userID):
    words = []
    d = []
    tweet_count = len(data)
    for i,text in enumerate(data):
        try:
            l = lang.detect(str(text))
            if l != "en":
                continue
        except lang.LangDetectException as error:
            print("Something went wrong: " + str(error))
            continue
        if i % 250 == 0:
            print(str(round(100*i/tweet_count)) + "% completed")
        text_words = text.split(",")
        words, d = zipf_plot_run_word_count(text_words, words, d)
    words.sort(key=lambda x:x[1], reverse=True)
    print(words[:20])
    plt.rc('font', size=14)
    fig, ax = plt.subplots(figsize=(12, 6))
    plt.title("Zipf's's Law: User " + str(userID))
    xax = []
    yax = []
    yax_expected = []
    zipf_n = words[0][1]
    for i in range(20):
        xax.append(words[i][0])
        yax.append(words[i][1])
        yax_expected.append(zipf_n/(i+1))
    ax.bar(xax, yax)
    plt.plot(xax,yax_expected, c='red')
    plt.show()
    return None

def zipf_plot_run_word_count(text_array, words, d):
    for t in text_array:
        t = t.strip("[]'' '")
        if t.startswith("http") or t.isnumeric():
            continue
        if t in d:
            x = d.index(t)
            words[x][1] += 1
        else:
            words.append([t,1])
            d.append(t)
    return words, d



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

import twitter

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
  

#https://fairyonice.github.io/extract-someones-tweet-using-tweepy.html
def run_tweet_scan(userID=50000):
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

def generate_tweets_csv(data:list):
    tweet_create_time = []
    tweet_text = []

    for i in data:
        tweet_create_time.append(i.created_at)
        text = i.full_text
        text = remove_punctuation(text)
        text = stem_words(text)
        tweet_text.append(text)
    user_list = {'created_at' : tweet_create_time,
        'tweet_text': tweet_text
        }
    df = pd.DataFrame(user_list, columns=['created_at', 'tweet_text'])
    df.to_csv(r"C:\Users\johan\OneDrive - Aarhus universitet\UNI\3 år\bachelor\Implementering\words_test.csv")
    print("Generated csv sheet successfully")

def zipf_plot(userID=50000):
    try:
        tweets = run_tweet_scan(userID)
    except IndexError as error:
        print(error)
        return None
    words = []
    d = []
    for t in tweets:
        text = t.full_text
        try:
            l = lang.detect(str(text))
            if l != "en":
                continue
        except lang.LangDetectException as error:
            print("Something went wrong: " + error)
            continue
        text = remove_punctuation(text)
        text = stem_words(text)
        #print(text)
        #Is word unique
        for t in text:
            if t in d:
                x = d.index(t)
                words[x][1] += 1
            else:
                words.append([t,1])
                d.append(t)
    words.sort(key=lambda x:x[1], reverse=True)
    print(words[:20])
    plt.rc('font', size=16)
    fig, ax = plt.subplots(figsize=(12, 6))
    plt.title("Zipf's's Law: User " + str(userID))
    xax = []
    yax = []
    for i in range(20):
        xax.append(words[i][0])
        yax.append(words[i][1])
    plt.plot(xax,yax, c='red')
    plt.show()
    return None

def word_scan(csv_name):
    screen_name_list = pd.read_csv(r"/home/johankn/Dev/Documents-1/"+str(csv_name)+".csv")['screen_name'].values.tolist()
    for sn in screen_name_list:
        if (os.path.isfile(r"/home/johankn/Dev/Documents-1/Tweets/tweet"+str(sn)+".csv")):
            print("A file with user " + str(sn)+ " already exists.")
        else:
            try:
                generate_tweets_csv(run_tweet_scan(userID=sn))
            except tweepy.TweepError as error:
                print(error)
                continue
word_scan("test2")

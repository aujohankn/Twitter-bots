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
def run_tweet_scan(screen_name=50000):
    try:
        api.get_user(id=screen_name)
        print('Found user')
    except tweepy.error.TweepError as error:
        print(error)
        return None
    tweets = api.user_timeline(id=screen_name, 
                           # 200 is the maximum allowed count
                           count=200,
                           include_rts = False,
                           # Necessary to keep full_text 
                           # otherwise only the first 140 words are extracted
                           tweet_mode = 'extended'
                           )
    if not tweets:
        print("No Tweets")
        return None
    all_tweets = []
    all_tweets.extend(tweets)
    oldest_id = tweets[-1].id
    while True:
        tweets = api.user_timeline(id=screen_name, 
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

def generate_tweets_csv(data:list, sn):
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
    df.to_csv(r"/home/johankn/Dev/Documents-1/Tweets/tweet"+str(sn)+".csv")
    print("Generated csv sheet successfully")

def read_tweets(userID):
    df = pd.read_csv(r"C:\Users\johan\OneDrive - Aarhus universitet\UNI\3 år\bachelor\Ny mappe\Documents\Tweets\tweet" + str(userID) + ".csv")['tweet_text'].values.tolist()
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
            print("Something went wrong: " + error)
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

def word_scan(csv_name):
    screen_name_list = pd.read_csv(r"/home/johankn/Dev/Documents-1/"+str(csv_name)+".csv")['screen_name'].values.tolist()
    for sn in screen_name_list:
        if (os.path.isfile(r"/home/johankn/Dev/Documents-1/Tweets/tweet"+str(sn)+".csv")):
            print("A file with user " + str(sn)+ " already exists.")
        else:
            print(sn)
            try:
                tweets = run_tweet_scan(screen_name=sn)
                if tweets != None:
                    generate_tweets_csv(tweets, sn)
            except tweepy.TweepError as error:
                print(error)
                continue

#zipf_plot(userID=10134642)
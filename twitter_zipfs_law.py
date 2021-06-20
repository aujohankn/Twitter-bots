import matplotlib.pyplot as plt
import pandas as pd
import os
import string
import re
import langdetect as lang

from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize

stemmer = PorterStemmer()

def stem_words(text):
    # Stem words in the list of tokenised words
    # From https://www.geeksforgeeks.org/text-preprocessing-in-python-set-1/
    word_tokens = word_tokenize(text)
    stems = [stemmer.stem(word) for word in word_tokens]
    return stems

def remove_punctuation(text):
    # Remove punctuation
    # From https://www.geeksforgeeks.org/text-preprocessing-in-python-set-1/
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)

def read_tweets(userID):
    # Reads the tweet csv and returns the tweet text in a Pandas DataFrame
    path = os.getcwd()+"\ScrapedData\Tweets\\" 
    df = pd.read_csv(path+"tweet" + str(userID) + ".csv")['tweet_text'].values.tolist()
    return df

def read_full_tweets(userID):
    # Reads the tweet csv and returns the full tweet with text and time in a Pandas DataFrame
    path = os.getcwd()+"\ScrapedData\Tweets\\" 
    df = pd.read_csv(path+"tweet" + str(userID) + ".csv")
    return df

def zipf_plot(data:list):
    # Draws the Zipf's law distribution from a dataset of tweet texts
    # Also draws the expected distribution
    # Input: List of tweet text strings
    # Returns nothing
    print(len(data))
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
    plt.rc('font', size=14)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    plt.title("Zipf's Law")
    xax = []
    yax = []
    yax_expected = []
    zipf_n = words[0][1]
    for i in range(min(len(data),20)):
        xax.append(words[i][0])
        yax.append(words[i][1])
        yax_expected.append(zipf_n/(i+1))
    ax.bar(xax, yax, label="User Data")
    try:
        ax.set_xticklabels(xax, ha='right', rotation=45, rotation_mode='anchor')
    except:
        print("Something went wrong in Zipf")

    ax.set_ylabel("Word count")
    plt.plot(xax,yax_expected, c='red', label="Zipf's Law")
    
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.5, axis="y")
    plt.legend()
    plt.tight_layout()
    plt.show()
    return None

def zipf_plot_run_word_count(text_array, words, d):
    # Counts the occurrence of every word in a list
    # Input: List of text to count words,
    # List of words with count (for recursion),
    # d is list of used words
    # Returns: List of words with their count,
    # also returns a list of words without count
    for t in text_array:
        t = t.strip("[]''’' “”")
        t = deEmojify(t)
        if t.startswith("http") or t.isnumeric() or not t:
            continue
        if t in d:
            x = d.index(t)
            words[x][1] += 1
        else:
            words.append([t,1])
            d.append(t)
    return words, d

def load_and_zipf_plot(userID):
    # Function for gui, simply runs the two functions in sequence
    # Returns nothing
    tweets = read_tweets(userID)
    zipf_plot(tweets)

def deEmojify(text):
    # Removes emojis and other symbols
    # From https://stackoverflow.com/questions/33404752/removing-emojis-from-a-string-in-python
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)


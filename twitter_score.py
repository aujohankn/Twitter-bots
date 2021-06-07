import os
import numpy as np
import langdetect as lang
import pandas as pd
import statistics

from twitter_benfords_law import csv_to_list
import twitter_zipfs_law as zl
import tm_tools as tm

path = r"/home/johankn/Dev/Documents-1/ScrapedData"

time_threshold = 60*60 #an hour
most_common_words = ["the", "be", "to", "of", "and", "a", "in", "that", "have",
                    "i", "it", "for", "not", "on", "with", "he", "as", "you", "do", "at"
                    "this", "but" , "his", "by", "from", "they", "we", "say"]

def benford_calculate_score(data:list):
    # Calculates a score based on deviation from Benford's law
    # Input: List of friends' friend count
    # Returns score as float
    benford = [0.301, 0.176, 0.125, 0.097, 0.079, 0.067, 0.058, 0.051, 0.046]
    digits = np.arange(1,10)
    digit_probs = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    data_length = len(data)
    for number in data:
        first_digit = int(str(number)[:1])
        digit_probs[first_digit-1] += 1 / data_length
    
    score:float = 0
    for i, d in enumerate(digit_probs):
        n = benford[i]
        score += ((abs(d-n)/n)/9)*100
    return score


def zipf_calculate_score(data:list):
    # Calculates a score based on deviation from Zipf's law
    # Input: List of tweet text strings
    # Returns score as float
    words = []
    tweet_count = len(data)
    d = []
    for i,text in enumerate(data):
        try:
            l = lang.detect(str(text))
            if l != "en":
                continue
        except lang.LangDetectException as error:
            print("Something went wrong: " + str(error))
            continue
        if i % 500 == 0:
            print(str(round(100*i/tweet_count)) + "% completed")
        text_words = text.split(",")
        words, d = zl.zipf_plot_run_word_count(text_words, words, d)
    words.sort(key=lambda x:x[1], reverse=True)
    total_words = sum(words[i][1] for i in range(len(words)))
    print("Total words",total_words)
    if total_words < 10:
        return -1
    xax = []
    yax = []
    yax_expected = []
    try:
        zipf_n = words[0][1]
    except IndexError as e:
        print(e)
        return -1    
    for i in range(len(words)):
        xax.append(words[i][0])
        yax.append(words[i][1])
        yax_expected.append(zipf_n/(i+1))
    score:float = 0
    for i in range(20):
        try:
            if yax[i] == yax[i+1] and yax[i] > 100:
                s = ("Same occurence count for words", words[i][0], "and", words[i+1][0], ":", yax[i])
                print(s)
                score += 5
        except IndexError as e:
            print(e)
            continue
    for i, w in enumerate(words):
        n = yax_expected[i]
        y = yax[i]
        if w[0] not in most_common_words and w[1] > 1:
            score += 100*(w[1]/total_words)
    return score

def tweet_calculate_score(data):
    # Calculates score for both Zipf's law and heated time maps
    # Input: List of tweets with both text and timestamp
    # Returns Zipf's law score and time map score
    # Returns -1 if N/A
    tweet_text_list = data['tweet_text'].values.tolist()
    zipf_score = zipf_calculate_score(tweet_text_list)
    time_score:float = 0
    tweet_time_list = data['created_at'].values.tolist()
    try:
        _,_,sep_array = tm.analyze_tweet_times(name_to_get=" ", all_tweets=tweet_time_list)
    except:
        return -1, -1
    if len(sep_array) == 0:
        return -1, -1
    time_average_dif = [0,0]
    time_average_dif = sum(sep_array) / len(sep_array)
    time_median_dif = [statistics.median(sep_array[i,0] for i in range(len(sep_array))),
                        statistics.median(sep_array[i,1] for i in range(len(sep_array)))]
    for point in sep_array:
        deviation = abs(point-time_median_dif)
        if deviation[0] < time_threshold and deviation[1] < time_threshold:
            time_score += 100/len(sep_array)
    print("Average:",time_average_dif)
    print("Median:",time_median_dif)
    return zipf_score, time_score

def calculate_user_total_score(userID):
    # Calculates the score from 
    # Input: Twitter account id to generate score for
    # Returns total score, Benford's law score, Zipf's law score, time map score in that order
    # Returns -1 if N/A
    print("Calculating score for user", userID)
    try:
        friend_list = csv_to_list(r'C:\Users\johan\OneDrive - Aarhus universitet\UNI\3 år\bachelor\Ny mappe\Documents\ScrapedData\Friends\friend_scan'+str(userID)+".csv")
        tweet_list = pd.read_csv(r'C:\Users\johan\OneDrive - Aarhus universitet\UNI\3 år\bachelor\Ny mappe\Documents\ScrapedData\Tweets\tweet'+str(userID)+".csv")
    except FileNotFoundError as e:
        print(e)
        return -1, -1, -1, -1
    benford_score = benford_calculate_score(friend_list)
    
    zipf_score, time_score = tweet_calculate_score(tweet_list)
    if zipf_score == -1 or time_score == -1:
        return -1, -1, -1, -1
    total_score = benford_score + zipf_score + time_score
    print("Benford score",benford_score)
    print("Zipf score", zipf_score)
    print("Time score", time_score)
    print("Total score:",total_score)
    return total_score, benford_score, zipf_score, time_score

def run_score_scan():
    # Runs the full score scan, looking at all gathered data,
    # Generates a .csv file with score for all Twitter accounts gathered
    print("Begin score scan")
    file_list = os.listdir(path+'/Accounts/')
    user_id_list = []
    user_total_score_list = []
    user_benford_score_list = []
    user_zipf_score_list = []
    user_time_score_list = []
    for file in file_list:
        new_data = pd.read_csv(path+'/Accounts/' + file)
        for index, row in new_data.iterrows():
            userID = row[1]
            total_score, benford_score, zipf_score, time_score = calculate_user_total_score(userID)
            user_id_list.append(userID)
            user_total_score_list.append(total_score)
            user_benford_score_list.append(benford_score)
            user_zipf_score_list.append(zipf_score)
            user_time_score_list.append(time_score)
    user_list = {'id' : user_id_list,
        'total_score': user_total_score_list,
        'benford_score' : user_benford_score_list,
        'zipf_score': user_zipf_score_list,
        'time_score': user_time_score_list
        }

    df = pd.DataFrame(user_list, columns=['id', 'total_score', 'benford_score', 'zipf_score', 'time_score'])
    df.to_csv(path+"/Scores/score_scan.csv")
    print("End score scan")
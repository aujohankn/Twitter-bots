from re import I
import tweepy
import numpy as np
import pandas as pd
import timeit
import os.path
from twitter_zipfs_law import stem_words, remove_punctuation

root_path = r"/home/johankn/Dev/Documents-1/ScrapedData"

auth = tweepy.OAuthHandler("hthiIooKXUK1nN13UAH49ZOs2", "gWnJTNB3xy9nOrAUjTqdiQCIe3WxvgzQUZTD4EVXWT5uw0X9ju")
auth.set_access_token("1363777368519753729-dgXhlOUFQMt9OMDwZJhScjfaXOxuuO", "1SRoyDU4RNdEFsIBTC4305V76yWFFrH0Br23TCmSzjfBh")

api = tweepy.API(auth, wait_on_rate_limit=True, retry_count=10, retry_delay=10, retry_errors=set([104, 503]))

def get_appropriate_account(i):
    try:
        user = api.get_user(i)
    except tweepy.error.TweepError:
        return None
    else:
        try:
            friends = user.friends_count
        except tweepy.error.TweepError:
            return None
        else:
            if (friends > 99 and friends < 10000):
                return user

#run scan
#returns list of id as int
def account_scan(start_id=50000, size_of_result=10):
    check_id = start_id
    accounts = []
    while (len(accounts) < size_of_result):
        user = get_appropriate_account(check_id)
        if (user == None):
            check_id += 1
        else:
            accounts.append(check_id)
            check_id += 10000
    return accounts

def generate_account_csv(data:list, name):
    user_id_list = []
    user_name_list = []
    user_followers_count_list = []
    user_friends_count = []
    user_statuses_count = []
    user_likes_count = []
    for i in data:
        user_id_list.append(i)
        user = api.get_user(i)
        user_name_list.append(user.name)
        user_followers_count_list.append(user.followers_count)
        user_friends_count.append(user.friends_count)
        user_statuses_count.append(user.statuses_count)
        user_likes_count.append(user.favourites_count)
    user_list = {'id' : user_id_list,
        'name': user_name_list,
        'followers_count': user_followers_count_list,
        'friends_count' : user_friends_count,
        'statuses_count': user_statuses_count,
        'likes_count': user_likes_count
        }
    df = pd.DataFrame(user_list, columns=['id', 'name', 'followers_count', 'friends_count' , 'statuses_count', 'likes_count'])
    df.to_csv(root_path+"/Accounts/account_scan"+str(name)+".csv")
    print("Generated csv sheet successfully at " + root_path+"/Accounts/account_scan"+str(name)+".csv")

def csv_to_list(path):
    df = pd.read_csv(path)['friends_count'].values.tolist()
    return df

def get_friends_of_friends_count(id=50000, write_csv=True):
    friend_list_id = []
    friend_list_friends_count = []
    try:
        data_size = min(api.get_user(id).friends_count, 5000)
        friend_list = tweepy.Cursor(api.friends, id).items(data_size)
        for friend in friend_list:
            if (friend.friends_count > 0):
                friend_list_id.append(friend.id)
                friend_list_friends_count.append(friend.friends_count)
    except tweepy.TweepError as e:
        print("Something went wrong: " + str(e))
        return None
    friend_list = {
        'id' : friend_list_id,
        'friends_count' : friend_list_friends_count
    }
    if write_csv:
        df = pd.DataFrame(friend_list, columns=['id', 'friends_count'])
        df.to_csv(root_path+"/Friends/friend_scan"+str(id)+".csv")
        print("Generated csv sheet successfully at " + root_path+"/Friends/friend_scan"+str(id)+".csv")
    return friend_list_friends_count

def fof_scan(filename):
    id_list = pd.read_csv(root_path+"/Accounts/account_scan"+str(filename)+".csv")['id'].values.tolist()
    for i in id_list:
        if (os.path.isfile(root_path+"/Friends/friend_scan"+str(i)+".csv")):
            print("A file with user " + str(i)+ " already exists.")
        else:
            get_friends_of_friends_count(id=i)

#https://fairyonice.github.io/extract-someones-tweet-using-tweepy.html
def run_tweet_scan(id=50000):
    try:
        api.get_user(id=id)
        print('Found user')
    except tweepy.error.TweepError as error:
        print(error)
        return None
    tweets = api.user_timeline(id=id, 
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
        tweets = api.user_timeline(id=id, 
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

def generate_tweets_csv(data:list, id):
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
    df.to_csv(root_path+"/Tweets/tweet"+str(id)+".csv")
    print("Generated csv sheet successfully")

def word_scan(filename):
    id_list = pd.read_csv(root_path+"/Accounts/account_scan"+str(filename)+".csv")['id'].values.tolist()
    for i in id_list:
        if (os.path.isfile(root_path+"/Tweets/tweet"+str(i)+".csv")):
            print("A file with user " + str(i)+ " already exists.")
        else:
            try:
                tweets = run_tweet_scan(id=i)
                if tweets != None:
                    generate_tweets_csv(tweets, i)
            except tweepy.TweepError as error:
                print(error)
                continue

def run_full_scan(start_id=5375633):
    print("Full scan begun...")
    last_id = start_id
    while True:
        print("Retrieving accounts, starting from " + str(last_id))
        accounts = account_scan(start_id=last_id, size_of_result=50)
        start_id = last_id
        last_id = accounts[-1]
        print("Accounts retrieved")
        generate_account_csv(accounts, str(start_id) +"-"+ str(last_id))
        print("Friends of friends")
        fof_scan(str(start_id) +"-"+ str(last_id))
        print("Tweet scan")
        word_scan(str(start_id) +"-"+ str(last_id))
        last_id += 1
        for acc in accounts:
            print("Run scan for " +str(acc))


            print("Account finished")

#run_full_scan()
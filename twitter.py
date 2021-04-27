import tweepy
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import timeit



auth = tweepy.OAuthHandler("hthiIooKXUK1nN13UAH49ZOs2", "gWnJTNB3xy9nOrAUjTqdiQCIe3WxvgzQUZTD4EVXWT5uw0X9ju")
auth.set_access_token("1363777368519753729-dgXhlOUFQMt9OMDwZJhScjfaXOxuuO", "1SRoyDU4RNdEFsIBTC4305V76yWFFrH0Br23TCmSzjfBh")

api = tweepy.API(auth, wait_on_rate_limit=True, retry_count=10, retry_delay=10, retry_errors=set([503]))
#hello from local
def get_appropriate_account(i):
    try:
        user = api.get_user(i)
    except tweepy.error.TweepError:
        return None
    else:
        try:
            followers = user.followers_count
        except tweepy.error.TweepError:
            return None
        else:
            if (followers > 99):
                return user

#run scan
#returns list of id as int
def run_scan(start_id=50000, size_of_result=10):
    check_id = start_id
    accounts = []
    while (len(accounts) < size_of_result):
        user = get_appropriate_account(check_id)
        if (user == None):
            check_id += 1
        else:
            accounts.append(check_id)
            print(len(accounts))
            if (len(accounts) % 100 == 0):
                generate_excel(accounts)
            check_id += 10000
    return accounts

def benford_plot(data:list):
    digits = np.arange(1,10)
    digit_probs = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    data_length = len(data)
    for number in data:
        first_digit = int(str(number)[:1])
        digit_probs[first_digit-1] += 1 / data_length

    plt.rc('font', size=16)
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(digits, digit_probs)
    plt.xticks(digits)
    plt.xlabel('Digits')
    plt.ylabel('Probability')
    plt.title("Benford's Law: Probability of Leading Digits")
    plt.plot([1, 2, 3, 4, 5, 6, 7, 8, 9], [0.301, 0.176, 0.125, 0.097, 0.079, 0.067, 0.058, 0.051, 0.046], c='red')
    plt.show()

def generate_excel(data:list):
    user_screenname_list = []
    user_name_list = []
    user_followers_count_list = []
    user_following_count = []
    user_statuses_count = []
    user_likes_count = []
    for i in data:
        user_screenname_list.append(i)
        user = api.get_user(i)
        user_name_list.append(user.name)
        user_followers_count_list.append(user.followers_count)
        user_following_count.append(user.friends_count)
        user_statuses_count.append(user.statuses_count)
        user_likes_count.append(user.favourites_count)
    user_list = {'screen_name' : user_screenname_list,
        'name': user_name_list,
        'followers_count': user_followers_count_list,
        'following_count' : user_following_count,
        'statuses_count': user_statuses_count,
        'likes_count': user_likes_count
        }
    df = pd.DataFrame(user_list, columns=['screen_name', 'name', 'followers_count', 'following_count' , 'statuses_count', 'likes_count'])
    df.to_csv(r"/home/johankn/Documents/test6.csv")
    print("Generated csv sheet successfully")

def excel_to_list(name):
    df = pd.read_excel(r"C:\Users\johan\OneDrive - Aarhus universitet\UNI\3 år\bachelor\Implementering\list" + str(name) + ".xlsx")['followers_count'].values.tolist()
    return df
def csv_to_list(name):
    df = pd.read_csv(name)['followers_count'].values.tolist()
    return df

def get_friends_of_friends_count(screen_name=50000, write_csv=True):
    start_time = timeit.default_timer()
    screen_name_list = pd.read_excel(r"C:\Users\johan\OneDrive - Aarhus universitet\UNI\3 år\bachelor\Implementering\test.xlsx")['screen_name'].values.tolist()
    if screen_name in screen_name_list:
        friend_screen_name = []
        friend_followers_count = []
        data_size = min(api.get_user(screen_name).followers_count, 5000)
        for follower in tweepy.Cursor(api.followers, screen_name).items(data_size):
            if (follower.followers_count > 0):
                friend_screen_name.append(follower.screen_name)
                friend_followers_count.append(follower.followers_count)
        friend_list = {
            'screen_name' : friend_screen_name,
            'followers_count' : friend_followers_count
        }
        if write_csv:
            df = pd.DataFrame(friend_list, columns=['screen_name', 'followers_count'])
            df.to_csv(r"/home/johankn/Documents/fof"+str(screen_name)+".csv")
        stop_time = timeit.default_timer()
        print('Time: ', stop_time - start_time)
        return friend_followers_count
    else:
        print("Error, screen name not found")
        return None

generate_excel(run_scan(start_id=93647534 ,size_of_result=5000))

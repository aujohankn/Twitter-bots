# Modified version, taken from https://realpython.com/pysimplegui-python/

from os import error
import PySimpleGUI as sg
import os.path
import pandas as pd
import webbrowser

import twitter_benfords_law as bl
import twitter_zipfs_law as zl
import twitter_timemaps as tm
import twitter_auth as ta

api = ta.get_api('hthiIooKXUK1nN13UAH49ZOs2', 'gWnJTNB3xy9nOrAUjTqdiQCIe3WxvgzQUZTD4EVXWT5uw0X9ju',
                '1363777368519753729-dgXhlOUFQMt9OMDwZJhScjfaXOxuuO', '1SRoyDU4RNdEFsIBTC4305V76yWFFrH0Br23TCmSzjfBh')

path = os.getcwd()+"\ScrapedData\\"

def get_users_values():
    # Returns all data gathered from twitter_scraper.py
    file_list = os.listdir(path+'\Accounts\\')
    data = pd.DataFrame()
    data_total_score = []
    data_benford_score = []
    data_zipf_score = []
    data_time_score = []
    scores = pd.read_csv(path+"Scores\score_scan.csv")
    scores_ids = scores['id'].values.tolist()
    for file in file_list:
        new_data = pd.read_csv(path+'\Accounts\\' + file)
        for index, row in new_data.iterrows():
            userID = row[1]
            if (os.path.isfile(path+"\Friends\\friend_scan"+str(userID) + ".csv") and
            os.path.isfile(path+"\Tweets\\tweet"+str(userID) + ".csv")):
                #If a score has been generated for this user
                if userID in scores_ids:
                    if scores.loc[scores_ids.index(userID)][2] > 0:
                        data_total_score.append(scores.loc[scores_ids.index(userID)][2])
                        data_benford_score.append(scores.loc[scores_ids.index(userID)][3])
                        data_zipf_score.append(scores.loc[scores_ids.index(userID)][4])
                        data_time_score.append(scores.loc[scores_ids.index(userID)][5])
                        data = data.append(new_data.loc[[index]], ignore_index=True)
    data['total_score'] = data_total_score
    data['benford_score'] = data_benford_score
    data['zipf_score'] = data_zipf_score
    data['time_score'] = data_time_score
    data = data.sort_values(by='total_score', ascending=False, ignore_index=True)
    return data

def go_to_twitter_page(userID):
    # Simply opens an internet brower with the twitter link
    # Uses webbrowser package
    # Note: This function does not currently work because of api setup
    try:
        user = api.get_user(userID)
        link = webbrowser.open("https://twitter.com/"+str(user.screen_name))
    except:
        print("Unable to go to website")
        sg.Popup("Unable to go to website")
        return None

# --------------------------------- Define Layout ---------------------------------

users_values = get_users_values()
# List of users
account_list_col = [[sg.Text('List of Accounts')],[sg.Listbox(values=users_values['name'], enable_events=True, size=(40,20),key='-ACCOUNT LIST-')]]

account_info_list_col = [[sg.Text('Account Information')],
                        [sg.Text(size=(40,20),key='-ACCOUNT INFO LIST-')],
                        [sg.Button('Generate Benford', disabled=True)],
                        [sg.Button('Generate Zipf', disabled=True)],
                        [sg.Button('Generate Time Map', disabled=True)],
                        [sg.Button('Go to Twitter page', disabled=True)]]

# For now will only show the name of the file that was chosen
images_col = [[sg.Text('You choose from the list:')],
              [sg.Text(size=(40,1), key='-TOUT-')],
              [sg.Image(key='-IMAGE-')]]

# ----- Full layout -----
layout = [[sg.Column(account_list_col, element_justification='c'), sg.VSeperator(),sg.Column(account_info_list_col, element_justification='c')]]

# --------------------------------- Create Window ---------------------------------
window = sg.Window('Automated Social Media Account Detector', layout,resizable=True)

# ----- Run the Event Loop -----
# --------------------------------- Event Loop ---------------------------------
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == '-ACCOUNT LIST-':    # A file was chosen from the listbox
        try:
            names = users_values['name'].values.tolist()
            n = values['-ACCOUNT LIST-'][0]
            index = names.index(n)
            current_account = users_values.values.tolist()[index]
            vlist = []
            current_account_id = current_account[1]

            if (os.path.isfile(path+"\Friends\\friend_scan"+str(current_account_id) + ".csv")):
                window['Generate Benford'].update(disabled=False)
            else:
                window['Generate Benford'].update(disabled=True)
            if (os.path.isfile(path+"\Tweets\\tweet"+str(current_account_id) + ".csv")):
                window['Generate Zipf'].update(disabled=False)
                window['Generate Time Map'].update(disabled=False)
            else:
                window['Generate Zipf'].update(disabled=True)
                window['Generate Time Map'].update(disabled=True)

            window['Go to Twitter page'].update(disabled=False)

            vlist.append("ID: " + str(current_account[1]) + '\n')
            vlist.append("Name: " + str(current_account[2]) + '\n')
            vlist.append("Followers: " + str(current_account[3]) + '\n')
            vlist.append("Following: " + str(current_account[4]) + '\n')
            vlist.append("Tweets: " + str(current_account[5]) + '\n')
            vlist.append("Likes: " + str(current_account[6]) + '\n')
            vlist.append("\n")
            vlist.append("Total Score: " + str(round(current_account[7],2)) + '\n')
            vlist.append("Benford Score: " + str(round(current_account[8],2)) + '\n')
            vlist.append("Zipf Score: " + str(round(current_account[9],2)) + '\n')
            vlist.append("Time Score: " + str(round(current_account[10],2)) + '\n')
            window['-ACCOUNT INFO LIST-'].update("".join(vlist))
        except Exception as E:
            print(f'** Error {E} **')
            pass        # something weird happened making the full filename
    elif event == 'Generate Benford':
        if not values['-ACCOUNT LIST-']:
            pass
        else:
            try:
                bl.load_and_benford_plot(current_account_id)
            except Exception as E:
                sg.Popup("Unable to load account information")
                pass
    elif event == 'Generate Zipf':
        if not values['-ACCOUNT LIST-']:
            pass
        else:
            try:
                zl.load_and_zipf_plot(current_account_id)
            except error as e:
                print(e)
                sg.Popup("Unable to load tweets")
                pass
    elif event == 'Generate Time Map':
        if not values['-ACCOUNT LIST-']:
            pass
        else:
            try:
                tm.heatmap_plot(current_account_id)
            except error as e:
                print(e)
                sg.Popup("Unable to load tweets")
                pass
            except ValueError as e:
                print(e)
                sg.Popup(e)
                pass

    elif event == 'Go to Twitter page':
        go_to_twitter_page(current_account_id)
# --------------------------------- Close & Exit ---------------------------------
window.close()
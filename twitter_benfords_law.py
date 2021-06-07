import os
import matplotlib.pyplot as plt
import numpy as np

from twitter_scraper import csv_to_list

def benford_plot(data:list):
    # Inspired by/from https://www.learndatasci.com/glossary/benfords-law/
    # Draws the Benford's law distribution from a dataset of friends' of friends
    # Also draws the expected distribution
    # Input: List of friends' friend count
    # Returns nothing
    digits = np.arange(1,10)
    digit_probs = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    digit_count = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    data_length = len(data)
    for number in data:
        first_digit = int(str(number)[:1])
        digit_probs[first_digit-1] += 1 / data_length
        digit_count[first_digit-1] += 1
    plt.rc('font', size=16)
    fig, ax = plt.subplots(figsize=(12, 6))
    ud = ax.bar(digits, digit_probs)
    for i, d in enumerate(digit_probs):
        plt.text(i+.8,d+.005,digit_count[i], rotation=45)
    ud.set_label("User Data")
    plt.yticks([0, .05, .1, .15, .2, .25, .3, .35, .4, .45])
    ax.set_yticklabels(["0%", "5%", "10%", "15%", "20%", "25%", "30%", "35%", "40%", "45%"])
    plt.xticks(digits)
    plt.xlabel('Digits')
    plt.ylabel('Distribution in %')
    plt.title("Benford's Law")
    bnf, = ax.plot([1, 2, 3, 4, 5, 6, 7, 8, 9], [0.301, 0.176, 0.125, 0.097, 0.079, 0.067, 0.058, 0.051, 0.046], c='red')
    bnf.set_label("Benford's Law")
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.5,)
    plt.legend()
    plt.tight_layout()
    plt.show()

def load_and_benford_plot(userID):
    # Function for gui, simply runs the two functions in sequence
    path = os.getcwd()+"\ScrapedData\Friends\\"
    list = csv_to_list(path+"friend_scan"+str(userID)+".csv")
    benford_plot(list)

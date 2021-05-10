import tweepy
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import timeit
import os.path
import nltk
import string
import re
import os.path

import twitter

api = twitter.api

for i in range(50000,110000):
    try: 
        twitter.benford_plot(twitter.csv_to_list(r"C:\Users\johan\OneDrive - Aarhus universitet\UNI\3 år\bachelor\Ny mappe\Documents\fof" + str(i) + ".csv"), screen_name=i)
    except FileNotFoundError as error:
        continue
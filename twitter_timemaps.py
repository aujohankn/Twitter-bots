import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import datetime
import tm_tools

def heatmap_plot(userID):
    df = pd.read_csv(r"C:\Users\johan\OneDrive - Aarhus universitet\UNI\3 år\bachelor\Ny mappe\Documents\ScrapedData\Tweets\tweet" + str(userID) + ".csv")['created_at'].values.tolist()
    tm_tools.analyze_tweet_times(str(userID), df)
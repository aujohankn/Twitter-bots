import os
import pandas as pd
import tm_tools

def heatmap_plot(userID):
    # Reads the tweet timestamps from a specific Twitter account and generates the heated time map
    print("Heatmap plot")
    df = pd.read_csv(os.getcwd()+"\ScrapedData\Tweets\tweet" + str(userID) + ".csv")['created_at'].values.tolist()
    tm_tools.analyze_tweet_times(str(userID), df)
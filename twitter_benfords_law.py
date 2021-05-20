import matplotlib.pyplot as plt
import numpy as np
from twitter_scraper import csv_to_list

def benford_plot(data:list, id=""):
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
    plt.title("Benford's Law: User " + str(id) +" with " + str(data_length) + " friends.")
    plt.plot([1, 2, 3, 4, 5, 6, 7, 8, 9], [0.301, 0.176, 0.125, 0.097, 0.079, 0.067, 0.058, 0.051, 0.046], c='red')
    plt.show()

def load_and_benford_plot(userID):
    list = csv_to_list(r"C:\Users\johan\OneDrive - Aarhus universitet\UNI\3 år\bachelor\Ny mappe\Documents\Fof csv files\fof"+str(userID)+".csv")
    benford_plot(list,userID)
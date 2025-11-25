# nltk try
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import IPython
nltk.download("vader_lexicon")
from transformers import pipeline

import subprocess

class ollama_start:
    def __init__ self:



sia = SentimentIntensityAnalyzer()              # nltk
sentiment = pipeline("sentiment-analysis",      # transformers 
                     model="cardiffnlp/twitter-roberta-base-sentiment-latest")


def nltk_sent():
    intext = "Good morning, you seem well!"
    while intext:
        print(f"Input is: {intext}")
        siascores = sia.polarity_scores(intext)
        print(f"{siascores=}")
        pipescores = sentiment(intext)
        print(f"{pipescores=}")
        intext = input("Input intext <enter to end>:")


if __name__ == "__main__":
    nltk_sent()
    proc = subprocess(["ollama", "serve"])
    time.sleep(5)
    proc

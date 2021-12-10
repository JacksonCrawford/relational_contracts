import csv
import re
import json
from pathlib import Path
from word_cleaner import word_cleaner
from stopwords import stopword_generator

from collections import defaultdict
from gensim import corpora, models

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# Initialize dictionaries of hyposet and new_word objects
hyposets = list()
new_words = list()

# Initialize stopword_generator object
stopper = stopword_generator()
# Store the set of stopwords
english_stops = stopper.get_stopwords()

# Initialize the word_cleaner object
cleaner = word_cleaner()


# Method to get all the articles (currently from the first day of May 1998 data
def get_data():
    # folder = Path("/home/jacksoncrawford/cs/relational_contracts/nlp/2000/").rglob("*.json")
    # folder = Path("/home/jacksoncrawford/cs/relational_contracts/nlp/1999/").rglob("*.json")
    # folder = Path("/home/jacksoncrawford/cs/relational_contracts/nlp/test_articles/").rglob("*.json")
    # files = [file for file in folder]
    # text_list = list()

    # Iterate through files
    # for file in files:
        # Open filejj
    #     with open(file, "r") as infile:
            # Append contents to text_list
    #         text_list.append(json.loads(infile.read()))

    # text_list = [text["text"] for text in text_list]

    text_list = list()

    with open("/home/jacksoncrawford/cs/relational_contracts/nlp/test_articles/wired_article_01.01.1995_0716.json", "r") as infile:
        text_list.append(infile)
    with open("/home/jacksoncrawford/cs/relational_contracts/nlp/test_articles/wired_article_04.01.1995_0547.json", "r") as infile:
        text_list.append(infile)
    with open("/home/jacksoncrawford/cs/relational_contracts/nlp/test_articles/wired_article_06.01.1995_0468.json", "r") as infile:
        text_list.append(infile)

    return text_list

# Store article data from get_data() in articles
articles = get_data()

def generate_frequencies():
    frequency = defaultdict(int)
    for text in articles:
        for token in text:
            frequency[token] += 1

    return frequency


def generate_corpus(frequency):
    texts = [
        [token for token in text if frequency[token] > 1]
        for text in articles
    ]


    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    tfdif = models.TfidfModel(corpus) # Initialize a model

    corpus_tfdif = tfdif[corpus]

    lsi_model = models.LsiModel(corpus_tfdif, id2word=dictionary, num_topics=2)
    corpus_lsi = lsi_model[corpus_tfdif]
    lsi_model.print_topics(2)

    return corpus_lsi

def main():
    frequencies = generate_frequencies()
    corpus = generate_corpus(frequencies)

main()

    

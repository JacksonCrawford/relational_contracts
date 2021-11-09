from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
import csv
import re
import json
from collections import OrderedDict
from pathlib import Path


# TODO: Refactor topics to word frequency evaluator
# TODO: Finish weight system
# TODO: Implement hypernym evaluator

# Initialize dict of topics and list or articles
topics = dict()
definitions = list()
hypernyms = dict()

# Get the nltk bundled stopwords and add some of my own
def get_stopwords():
    stops = set(stopwords.words("english"))

    stops.add("one")
    stops.add("two")
    stops.add("three")
    stops.add("four")
    stops.add("five")
    stops.add("six")
    stops.add("seven")
    stops.add("eight")
    stops.add("nine")
    stops.add("ten")
    stops.add("ours")
    stops.add("our")
    stops.add("would")
    stops.add("could")
    stops.add("should")
    stops.add("said")
    stops.add("like")
    stops.add("also")
    stops.add("says")
    stops.add("percent")
    stops.add("first")
    stops.add("get")

    return stops

# Set of stopwords
english_stops = get_stopwords()


# Remove all non-alphanumeric characters
# TODO: Hyphens
# TODO: 's
def clean(word):
    code = 0
    for letter in word:
        code = ord(letter)
        if code < 65 or code > 122 or (code > 90 and code < 97):
            word = word.replace(letter, "")

    return word


# Get all the articles (currently from the first day of May 1998 data
def get_data():
    folder = Path("/home/jacksoncrawford/cs/relational_contracts/nlp/2000/").rglob("*.json")
    files = [file for file in folder]
    article_num = 1
    article_num_f = f"{article_num:03}"
    articulos = list()

#    for i in range(len(files)):
    for file in files:
        with open(file, "r") as infile:
            articulos.append(json.loads(infile.read()))

        article_num += 1
        article_num_f = f"{article_num:03}"

    
    return articulos
#    return [[articulo["heading"] for articulo in articulos], [articulo["text"] for articulo in articulos]]

articles = get_data()

# Add a word to toipcs if it is not already there. If it is, increment by weight
def add_to_topics(word, weight):
    if word not in topics:
        topics[word] = 1
    else:
        topics[word] += 1

# Add a word to hypernyms if it is not already there. If it is, increment by weight
def add_to_hypernyms(word, weight):
    if word not in hypernyms:
        hypernyms[word] = weight
    else:
        hypernyms[word] += weight


# Sort the topics dictionary by value and print the top twenty-five
def top_topics():
    sorted_synms = dict(reversed(sorted((value, key) for (key, value) in topics.items())))

    print("Word  :  Weight")
    count = 0

    f = open("word_count.csv", "w")
    writer = csv.writer(f)
    writer.writerow(["Word", "Weight by occurence"])

    for key, value in sorted_synms.items():
        print(value, ":", key)
        writer.writerow([value, key])
        count += 1

        if count == 25:
            break

    f.close()

# Sort the topics dictionary by value and print the top twenty-five
def top_hypernyms():
    sorted_topics = dict(reversed(sorted((value, key) for (key, value) in hypernyms.items())))
    print("\nhypernym  :  Weight")
    count = 0

    f = open("hypernym.csv", "w")
    writer = csv.writer(f)
    writer.writerow(["Hypernym", "Weight by occurence"])

    for key, value in sorted_topics.items():
        print(value, ":", key)
        writer.writerow([value, key])
        count += 1

        if count == 25:
            break

    f.close()

# Method to analyze an article's header
def analyze_header(header):
    header_text = header.split()
    header_text = [clean(word) for word in header_text if clean(word) != ""]
    header_text = [word for word in header_text if word not in english_stops]

    hns = list()

    for word in header_text:
        try:
            add_to_topics(word, 4)
            syn = wn.synsets(word)[0]
            definitions.append(syn.definition()[0])
            
            add_to_hypernyms(syn.hypernyms()[0], 4)
        except:
            definitions.append("")


# Method to analyze an article's text
def analyze_article_text(article):
    text = article.split()
    text = [clean(word) for word in text if clean(word) != ""]
    text = [word for word in text if word not in english_stops]

    hns = list()

    for word in text:
        try:
            add_to_topics(word, 1)
            syn = wn.synsets(word)[0]
            definitions.append(syn.definition()[0])

            add_to_hypernyms(syn.hypernyms()[0], 1)
        except:
            definitions.append("")

    text = [clean(word) for word in text if clean(word) != ""]


# Main method
def main():
    articles = get_data()
    
    text = str()

    for article in articles:
        analyze_header(article["heading"])
        analyze_article_text(article["text"])

    top_topics()
    top_hypernyms()

if __name__=="__main__":
    main()

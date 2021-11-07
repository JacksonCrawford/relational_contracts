from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
import re
import json
from collections import OrderedDict

# Initialize dict of topics and list or articles
topics = dict()
articles = list()

# Remove all non-alphanumeric characters (but replace "-" with a space)
def clean(word):
    word = word.replace("-", " ")
    code = 0
    for letter in word:
        code = ord(letter)
        if code < 65 or code > 122 or (code > 90 and code < 97):
            word = word.replace(letter, "")

    return word


# Get all the articles (currently from the first day of May 1998 data
def get_data():
    article_num = 1
    article_num_f = f"{article_num:03}"

    files = list()

    for i in range(82):
        with open("may_1998/wired_article_05.01.1998_" + article_num_f + ".json", "r") as infile:
            files.append(json.loads(infile.read()))

        article_num += 1
        article_num_f = f"{article_num:03}"
    
    return [file["text"] for file in files]


# Add a word to toipcs if it is not already there. If it is, increment value
def add_to_topics(word):
    if word not in topics:
        topics[word] = 1
    else:
        topics[word] += 1


# Sort the topics dictionary by value and print the top twenty-five
def top_topics():
    sorted_topics = dict(reversed(sorted((value, key) for (key, value) in topics.items())))

    print("Topic  :  # of Occurrences")
    count = 0
    for key, value in sorted_topics.items():
        print(value, ":", key)
        count += 1

        if count == 25:
            break


# Get the nltk bundled stopwords and add some of my own
def get_stopwords():
    stops = set(stopwords.words("english"))

    stops.append("one")
    stops.append("two")
    stops.append("three")
    stops.append("four")
    stops.append("five")
    stops.append("six")
    stops.append("seven")
    stops.append("eight")
    stops.append("nine")
    stops.append("ten")
    stops.append("ours")
    stops.append("our")
    stops.append("would")
    stops.append("could")
    stops.append("should")
        

# Main method
def main():
    articles = get_data()

    english_stops = set(stopwords.words("english"))
    definitions = list()
    
    text = str()

    for article in articles:
        text = article.split()
        text = [clean(word) for word in text if clean(word) != ""]
        text = [word for word in text if word not in english_stops]

        for word in text:
            try:
                add_to_topics(word)
                definitions.append(wn.synsets(word)[0].definition())
            except:
                definitions.append("")

        text = [clean(word) for word in text if clean(word) != ""]

    top_topics()

main()

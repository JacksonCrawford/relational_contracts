from nltk.corpus import wordnet as wn
import csv
import re
import json
from collections import OrderedDict
from pathlib import Path
from hyposet import hyposet
from new_word import new_word
from word_cleaner import word_cleaner
from stopwords import stopword_generator
from hypernym import hypernym


# Initialize dictionaries of hyposet and new_word objects
new_words = list()
hypernyms = list()

months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]

# Initialize stopword_generator object
stopper = stopword_generator()
# Store the set of stopwords
english_stops = stopper.get_stopwords()

# Initialize the word_cleaner object
cleaner = word_cleaner()

# Method to get all the articles (currently from the first day of May 1998 data
def get_data():
    folder = Path("/home/jacksoncrawford/cs/relational_contracts/nlp/1999/").rglob("*.json")
    # folder = Path("/home/jacksoncrawford/cs/relational_contracts/nlp/test_articles/").rglob("*.json")
    files = [file for file in folder]
    text_list = list()

    # Iterate through files
    for file in files:
        # Open file
        with open(file, "r") as infile:
            # Append contents to text_list
            text_list.append(json.loads(infile.read()))

    return text_list

# Store article data from get_data() in articles
articles = get_data()

# Method to get the keys for sorting the hypernyms list
def get_sorter_key_hyp(hyp):
    return hyp.get_count()

# Method to get the keys for sorting the new_words list
def get_sorter_key_nw(new_word):
    return new_word.get_count()

# Method to check if new_words contains an argued new_word
def new_words_contains(word):
    # Counter for returning index
    index = 0
    for new_word in new_words:
        # If argued word is in new_words, return the index
        if new_word.get_word() == word:
            return index
        index += 1

    # If word was not found, return -1
    return -1

# Method to check if hyponyms contains an argued hypernym
def hypernyms_contains(hypernym):
    # Counter for returning index
    index = 0
    for obj in hypernyms:
        # If hypernym is in hyposets, return the index
        if obj.get_hypernym() == hypernym:
            return index
        index += 1

    # If hypernym was not found, return -1
    return -1

# Method to display the top 25 hyposets and store them in a json
def top_hypernyms():
    # Sort the hyposets by the count (frequency)
    hypernyms.sort(key=get_sorter_key_hyp)
    hypernyms.reverse()

    count = 0
    top_ten = list()
    for hypernym in hypernyms:
        top_ten.append(hypernym.get_hypernym())

        count += 1

        # Terminate loop if count is 25
        if count == 10:
            break

    # Print heading
    print("\nhypernym  :  Weight")
    count = 0
    with open("hypernym_occurences.csv", "w") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(top_ten)
        # Loop through hyposets
        for hypernym in hypernyms:
            # Print the hypernym
            print("\n", hypernym.get_hypernym())
            writer.writerow(hypernym.get_occurences())

            count += 1

            # Terminate loop if count is 25
            if count == 10:
                break

# Method to display the top 25 new_words and store them in a json
def top_new_words():
    # Sort the new_words by the count (frequency)
    new_words.sort(key=get_sorter_key_nw)
    new_words.reverse()

    count = 0
    top_ten = list()
    for new_word in new_words:
        top_ten.append(new_word.get_word())

        count += 1

        # Terminate loop if count is 25
        if count == 50:
            break

    # Print heading
    print("\nnew_word  :  Weight")
    count = 0

    with open("new_word_occurences.csv", "w") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(top_ten)
        # Loop through new_words
        for new_word in new_words:
            # Print the root word
            print("\n", new_word.get_word());
            writer.writerow(new_word.get_occurences())

            count += 1

            # Terminate loop if count is 25
            if count == 50:
                break

# Method to analyze an article's text
def hypernyms_over_time(article, timestamp):
    # Split the article's text and store it in text
    text = article.split()
    # Clean text and remove stopwords
    text = [cleaner.clean(word) for word in text if cleaner.clean(word) != ""]
    text = [word for word in text if word not in english_stops]

    month = timestamp[0:2:]

    # Loop through each word in text
    for word in text:
        try:
            syn = wn.synsets(word)[0]
            # Store synset of word in syn
            # syn = wn.synsets(word)[0]
            # Get hypernym of syn
            # hyp = syn.hypernyms()[0]
            # Get index of hypernym in hyposets
            # contains = hypernyms_contains(hyp)

            # If it already exists in hyposets, add its synset and add the word
            # if(contains > 0):
            #     hypernyms[contains].add_occurence(month)
            # else: # If it does not exist in hyposets, create it (along with synset and word)
            #     obj = hypernym(hyp, month)
            #     hypernyms.append(obj)
        except IndexError as err: # Catch error for a word not in WordNet
            # Get index of word in new_words
            contains = new_words_contains(word)

            # If it already exists in new_words, add its previous word
            if(contains > 0):
                new_words[contains].add_occurence(month)
            else: # If it does not exist in new_words, add it (along with previous word)
                obj = new_word(word)
                obj.add_occurence(month)
                new_words.append(obj)
        except KeyError as kerr:
            pass

        # Set word to be prev_word at end of loop iteration
        prev_word = word


# Main method
def main():
    for article in articles:
        hypernyms_over_time(article["text"], article["timestamp"])

    # top_hypernyms()
    top_new_words()


if __name__=="__main__":
    main()

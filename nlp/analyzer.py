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
    folder = Path("/home/jacksoncrawford/cs/relational_contracts/nlp/test_articles/").rglob("*.json")
    files = [file for file in folder]
    text_list = list()

    # Iterate through files
    for file in files:
        # Open filejj
        with open(file, "r") as infile:
            # Append contents to text_list
            text_list.append(json.loads(infile.read()))

    return text_list

# Store article data from get_data() in articles
articles = get_data()

# Method to get the keys for sorting the hyposets list
def get_sorter_key_hyp(hyposet):
    return hyposet.get_count()

# Method to get the keys for sorting the new_words list
def get_sorter_key_nw(new_word):
    return new_word.get_count()

# Method to check if hyponyms contains an argued hypernym
def hyposets_contains(hypernym):
    # Counter for returning index
    index = 0
    for hyposet in hyposets:
        # If hypernym is in hyposets, return the index
        if hyposet.get_hypernym() == hypernym:
            return index
        index += 1

    # If hypernym was not found, return -1
    return -1

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

# Method to display the top 25 hyposets and store them in a json
def top_hyposets():
    # Sort the hyposets by the count (frequency)
    hyposets.sort(key=get_sorter_key_hyp)
    hyposets.reverse()

    # Print heading
    print("\nhypernym  :  Weight")
    count = 0
    # Loop through hyposets
    for hyposet in hyposets:
        # Print the hypernym
        print("\n", hyposet.get_hypernym(), ":", hyposet.get_count())


        # Print the synsets
        print("\t|->", hyposet.get_synsets())
        count += 1

        # Terminate loop if count is 25
        if count == 50:
            break

# Method to display the top 25 new_words and store them in a json
def top_new_words():
    # Sort the new_words by the count (frequency)
    new_words.sort(key=get_sorter_key_nw)
    new_words.reverse()

    # Print heading
    print("\nnew_word  :  Weight")
    count = 0
    # Loop through new_words
    for new_word in new_words:
        # Print the root word
        print("\n", new_word.get_word(), ":", new_word.get_count());
        # Print associated words (preceding in text)
        print("\t|->", new_word.get_prev_words())
        count += 1

        # Terminate loop if count is 25
        if count == 25:
            break

# Method to analyze an article's text
def analyze_article_text(article):
    # Split the article's text and store it in text
    text = article.split()
    # Clean text and remove stopwords
    text = [cleaner.clean(word) for word in text if cleaner.clean(word) != ""]
    text = [word for word in text if word not in english_stops]

    # Initialize prev_word variable for storing previous word in loop
    prev_word = str()

    # Loop through each word in text
    for word in text:
        try:
            # Store synset of word in syn
            syn = wn.synsets(word)[0]
            # Get hypernym of syn
            hypernym = syn.hypernyms()[0]
            # Get index of hypernym in hyposets
            contains = hyposets_contains(hypernym)

            # If it already exists in hyposets, add its synset and add the word
            if(contains > 0):
                hyposets[contains].add_synset(syn)
                hyposets[contains].add_word(word)
                hyposets[contains].inc_count()
            else: # If it does not exist in hyposets, create it (along with synset and word)
                obj = hyposet(syn.hypernyms()[0])
                obj.add_synset(syn)
                obj.add_word(word)
                hyposets.append(obj)
        except IndexError as err: # Catch error for a word not in WordNet
            pass
            # Get index of word in new_words
            contains = new_words_contains(word)

            # If it already exists in new_words, add its previous word
            if(contains > 0):
                new_words[contains].add_prev_word(prev_word)
                new_words[contains].inc_count()
            else: # If it does not exist in new_words, add it (along with previous word)
                obj = new_word(word)
                obj.add_prev_word(prev_word)
                new_words.append(obj)
        except KeyError as kerr:
            pass

        # Set word to be prev_word at end of loop iteration
        prev_word = word

    # Clean text again
    text = [cleaner.clean(word) for word in text if cleaner.clean(word) != ""]


# Main method
def main():
    # Analyze every article
    for article in articles:
        analyze_article_text(article["text"])

    # Print the top hyposets and new_words (and sorting the lists)
    top_hyposets()
    top_new_words()

    # Open output/hyposet_results.json
    with open("output/hyposet_results.json", "w") as outfile:
        # Initialize lists for storing hyposets and new_words
        top_twentyfive_hyp = list()

        count = 0

        # Loop through first 25 hyposets
        for hyposet in hyposets:
            # Add json dict to list
            top_twentyfive_hyp.append(hyposet.get_json())

            count += 1
            if count == 25:
                break

        json.dump(top_twentyfive_hyp, outfile)

    # Open output/new_word_results.json
    with open("output/new_word_results.json", "w") as outfile:
        # Initialize lists for storing hyposets and new_words
        top_twentyfive_nw = list()

        count = 0

        # Loop through first 25 hyposets
        for new_word in new_words:
            # Add json dict to list
            top_twentyfive_nw.append(new_word.get_json())

            count += 1
            if count == 25:
                break

        # Dump into json
        json.dump(top_twentyfive_nw, outfile)

if __name__=="__main__":
    main()

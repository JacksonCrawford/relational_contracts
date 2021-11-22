import json

class hyposet:
    # Constructor
    def __init__(self, hyp):
        # Store argued hypernym
        self.hypernym = hyp
        # Set count to 1
        self.count = 1
        # Store synsets
        self.synsets = dict()
        # Store words
        self.words = dict()

    # Method to add synset to synsets (or increment count if it already exists)
    def add_synset(self, synset):
        # Store synset as just its name (type string)
        syn = synset.name()

        # If syn is already in synsets
        if syn in self.synsets:
            # Increment it
            self.synsets[syn] += 1
        else:
            # Add syn to synsets
            self.synsets[syn] = 1

        return True

    # Method to add word to words (or increment count if it already exists)
    def add_word(self, word):
        # If words is already in synsets
        if word in self.words:
            # Increment it
            self.words[word] += 1
        else:
            # Add word to words
            self.words[word] = 1

        return True


    # Method to increment count
    def inc_count(self):
        self.count += 1
        return True

    # Method to get the hypernym
    def get_hypernym(self):
        return self.hypernym

    def get_hypernym_str(self):
        return self.hypernym.name()

    # Method to get the synsets
    def get_synsets(self):
        return self.synsets

    # Method to get the synsets
    def get_synset_count(self, syn):
        return self.synsets[syn]

    # Method to get the words
    def get_words(self):
        return self.words

    # Method to get the count
    def get_count(self):
        return self.count

    # Method to get the dictionary for storing in JSON
    def get_json(self):
        return {"hypernym": self.hypernym.name(), "synsets": self.synsets, "words": self.words}
    

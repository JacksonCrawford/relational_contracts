class new_word:
    # Constructor
    def __init__(self, wrd):
        # Store argued word
        self.word = wrd
        # Store previous words
        self.prev_words = dict()
        # Store count
        self.count = 1

    # Method to add previous words to prev_words (or increment count if it already exists)
    def add_prev_word(self, prev_word):
        # If prev_word is already in prev_words
        if prev_word in self.prev_words:
            # Increment it
            self.prev_words[prev_word] += 1
        else:
            # Add prev_word to prev_words
            self.prev_words[prev_word] = 1

        return True

    # Method to increment count
    def inc_count(self):
        self.count += 1
        return True

    # Method to get the count
    def get_count(self):
        return self.count

    # Method to get the word
    def get_word(self):
        return self.word

    # Method to get the prev_words
    def get_prev_words(self):
        return self.prev_words

    # Method to get the dictionary for storing in JSON
    def get_json(self):
        return {"unique word": self.word, "count": self.count}

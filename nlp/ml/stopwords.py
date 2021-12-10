from nltk.corpus import stopwords

class stopword_generator:
    # Constructor
    def __init__(self):
        # Get NLTK stopwords
        self.stops = set(stopwords.words("english"))

        # Add my own stopwords
        self.stops.add("one")
        self.stops.add("two")
        self.stops.add("three")
        self.stops.add("four")
        self.stops.add("five")
        self.stops.add("six")
        self.stops.add("seven")
        self.stops.add("eight")
        self.stops.add("nine")
        self.stops.add("ten")
        self.stops.add("ours")
        self.stops.add("our")
        self.stops.add("would")
        self.stops.add("could")
        self.stops.add("should")
        self.stops.add("said")
        self.stops.add("like")
        self.stops.add("also")
        self.stops.add("says")
        self.stops.add("percent")
        self.stops.add("first")
        self.stops.add("get")

    def get_stopwords(self):
        return self.stops

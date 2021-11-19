# TODO: Hyphens and 's
class word_cleaner():
    def __init__(self):
        self.word = str()

    # Remove all non-alphanumeric characters
    def clean(self, word):
        code = 0
        for letter in word:
            code = ord(letter)
            if code < 65 or code > 122 or (code > 90 and code < 97):
                word = word.replace(letter, "")

        return word

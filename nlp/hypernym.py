class hypernym():
    def __init__(self, word, month):
        self.word = word
        # self.months = {"01": 0, "02": 0, "03": 0, "04": 0, "05": 0, "06": 0, "07": 0"08": 0, "09": 0, "10": 0, "11": 0, "12": 0}
        self.months = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.months[int(month)] = 1
        self.count = 1

    def add_occurence(self, month):
        if(month[0] == "0"):
            self.months[int(month[1])-1] += 1
        else:
            self.months[int(month)-1] += 1

        # self.months[month] += 1
        self.count += 1
        return True

    def get_hypernym(self):
        return self.word

    def get_occurences(self):
        return self.months

    def get_count(self):
        return self.count

    def get_json(self):
        return {"word": self.word, "month": self.month}

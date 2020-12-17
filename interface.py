import requests
from bs4 import BeautifulSoup

page = requests.get("https://www.wired.com/sitemap/")
soupLinks = BeautifulSoup(page.text, "lxml")
links = soupLinks.find(class_="sitemap__section-archive")

aTags = links.find_all("a")
firstLink = str(aTags[0].contents[0])
yearDex = firstLink.find("=") + 1
current = int(firstLink[yearDex:yearDex + 4:])

options = {"year": 1992, "blacklist": list(), "num": 0, "keywords": str(),
"timer": "0"}

def interface():
    print("Welcome to the WIRED scraping program!\nHere you may set up and initiate ")
    print("a scrape of the WIRED sitemap. In order\nto begin, please select one of the ")
    print("options below:")
    a = True
    while a:
        print("[1] Select a year (default = 1992)\n[2] Blacklist (default=None)")
        print("[3] Set JSON file # (default=0)\n[4] Set keyword(s) (default=None)")
        print("[5] Set delay timer (default=0sec)\n[6] Go!")

        pick = check(1, 6, "option number")

        if pick == 1:
            options["year"] = check(1992, current, "year")
        elif pick == 2:
            options["blacklist"] = blacklist()
        elif pick == 3:
            options["num"] = check(0, 9999, "JSON file start number")
        elif pick == 4:
            options["keywords"] = keywords()
        elif pick == 5:
            options["timer"] = timer()
        else:
            break
    print(options)
    return options

def check(x, y, purpose):
    while True:
        try:
            pick = int(input("Enter a(n) " + purpose + ": "))
            if pick < x or pick > y:
                print("Out of range, try again.")
            else:
                break
        except ValueError:
            print("Invalid input, please enter an integer from " + str(x) + "-" + str(y))
    return pick

def blacklist():
    print("Here you may enter links for weeks to be blacklisted. Press enter")
    print("with a blank field in order to exit.")
    while True:
        weekURL = input("Paste a URL: ")
        if weekURL == "":
            break

    return weekURL

def keywords():
    print("Here you may enter keywords to be searched for in URL names throughout the")
    print("year. You may enter multiple words to be searched for individually, or specific")
    print("phrases. In order to find phrases, seperate each word with a dash (\"-\"). In")
    print("order to find individual words, separate them with a space.\n")

    words = input("Enter your word(s): ")

    return words

def timer():
    print("Here you have the option of selecting a timer. You may have a randomly")
    print("selected number of seconds within a range, or a fixed number.\n[1] Fixed")
    print("[2] Random")

    pick = check(1, 2, "option number")
    if pick == 1:
        delay = check(0, 9999, "number of seconds")
        return delay
    elif pick == 2:
        start = check(0, 9999, "number of seconds")
        end = check(start, 9999, "number of seconds")
        return "rand " + str(start) + " " + str(end)

interface()

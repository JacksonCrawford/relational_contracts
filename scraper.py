import foundation
import interface
import requests
from bs4 import BeautifulSoup
import json
import time
import random

options = interface.interface()

# Uses requests to navigate to the Wired sitemap and grab all data under the specified class
page = requests.get("https://www.wired.com/sitemap/")
soupLinks = BeautifulSoup(page.text, "lxml")
links = soupLinks.find(class_="sitemap__section-archive")

# Finds all links with "1998" in them
def masterLinker():
    linkList = list()
    blacklist = options["blacklist"]
    keywords = options["keywords"]
    aTags = links.find_all("a")
    for link in aTags:
        url = link.contents[0]
        if str(options["year"]) in str(url) and str(url) not in blacklist:
            if len(keywords) > 0 and str(url) in keywords:
                linkList.append(url)
            else:
                linkList.append(url)
    return linkList

# Finds all links within the class of the site specified above
def linker(url):
    linkList = list()
    try:
        site = requests.get(url)
    except:
        t = time.localtime()
        currentTime = time.strftime("%H:%M:%S", t)
        print("Sleeping for 1 hour (3600 sec), beginning at:", currentTime)
        time.sleep(3600)
        site = requests.get(url)

    soupy = BeautifulSoup(site.text, "lxml")
    linkz = soupy.find(class_="sitemap__section-archive")

    aTags = linkz.find_all("a")
    for link in aTags:
        url = link.contents[0]
        linkList.append(url)
    return linkList

# Main function that is run, uses a loop to evaluate data with scraper()
# in all links returned by linker()
def main():
    bigLinks = masterLinker()
    linkNum = options["num"]
    for bigLink in bigLinks:
        print(str(bigLink) + "----------------")

        lilLinks = linker(bigLink)
        for link in lilLinks:
            data = foundation.scraper(link)

            timestamp = data["timestamp"]
            fileDate = timestamp[:timestamp.find(" "):]
            articleNum = f"{linkNum:04}"

            '''with open("wired_article_" + fileDate + "_" + articleNum + ".json", "w") as j:
                json.dump(data, j)
            print(str(link) + " -- #" + str(articleNum))'''
            linkNum += 1
            print(linkNum)

            if type(options["timer"]) == str and "rand" in options["timer"]:
                delay = options["timer"].split()
                time.sleep(random.randint(int(delay[1]), int(delay[2])))
                print("Sleep " + str(delay[1]) + str(delay[2]))
            else:
                time.sleep(options["timer"])
                print(options["timer"])

main()

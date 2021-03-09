import foundation
import requests
from bs4 import BeautifulSoup
import json
import time
import random

year = input("Enter a year: ")

startTime = time.time()

# Uses requests to navigate to the Wired sitemap and grab all data under the specified class
page = requests.get("https://www.wired.com/sitemap/")
soupLinks = BeautifulSoup(page.text, "lxml")
links = soupLinks.find(class_="sitemap__section-archive")

# Finds all links with specified "year" in them
def masterLinker():
    resume = True
    linkList = list()
    aTags = links.find_all("a")
    for link in aTags:
        url = link.contents[0]
        '''if str(url) == "https://www.wired.com/sitemap?year=0000&month=0&week=0":
             resume = True'''
        if year in str(url) and resume:
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
    linkNum = 0
    for bigLink in bigLinks:
        print(str(bigLink) + "----------------")

        lilLinks = linker(bigLink)
        for link in lilLinks:
            data = foundation.scraper(link)

            timestamp = data["timestamp"]
            fileDate = timestamp[:timestamp.find(" "):]
            articleNum = f"{linkNum:04}"

            with open("wired_article_" + fileDate + "_" + articleNum + ".json", "w") as j:
                json.dump(data, j)
            print(str(link) + " -- #" + str(articleNum))
            linkNum += 1

            time.sleep(random.randint(20, 180))

    with open("stats.txt", "w") as file:
        file.write("Year: " + str(year) + "\nTime to complete: " + str(time.time() - startTime))
        file.write("\n# of files: " + str(linkNum) + "\n\nJackson's Notes: ")
main()

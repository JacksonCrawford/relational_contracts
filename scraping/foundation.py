import requests
from bs4 import BeautifulSoup
import json
import time

import newFoundation


# The function that actually accesses each link and finds the data.
# All attributes that are searched for have exception handlers for the event that the data
# is not present on the site, and returns "not found" under the value in the JSON file.
def scraper(link):
    # Declares dictionary for JSON export
    jsonDict = {"URL": str(), "heading": str(), "subheading": str(), "author": str(), "category": str(), "type": str(), "timestamp": str(), "text": str()}
    x = 0

    #print(link)
    # Looks for article main content
    try:
        site = requests.get(link)
    except:
        print("Failure in Name Resolution: " + str(link))
        time.sleep(120)
        site = requests.get(link)

    soup = BeautifulSoup(site.text, "lxml")
    try:
        soupyLinks = soup.find(class_="article main-content")
        chunkySoup = soupyLinks.find(class_="article__chunks article__chunks--without-top-spacing-content-well")
    except AttributeError:
        return newFoundation.scraper(link)

    jsonDict["URL"] = str(link)

    # Finds article heading
    try:
        header = (soupyLinks.find("h1")).contents[0]
#        print(header)
        jsonDict["heading"] = str(header).lower()
    except AttributeError:
        jsonDict["heading"] = "not found"

    # Finds article subheading
    try:
        subhead = soupyLinks.find(class_="content-header__row content-header__dek")
        subheading = multipleContents(subhead)
        jsonDict["subheading"] = str(subheading).lower()
    except AttributeError:
        jsonDict["subheading"] = "not found"

    # Finds article's author
    try:
        author = soupyLinks.find(class_="content-header__rubric-block")
        aTag = author.find("a")
        finalName = str(aTag.contents[0])
#        span = aTag.find_all("span")
#        print(aTag.contents)
#        exit()
#        finalName = str(aTag.contents[0]) + str(span[0].contents[0])
        jsonDict["author"] = str(finalName).lower()
    except AttributeError:
        jsonDict["author"] = "not found"
        print(str(link) + " Had no author")

    # Finds whether or not the article is a magazine or not
    try:
        form = soupyLinks.find(class_="sc-fubCfw sc-pFZIQ sc-bZSQDF jetItr fUXXxb eUgDnc").contents[0]
        jsonDict["type"] = str(form).lower()
    except AttributeError:
        jsonDict["type"] = "article"

    # Finds the timestamp of the article's publishing (stored as a string)
    try:
        timestamp = soupyLinks.find("time").contents[0]
        jsonDict["timestamp"] = str(timestamp)
    except AttributeError:
        jsonDict["timestamp"] = "not found"
        fileDate = "NoDateFound"
        print(str(link) + " Had no timestamp")

    # Finds the article's category
    try:
        catSoup = soupyLinks.find(class_="content-header__rubric-date-block")
        category = catSoup.find_all("span")
        finalCategory = category[0].contents[0]
        jsonDict["category"] = str(finalCategory).lower()
    except AttributeError:
        jsonDict["category"] = "not found"
        print(str(link) + " Had no category")
    except IndexError:
        jsonDict["category"] = "not found"
        print(str(link) + " Had no category")

    # Finds the text of the article (placed within <p></p> (paragraph) tags
    while x != 3:
        try:
            jsonDict["text"] += paragraph(chunkySoup)
            break
        except AttributeError:
            print("Text not found -> #" + str(x))
            x += 1
            time.sleep(100)

    return jsonDict

def multipleContents(soup):
    text = str()
    if len(soup.contents) == 1:
        return soup.contents[0]
    elif len(soup.contents) > 1:
        for content in soup.contents:
            text += str(content)
    aTags = soup.find_all("a")
    aContents = dict()
    for aTag in aTags:
            aContents[str(aTag)] = str(aTag.contents[0])
            if len(aTag.contents) > 0:
                for content in aTag.contents[1::]:
                    aContents[str(aTag)] += str(content)

    for key in aContents.keys():
            text = text.replace(key, aContents[key])

    return tagRm(text)


# Removes tags from text while ensuring no data is lost due to multiple contents within p tags
def paragraph(soup):
    try:
        text = str()
        aTags = soup.find_all("a")
        aContents = dict()
        spanTags = soup.find_all("span")
        spanContents = dict()
        strongTags = soup.find_all("strong")
        strongContents = dict()
        emTags = soup.find_all("em")
        emContents = dict()
        imgTags = soup.find_all("img")

        for aTag in aTags:
            if len(aTag.contents) == 0:
                aContents[str(aTag)] = str()
            else:
                aContents[str(aTag)] = str(aTag.contents[0])

        for emTag in emTags:
            if len(emTag.contents) == 0:
                emContents[str(aTag)] = str()
            else:
                emContents[str(emTag)] = str(emTag.contents[0])

        for strongTag in strongTags:
            if len(strongTag.contents) == 0:
                strongContents[str(aTag)] = str()
            else:
                strongContents[str(strongTag)] = str(strongTag.contents[0])

        for spanTag in spanTags:
            if len(spanTag.contents) == 0:
                spanContents[str(aTag)] = str()
            else:
                spanContents[str(spanTag)] = str(spanTag.contents[0])

        pTags = soup.find_all("p")
        for pTag in pTags:
            for ele in pTag.contents:
                text += str(ele)

        for key in spanContents.keys():
            text = text.replace(key, spanContents[key])

        for key in emContents.keys():
            text = text.replace(key, emContents[key])

        for key in strongContents.keys():
            text = text.replace(key, strongContents[key])
        for key in aContents.keys():
            text = text.replace(key, aContents[key])

        for tag in imgTags:
            text = text.replace(str(tag), str())

        text = text.replace("\\", "")
    except AttributeError:
        return "not found"

    return tagRm(text).lower()

def tagRm(text):
    text = text.replace("<em>", "")
    text = text.replace("</em>", "")
    text = text.replace("<strong>", "")
    text = text.replace("</strong>", "")
    text = text.replace("<br/>", "")

    return text

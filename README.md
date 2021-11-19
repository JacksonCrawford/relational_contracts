# Relational Contracts Research Project

Code Overview:

- Scrape article data from the WIRED Sitemap (https://www.wired.com/sitemap/)
- Analyze data with Natural Language Processing algorithms and pull out important topics
- Visualize results (jointly with CS360 final project)

## Program Overview:

### Scraping

##### foundation.py

Performs the actual scraping of an article

##### newFoundation.py

Same functionality as foundation.py, but adapted for alternate wired article layout.

##### scraper.py

Finds the links from the sitemap and passes them to the article scraping foundation programs to be scraped and stored

### NLP

##### analyzer.py

Reads every article and performs the actual analysis of them before storing the top twenty-five hyposets (defined below) and unique words in json format

##### hyposet.py

Object to store a word tree with the hypernym at the root. The next level down is the closest associated subcategory, and then the words themselves below. All have their count listed alongside.

##### new_word.py

Object to store a word that is not defined in WordNet. This object also store the preceding word of an unkown word for more ML analysis later on.

##### stopwords.py

Class that stores nltk's default stopwords and some of my own.

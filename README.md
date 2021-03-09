# Scrape of the WIRED Sitemap

Project Overview:

Scrape article data from the WIRED Sitemap (https://www.wired.com/sitemap/)

## Program Overview:

#### foundation.py

Performs the actual scraping of the article sites.

#### newFoundation.py

Same functionality as foundation.py, but adapted for alternate wired article layout.

#### scraper.py

Finds the links from the sitemap and passes them to foundation.py to be scraped.

# page-price-scraper

## Introduction

**This project is a webscraper for thespruce.com**.  It uses Selenium, BeautifulSoup4, and Regex to extract product and price information from given URLs of "X Best *Products* in *Category*" pages from The Spruce.

The Spruce uses JavaScript to fetch current prices from their retail partners, so Selenium was necessary rather than simple Requests.

Rather than building out the crawler functions to collect URLs and decide whether or not to scrape them, I used a list of all URLs from The Spruce that contain the word "Best", which was collected using Screaming Frog by someone on Fiverr.  Not all pages that contain "best" in their URL are list-type articles, so the bot needed to be able to handle missing information.

## Motivation

An old friend has a list-type blog with affiliate links.  If he could know what products sell for high prices and make good list-type content, then he could cross-check that high-ticket, easy-to-write-about products to easy-to-rank SEO terms and rank higher for better products on search engines. The Spruce is a popular list-type blog with many customers, so if a specific type of product works for The Spruce, it's likely to work for his blog as well.

## How it works

At a super high level, the web scraping process is as followed:

1. Define a target domain
2. Get a list of URLs on the site (either from a list or crawler)
3. Load the webpage and wait for all HTML and JavaScript objects to load
4. Scrape the page for targeted information
5. Store data in a spreadsheet and repeat for all URLs 
6. Clean, summarize, and present data

`scraper.py` reads a static list of URLs and launches a Selenium instance of the page.  The bot waits 5 seconds for the content to load and then uses BeautifulSoup4 and Regex to extract the page Title, Product Name, Product Reviews by Retailer, Product Prices by Retailer.  This information, along with the date the data was scraped, is saved as a CSV to the `output/` directory.  The logic behind creating one CSV per URL is so it would be easier to use multiprocessing in the future (launching multiple bots at once from the same list of URLs).  The bot waits a standard 5 seconds because it is usually enough time to load the webpage and waiting on specific objects is dangerous as the list of URLs contain pages that are not in the product-list-type desired format.  Examples of the resulting CSVs can be found in the `output/` directory.

`postprocessing.py` takes all CSVs from the `output/` directory and concatenates them into a single dataframe.  The rows are sorted alphabetically by the page title and exported as a CSV indexed by (Page Title, Product Title) with the current prices of the product by retailer and average price of the product across all retailers.  This large dataframe is then grouped by Page Title, so users can quickly see the average price of all products by page.  Note: this method of creating many small CSVs and concatenating them later was surprisingly fast, taking less than a second to execute the entire postprocessing script.  Examples of the product-indexed CSV can be found in `procuts.csv` and the page-indexed summary information can be found in `summary.csv`.

## Next Steps

Possible next steps include:

- Building out web crawler functionality and logic, so it may periodically search the home page for new list type pages.
- Adding multiprocessing to speed up the scraping process by allowing multilpe windows bots to run at the same time.
- Add logic to filter out pages that aren't list-type and not save their missing information.

## Keywords

- Web scraping
- Selenium
- Regular Expressions / Regex
- BeautifulSoup4 / bs4
- Pandas
- Data collection
- Data engineering
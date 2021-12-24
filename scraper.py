
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import os
import time
import pandas as pd
import numpy as np
import re
from statistics import mean

CHROME_DRIVER_LOC = '/home/jordan/Documents/page-price-scraper/chromedriver'

def load_page(url, static_mode=False):
    '''Read webpage.  Need to use selenium to wait on JavaScript objects'''
    html_file = 'selenium_page.html'

    if static_mode:
        # -- Stale version
        with open(html_file, 'r') as f:
            s_page = f.read()
    else:
        # -- Live version
        driver = webdriver.Chrome(CHROME_DRIVER_LOC)
        driver.get(url)
        time.sleep(5)
        s_page = driver.page_source
        with open(html_file, 'w') as f:
            print(s_page, file=f)
    
    return BeautifulSoup(s_page, 'html.parser')


def main():
    # sample_page = 'https://www.thespruce.com/best-canister-vacuums-4171592'
    sample_page = 'https://www.thespruce.com/best-headboards-4165760'
    # sample_page = 'https://www.thespruce.com/best-garage-heaters-4176054'

    soup = load_page(sample_page, static_mode=True)

    product_data = []

    # Get page title: class="heading__title"
    page_titles = soup.find("h1", class_="heading__title")
    try:
        page_titles = re.findall('>(.*)<\/', str(page_titles))[0]
    except IndexError:
        page_titles = page_titles

    # Get product retailer: data-retailer-type
    product_sections = soup.find_all("div", class_="comp sc-list-item list-sc-item__content mntl-block")
    print("-- product sections --")
    print(f"Product sections type: {type(product_sections)}")
    for section in product_sections:
        print(f"Section type: {type(section)}")
        with open('section.txt', 'w') as f:
            print(section, file=f)
        print('-----')

        # Get product title: class="product-record__heading--text"
        product_titles = section.find("span", class_="product-record__heading--text")
        print(f"product_titles = {product_titles}")
        try:
            product_titles = re.findall('>([^<]*)<\/', str(product_titles))[0].replace('\n', ' ').strip()
        except IndexError:
            product_titles = product_titles
        
        # Get product ratings
        product_ratings = section.find("span", class_="star-rating__label")
        try:
            product_ratings = re.findall('>(\d*[.,]?\d*)<\/', str(product_ratings))[0]
        except IndexError:
            product_ratings = product_ratings
        print(f"product_ratings = {product_ratings}")

        
        product_details = section.find_all("a", class_="button mntl-commerce-button mntl-text-link js-extended-commerce__button")
        
        price_details_list = []
        for details in product_details:
            with open('details.txt', 'w') as f:
                print(section, file=f)
            print(f"details_type = {type(details)}")

            # Price
            try:
                price = re.findall('price="*?(\$\d*,?\d*)', str(details))[0]
            except IndexError:
                price = np.nan
            
            print(f"price = {price}")

            # Retailer
            try:
                retailer = re.findall('View On (.*)<\/span>', str(details))[0]
            except IndexError:
                retailer = np.nan
            price_details_list.append({'retailer': retailer, 'price': price})

        print(f"product_prices = {price_details_list}")

        prices = [float(x['price'].strip('$').replace(',', '')) for x in price_details_list if isinstance(x['price'], str)]
        avg_product_price = mean(prices) if len(prices) > 0 else np.nan
        
        product_data.append([page_titles, product_titles, product_ratings, price_details_list, avg_product_price])
    

    header_row = ['page_titles', 'product_titles', 'product_ratings', 'product_prices', 'avg_product_price']
    df = pd.DataFrame(product_data, columns=header_row)
    # TODO: Add date

    print(df.groupby('page_titles').mean())

    df.to_csv('product_data.csv')

    # TODO: Crawler to read all the links in the bottom section

    return

if __name__=='__main__':
    main()
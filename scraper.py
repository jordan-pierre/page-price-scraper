
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import os
import time
import pandas as pd
import numpy as np
import re


def main():
    sample_page = 'https://www.thespruce.com/best-garage-heaters-4176054' # 'https://www.thespruce.com/best-canister-vacuums-4171592'

    html_file = 'selenium_page.html'
    # -- Live version
    driver = webdriver.Chrome('/home/jordan/Documents/page-price-scraper/chromedriver')
    driver.get(sample_page)

    time.sleep(5)
    s_page = driver.page_source
    with open(html_file, 'w') as f:
        print(s_page, file=f)

    # -- Stale version
    # with open(html_file, 'r') as f:
    #     s_page = f.read()

    soup = BeautifulSoup(s_page, 'html.parser')

    
    product_data = []

    # Get page title: class="heading__title"
    page_titles = soup.find("h1", class_="heading__title")
    print(page_titles)

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

        product_ratings = section.find("span", class_="star-rating__label")
        print(f"product_ratings = {product_ratings}")

        
        product_details = section.find_all("a", class_="button mntl-commerce-button mntl-text-link js-extended-commerce__button")
        
        details_list = []
        for details in product_details:
            with open('details.txt', 'w') as f:
                print(section, file=f)
            print(f"details_type = {type(details)}")

            # Price
            try:
                price = re.findall('data-commerce-price="*?(\$\d*,?\d*)', str(details))[0]
            except IndexError:
                price = np.nan
            
            print(f"price = {price}")

            # Retailer
            try:
                retailer = re.findall('View On ([a-zA-Z0-9\'_.-]*)<', str(details))[0]
            except IndexError:
                retailer = np.nan
            details_list.append({'price': price, 'retailer': retailer})


        # TODO: Extract price, link, and site
        print(f"product_prices = {details_list}")
        
        product_data.append([page_titles, product_titles, product_ratings, details_list])
    

    header_row = ['page_titles', 'product_titles', 'product_ratings', 'product_prices']
    df = pd.DataFrame(product_data, columns=header_row)
    df.to_csv('product_data.csv')

    return

if __name__=='__main__':
    main()
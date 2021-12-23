
from bs4 import BeautifulSoup
import requests


def main():
    sample_page = 'https://www.thespruce.com/best-canister-vacuums-4171592'
    page = requests.get(sample_page)
    with open('page.html', 'w') as f:
            print(page.content, file=f)

    soup = BeautifulSoup(page.content, 'html.parser')

    # Get page title: class="heading__title"
    page_titles = soup.find_all("h1", class_="heading__title")
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
        product_titles = section.find_all("span", class_="product-record__heading--text")
        print(f"product_titles = {product_titles}")

        product_ratings = section.find_all("span", class_="star-rating__label")
        print(f"product_ratings = {product_ratings}")

        
        product_prices = section.find_all("a", class_="data-commerce-price")
        print(f"product_prices = {product_prices}")
        
        break


    return

if __name__=='__main__':
    main()
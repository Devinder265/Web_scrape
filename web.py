# Importing Required Libraries
import requests
from bs4 import BeautifulSoup
import csv

# Creating CSV File
csv_file = open('amazon_products.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Product Name', 'Product URL', 'Product Price', 'Rating', 'Number of Reviews', 'Description', 'ASIN', 'Product Description', 'Manufacturer'])

# Scraping Products from Amazon
for i in range(1, 21):
    url = f'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{i}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    products = soup.find_all('div', {'data-component-type': 's-search-result'})

    for product in products:
        try:
            product_url = 'https://www.amazon.in' + product.find('a', {'class': 'a-link-normal s-no-outline'})['href']
        except:
            product_url = None

        try:
            product_name = product.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}).text.strip()
        except:
            product_name = None

        try:
            product_price = product.find('span', {'class': 'a-price-whole'}).text.strip()
        except:
            product_price = None

        try:
            rating = product.find('span', {'class': 'a-icon-alt'}).text.strip()
        except:
            rating = None

        try:
            num_reviews = product.find('span', {'class': 'a-size-base'}).text.strip()
        except:
            num_reviews = None

        # Scraping Additional Product Information
        if product_url:
            response = requests.get(product_url)
            soup = BeautifulSoup(response.content, 'html.parser')

            try:
                description = soup.find('div', {'id': 'productDescription'}).text.strip()
            except:
                description = None

            try:
                asin = soup.find('th', {'class': 'a-color-secondary a-size-base prodDetSectionEntry'}).text.strip()
            except:
                asin = None

            try:
                product_description = soup.find('div', {'id': 'feature-bullets'}).text.strip()
            except:
                product_description = None

            try:
                manufacturer = soup.find('a', {'id': 'bylineInfo'}).text.strip()
            except:
                manufacturer = None

        # Writing Data to CSV File
        csv_writer.writerow([product_name, product_url, product_price, rating, num_reviews, description, asin, product_description, manufacturer])

# Closing CSV File
csv_file.close()
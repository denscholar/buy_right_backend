import selenium.webdriver as webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from bs4 import BeautifulSoup
import time

from products.models import Category, Product


# from products.models import Product


# def close_popup(driver):
#     try:
#         # Wait for the popup and close button to appear and then click it
#         close_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".popup-close-button"))
#         )
#         close_button.click()
#         print("Popup closed successfully.")
#     except (TimeoutException, NoSuchElementException):
#         print("No popup detected, continuing with scraping.")


# def scrape_website(website):
#     print("launchin chrome browser...")

#     options = webdriver.ChromeOptions()
#     driver = webdriver.Chrome(
#         service=Service(ChromeDriverManager().install()), options=options
#     )

#     try:
#         driver.get(website)
#         driver.implicitly_wait(5.0)

#         input_element = driver.find_element(By.ID, value="fi-q")
#         input_element.clear()
#         search_items = [
#             # "Computing",
#             "Electronics",
#             # "Sporting Goods",
#             # "Phones & Tablets",
#             # "Toys & Games",
#             # "Automobile",
#             # "Health & Beauty",
#             # "Industrial & Scientific",
#             # "Fashion",
#         ]

#         for search_item in search_items:
#             try:
#                 input_element.clear()
#                 input_element.send_keys(search_item)

#                 submit_button = WebDriverWait(driver, 10).until(
#                     EC.element_to_be_clickable((By.CLASS_NAME, "_prim"))
#                 )

#                 submit_button.click()

#                 time.sleep(3)
#                 current_page = 1

#                 while True:

#                     soup = BeautifulSoup(driver.page_source, "html.parser")

#                     products_container = soup.find(id="jm")

#                     if products_container:
#                         products = products_container.find_all(
#                             "article", class_="prd _fb col c-prd"
#                         )

#                         for product in products:
#                             title = (
#                                 product.find("h3", class_="name").get_text(strip=True)
#                                 if product.find("h3", class_="name")
#                                 else None
#                             )
#                             image_url = (
#                                 product.find("img")["data-src"]
#                                 if product.find("img")
#                                 else None
#                             )
#                             product_url = (
#                                 "https://www.jumia.com.ng"
#                                 + product.find("a", class_="core")["href"]
#                                 if product.find("a", class_="core")
#                                 else None
#                             )
#                             product_price = (
#                                 product.find("div", class_="prc").get_text(strip=True)
#                                 if product.find("div", class_="prc")
#                                 else None
#                             )

#                             obj, created = Product.objects.get_or_create(
#                                 product_url=product_url,
#                                 defaults={
#                                     "product_name": title,
#                                     "image_url": image_url,
#                                     "product_price": product_price,
#                                 },
#                             )

#                         try:
#                             max_retries = 3
#                             retries = 0

#                             while retries < max_retries:
#                                 try:
#                                     next_button = WebDriverWait(driver, 10).until(
#                                         EC.element_to_be_clickable(
#                                             (
#                                                 By.CSS_SELECTOR,
#                                                 'a[aria-label="Next Page"]',
#                                             )
#                                         )
#                                     )
#                                     driver.execute_script(
#                                         "arguments[0].scrollIntoView();", next_button
#                                     )
#                                     time.sleep(1)

#                                     # Capture current page URL to compare after clicking
#                                     previous_url = driver.current_url

#                                     driver.execute_script(
#                                         "arguments[0].click();", next_button
#                                     )
#                                     time.sleep(5)  # Wait for the page to load

#                                     # Check if the URL has changed to ensure pagination has moved forward
#                                     if driver.current_url == previous_url:
#                                         print(
#                                             "Pagination failed; ending pagination loop."
#                                         )
#                                         break
#                                     else:
#                                         current_page += 1
#                                         print(f"Moving to page {current_page}")
#                                         break

#                                 except ElementClickInterceptedException:
#                                     print("Click intercepted, retrying...")
#                                     retries += 1
#                                     time.sleep(1)

#                         except TimeoutException:
#                             print("No more pages to navigate.")
#                             break
#             except StaleElementReferenceException:
#                 print(
#                     f"Element reference was stale. Retrying for search item: {search_item}"
#                 )
#                 continue

#     except Exception as e:
#         raise e

#     finally:
#         driver.quit()


# scrape_website("https://www.jumia.com.ng/")


# initialize the chrome driver
def start_driver():
    options = webdriver.ChromeOptions()
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )


# Scraper function for
def scrape_jumia(driver, search_terms):
    driver.get("https://www.jumia.com.ng/")
    input_element = driver.find_element(By.ID, "fi-q")

    for search_item in search_terms:
        input_element.clear()
        input_element.send_keys(search_item)

        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "_prim"))
        )
        submit_button.click()
        time.sleep(3)

        scrape_jumia_pages(driver, search_terms)


# Helper function to scrape pages on Jumia
def scrape_jumia_pages(driver, search_terms):
    current_page = 1

    for search in search_terms:
        while True:
            soup = BeautifulSoup(driver.page_source, "html.parser")
            products_container = soup.find(id="jm")

            if products_container:
                products = products_container.find_all(
                    "article", class_="prd _fb col c-prd"
                )

                for product in products:
                    title = (
                        product.find("h3", class_="name").get_text(strip=True)
                        if product.find("h3", class_="name")
                        else None
                    )
                    image_url = (
                        product.find("img")["data-src"] if product.find("img") else None
                    )
                    product_url = (
                        "https://www.jumia.com.ng"
                        + product.find("a", class_="core")["href"]
                        if product.find("a", class_="core")
                        else None
                    )
                    product_price = (
                        product.find("div", class_="prc").get_text(strip=True)
                        if product.find("div", class_="prc")
                        else None
                    )

                    # create the category

                    categoryObj, created = Category.objects.get_or_create(
                        name=search,
                        defaults={
                            "name": search,
                        },
                    )

                    obj, created = Product.objects.get_or_create(
                        product_url=product_url,
                        defaults={
                            "categoty": categoryObj,
                            "product_name": title,
                            "image_url": image_url,
                            "product_price": product_price,
                            "source": "Jumia",
                        },
                    )

                    print("source:", "Jumia")
                    print("product_name:", title)
                    print("image_url:", image_url)
                    print("product_url:", product_url)
                    print("product_price:", product_price)

            if not go_to_next_page(driver):
                break


# Function to handle pagination on Jumia
def go_to_next_page(driver):
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[aria-label="Next Page"]'))
        )
        driver.execute_script("arguments[0].scrollIntoView();", next_button)
        driver.execute_script("arguments[0].click();", next_button)
        time.sleep(5)  # Wait for the page to load

        return True
    except TimeoutException:
        print("No more pages.")
        return False


# Main function to scrape multiple websites
def scrape_websites(websites_to_scrape):
    driver = start_driver()
    try:
        for website in websites_to_scrape:
            if website["name"] == "jumia":
                print("Scraping Jumia...")
                scrape_jumia(driver, website["search_terms"])
            # Add more conditions here for other websites like 'konga', etc.

    finally:
        driver.quit()


# Configuration for websites to scrape

# websites = [
#     {
#         "name": "jumia",
#         "search_terms": ["Electronics"],
#     },
#     # Add more website dictionaries here as needed
# ]


# scrape_websites(websites)

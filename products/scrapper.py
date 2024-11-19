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

from .utils import scrape_Oyato_pages, scrape_jumia_pages, start_driver


# from products.models import Category, Product


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


def dismiss_blocking_elements(driver):
    try:
        # Handle the cookies banner
        cookies_accept_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Accept cookies']"))
        )
        cookies_accept_button.click()
        print("Cookies banner dismissed.")

        # Handle the close banner button
        close_banner_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='cls']"))
        )
        close_banner_button.click()
        print("Close banner dismissed.")
    except TimeoutException:
        print("Blocking elements not found or already dismissed.")
    except Exception as e:
        print(f"Error dismissing blocking elements: {e}")
    except Exception as e:
        print(f"Error dismissing blocking elements: {e}")


def locate_element_with_retry(driver, xpath, retries=3):
    for attempt in range(retries):
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            return element
        except StaleElementReferenceException:
            print(f"Stale element encountered. Retrying {attempt + 1}/{retries}...")
    raise Exception(f"Failed to locate the element after {retries} retries.")


# Scraper function for jumia
def scrape_jumia(driver, categories):
    driver.get("https://www.jumia.com.ng/")

    for category in categories:
        dismiss_blocking_elements(driver)
        target_xpath = f"//a[@class='itm']//span[text()='{category}']"
        try:
            link = locate_element_with_retry(driver, target_xpath)
            driver.execute_script(
                "arguments[0].click();", link
            )  # Use JS click for robustness
            scrape_jumia_pages(driver)
        except Exception as e:
            print(f"Error processing category '{category}': {e}")


# Scraper function for OYato
def scrape_oyato(driver, categories):
    driver.get("https://www.oyato.ng/")

    for category in categories:
        try:
            link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        f"//a[@class='dropdown-toggle']//span[contains(text(), '{category}')]",
                    )
                )
            )
            link.click()

            scrape_Oyato_pages(driver)
        except Exception as e:
            print(f"Error processing category '{category}': {e}")


# Main function to scrape multiple websites
def scrape_websites(websites_to_scrape):
    driver = start_driver()
    try:
        for website in websites_to_scrape:
            if website["name"] == "oyato":
                print("Scraping Oyato...")
                scrape_oyato(driver, website["categories"])
            if website["name"] == "jumia":
                print("Scraping Jumia...")
                scrape_jumia(driver, website["categories"])
            # Add more conditions here for other websites like 'konga', etc.

    finally:
        driver.quit()


# Configuration for websites to scrape
# websites = [
#     {
#         "name": "jumia",
#         "categories": ["Electronics"],
#     },
#     {
#         "name": "oyato",
#         "categories": ["Electronics"],
#     },
#     # Add more website dictionaries here as needed
# ]


# scrape_websites(websites)

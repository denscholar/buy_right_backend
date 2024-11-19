import selenium.webdriver as webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import re
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


# initialize the chrome driver
def start_driver():
    options = webdriver.ChromeOptions()
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )


# Helper function to scrape pages on Jumia
def scrape_jumia_pages(driver):
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

                # categoryObj, created = Category.objects.get_or_create(
                #     name=category,
                #     defaults={
                #         "name": category,
                #     },
                # )

                # obj, created = Product.objects.get_or_create(
                #     product_url=product_url,
                #     defaults={
                #         "categoty": categoryObj,
                #         "product_name": title,
                #         "image_url": image_url,
                #         "product_price": product_price,
                #         "source": "Jumia",
                #     },
                # )

                print("source:", "Jumia")
                print("product_name:", title)
                print("image_url:", image_url)
                print("product_url:", product_url)
                print("product_price:", product_price)

        if not go_to_next_page_jumia(driver):
            break


# Function to handle pagination on Jumia
def go_to_next_page_jumia(driver):
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


# Helper function to scrape pages on Oyato
def scrape_Oyato_pages(driver):
    while True:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "ajax-filter-container"))
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")
        products_container = soup.find("div", class_="site-wrapper")

        if products_container:
            products = products_container.find_all(
                "div", class_=re.compile(r"product-layout")
            )

            for product in products:
                # Extracting the product title
                title = (
                    product.find("div", class_="name").get_text(strip=True)
                    if product.find("div", class_="name")
                    else None
                )

                # Extracting the image URL
                image_url = product.find("img")["src"] if product.find("img") else None

                # Extracting the product URL
                product_url = (
                    product.find("a", class_="product-img")["href"]
                    if product.find("a", class_="product-img")
                    else None
                )

                # Extracting the product price
                product_price = (
                    product.find("span", class_="price-new").get_text(strip=True)
                    if product.find("span", class_="price-new")
                    else None
                )

                # create the category

                # categoryObj, created = Category.objects.get_or_create(
                #     name=category,
                #     defaults={
                #         "name": category,
                #     },
                # )

                # obj, created = Product.objects.get_or_create(
                #     product_url=product_url,
                #     defaults={
                #         "categoty": categoryObj,
                #         "product_name": title,
                #         "image_url": image_url,
                #         "product_price": product_price,
                #         "source": "Jumia",
                #     },
                # )

                print("source:", "Oyata")
                print("product_name:", title)
                print("image_url:", image_url)
                print("product_url:", product_url)
                print("product_price:", product_price)

        if not go_to_next_page_oyota(driver):
            break


# Function to handle pagination on Oyata
def go_to_next_page_oyota(driver):

    try:
        next_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[@class='next']"))
        )
        print("Next button found.")

        # Debug button properties
        # print(f"Is displayed: {next_button.is_displayed()}")
        # print(f"Href attribute: {next_button.get_attribute('href')}")
        # print(f"Outer HTML: {next_button.get_attribute('outerHTML')}")

        # Attempt to fix visibility issues
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
        time.sleep(1)  # Smooth scroll

        if not next_button.is_displayed():
            print("Forcing visibility of the 'Next' button.")
            driver.execute_script(
                "arguments[0].style.visibility = 'visible'; "
                "arguments[0].style.display = 'block'; "
                "arguments[0].style.opacity = '1';",
                next_button
            )
            time.sleep(1)

        # Click or navigate
        if next_button.is_displayed():
            try:
                next_button.click()
                print("Clicked 'Next' button.")
            except Exception as e:
                print(f"Normal click failed: {e}. Trying JS click.")
                driver.execute_script("arguments[0].click();", next_button)

            time.sleep(5)  # Wait for the next page to load
            return True
        else:
            # Navigate using href if button cannot be clicked
            print("Next button is not clickable. Attempting navigation via href.")
            next_url = next_button.get_attribute("href")
            if next_url:
                driver.get(next_url)
                print(f"Navigated to: {next_url}")
                time.sleep(5)  # Wait for the next page to load
                return True
            else:
                print("Next button does not have a valid href.")
                return False

    except TimeoutException:
        print("TimeoutException: 'Next' button not found within 20 seconds.")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

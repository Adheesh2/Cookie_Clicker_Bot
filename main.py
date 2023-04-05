import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'

chrome_driver_path = r"E:\Code\Chrome Driver\geckodriver-v0.33.0-win32\geckodriver.exe"
service = Service(chrome_driver_path)
driver = webdriver.Firefox(service=service, options=options)
driver.get("http://orteil.dashnet.org/experiments/cookie/")

cookie = driver.find_element(By.XPATH, '//*[@id="cookie"]')
item_div = driver.find_elements(By.CSS_SELECTOR, "#store div")
item_id = [item.get_attribute("id") for item in item_div]

timeout = time.time() + 5
five_min = time.time() + 60 * 5  # 5minutes

while True:
    cookie.click()

    # Every 5 seconds:
    if time.time() > timeout:

        # Get current cookie count
        money_element = driver.find_element(By.ID, "money").text
        if "," in money_element:
            money_element = money_element.replace(",", "")
        cookie_count = int(money_element)

        # Get all upgrade <b> tags
        all_prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
        item_prices = []

        # Convert <b> text into an integer price.
        for price in all_prices:
            element_text = price.text
            if element_text != "":
                cost = int(element_text.split("-")[1].strip().replace(",", ""))
                item_prices.append(cost)

        # Create dictionary of store items and prices
        cookie_upgrades = {}
        for n in range(len(item_prices)):
            cookie_upgrades[item_prices[n]] = item_id[n]

        # Find upgrades that we can currently afford
        affordable_upgrades = {}
        for cost, id in cookie_upgrades.items():
            if cookie_count > cost:
                affordable_upgrades[cost] = id

        if len(affordable_upgrades)>0:
            # Purchase the most expensive affordable upgrade
            highest_price_affordable_upgrade = max(affordable_upgrades)
            print(highest_price_affordable_upgrade)
            to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]
            driver.find_element(By.ID, to_purchase_id).click()

        timeout = time.time() + 5
        if time.time() > five_min:
            cookie_per_s = driver.find_element(By.ID, "cps").text
            print(cookie_per_s)
            break

driver.close()

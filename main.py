import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

OBERLO_URL = 'https://app.oberlo.com/my-products'

shopify_url = ""
email = ""
password = ""
all_products = []

with open('settings.json', 'r') as f:
    settings = json.loads(f.read())
    shopify_url = settings['shopify_url']
    email = settings['username']
    password = settings['password']

if not shopify_url or not email or not password:
    print("settings file is not filled out!")
    exit(1)

def main():
    options = Options()
    options.add_argument("start-maximized")
    driver = webdriver.Chrome()

    # Go to Shopify
    driver.get('https://accounts.shopify.com/store-login')

    # Click Login, Fill out shopify URL, click login, fill out password, click login
    login = driver.find_element_by_name('shop[domain]')
    login.send_keys(shopify_url)
    driver.find_element_by_name('commit').click()

    email_driver = driver.find_element_by_name('account[email]')
    email_driver.send_keys(email)
    driver.find_element_by_tag_name('form').submit()

    password_driver = driver.find_element_by_name('account[password]')
    password_driver.send_keys(password)
    driver.find_element_by_tag_name('form').submit()

    # Click Apps
    driver.get(f"https://{shopify_url}/admin/apps")
    driver.implicitly_wait(3) # seconds

    # Click Oberlo
    oberlo_url = driver.find_elements_by_css_selector("[aria-label='Oberlo']")[0].get_attribute("href")
    driver.get(oberlo_url)

    ## Now we are signed in to Oberlo via SSO

    # Click My Products
    driver.get(OBERLO_URL)

    can_paginate = True
    curr_page = 1
    base_url = ""
    while can_paginate:
        page_products = get_all_products_on_page(driver)
        if not(page_products):
            break
        all_products.append(page_products)
        if curr_page == 1:
            base_url = driver.current_url
        curr_page += 1
        driver.get(f"{base_url}?page={curr_page}")
        # Wait for content to show up
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'page-content')))

    flattened_products = [item for sublist in all_products for item in sublist]
    write_products_to_csv(flattened_products)

def get_all_products_on_page(driver):
    # Clicking one product lets us see all 20 products.
    # How? The page has some JavaScript that contains all the data we need.
    all_listings = driver.find_element_by_class_name('resource-list')
    all_products = all_listings.find_elements_by_tag_name('a')
    if len(all_products) == 0:
        return None
    product = all_products[0]
    product_page_url = product.get_attribute('href')

    # Open tab
    driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
    # Load the side page, which has the JavaScript we fetch below
    driver.get(product_page_url)
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'page-content')))
    # Close the tab
    driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')

    # Find the json on the page that starts with myProducts
    all_page_text = driver.page_source
    json_object_start = all_page_text[all_page_text.find("myProducts: [{")+len("myProducts: "):]
    json_object = json_object_start[:json_object_start.find("filters")].strip()
    json_object_no_comma = json_object[:len(json_object)-1]
    one_page_products = json.loads(json_object_no_comma)
    return one_page_products

def write_products_to_csv(products):
    file_name=f'{shopify_url.split('.myshopify.com')[0]}_product_list_master.csv'
    pass

if __name__ == "__main__":
    main()

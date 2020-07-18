import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

shopify_url = ""
email = ""
password = ""

with open('settings.json', 'r') as f:
    settings = json.loads(f.read())
    shopify_url = settings['shopify_url']
    email = settings['username']
    password = settings['password']

if not shopify_url or not email or not password:
    print("settings file is not filled out!")
    exit(1)

options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome()

# Go to Shopify
driver.get('https://accounts.shopify.com/store-login')

# Click Login, Fill out shopify URL, click login, fill out password, click login
login = driver.find_element_by_name('shop[domain]')
login.send_keys(shopify_url)
driver.find_element_by_name('commit').click()
driver.implicitly_wait(3) # seconds

email_driver = driver.find_element_by_name('account[email]')
email_driver.send_keys(email)
driver.find_element_by_tag_name('form').submit()
driver.implicitly_wait(3) # seconds

password_driver = driver.find_element_by_name('account[password]')
password_driver.send_keys(password)
driver.find_element_by_tag_name('form').submit()
driver.implicitly_wait(3) # seconds

# Click Apps

driver.get('https://curtaindepot.myshopify.com/admin/apps')
driver.implicitly_wait(3) # seconds

# Click Oberlo

oberlo_url = driver.find_elements_by_css_selector("[aria-label='Oberlo']")[0].get_attribute("href")
driver.get(oberlo_url)

## Now we are signed in to Oberlo via SSO

# Click My Products

driver.get('https://app.oberlo.com/my-products')

# Clicking one product lets us see all 20 products.
# How? The page has some JavaScript that contains all the data we need.
all_listings = driver.find_element_by_class_name('resource-list')
product = all_listings.find_elements_by_tag_name('a')[0]
product_page_url = product.get_attribute('href')

# Open tab
driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')

# Load a page
driver.get(product_page_url)

# Close the tab
driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')
all_page_text = driver.page_source
# Find the json on the page that starts with myProducts
json_object_start = all_page_text[all_page_text.find("myProducts: [{")+len("myProducts: "):]
json_object = json_object_start[:json_object_start.find("filters")].strip()
json_object_no_comma = json_object[:len(json_object)-1]
print(json.dumps(json.loads(json_object_no_comma)))

# Click navigate, go to next page, and repeat

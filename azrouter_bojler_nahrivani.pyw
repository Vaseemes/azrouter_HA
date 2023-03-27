import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service

# Constants
login_url = "http://azrouter.local/#/"
username = "YOUR-USERNAME"
password = "YOUR-PASSWORD"
refresh_interval = 5 # you can change this
watt_selector = "#app > div > main > div > main > div > div > div > div > div:nth-child(2) > div > div.v-card__text > div > div.d-flex.col.col-12 > div.pb-7.pr-5.display-3"
output_file_path = "//YOUR-HA-IP_ADDRESS/config/www/azrouter_bojler_nahrivani.txt"
ser = Service(r"C:\geckodriver.exe") # You can choose whatever path you want, it will just create .txt file there

# Set up Firefox driver
options = FirefoxOptions()
options.add_argument("--headless")
browser = webdriver.Firefox(service=ser, options=options)
browser.get(login_url)

# Login
searchElemUser = browser.find_element(By.CSS_SELECTOR, '#input-25')
searchElemUser.send_keys(username)

searchElemPW = browser.find_element(By.CSS_SELECTOR, '#input-28')
searchElemPW.send_keys(password)

browser.find_element(By.CSS_SELECTOR, '.v-btn').click()

browser.implicitly_wait(5)

# Monitor watt usage and write to file
prev_value = ""
while True:
    search_watt = browser.find_element(By.CSS_SELECTOR, watt_selector)
    watt_text = str(search_watt.text)
    watt_value = watt_text.split("(", 1)[0].strip()[:-2]
    print(watt_value)
    
    
    if prev_value != watt_value:
        print(f"\r{watt_value}", end="")
        prev_value = watt_value
        
        with open(output_file_path, "w") as f:
            f.write(watt_value)
    
    time.sleep(refresh_interval)

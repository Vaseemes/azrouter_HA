import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service


# Constants
login_url = "http://azrouter.local/#/devices"
username = "YOUR-USERNAME"
password = "YOUR-PASSWORD"
refresh_interval = 180 # you can change this
bojler_temp_selector = "#app > div > main > div > main > div > div > div > div > div > div > div.row.py-5.px-2.no-gutters > div:nth-child(2) > div:nth-child(1) > div > div.v-progress-linear__content > div > span"
output_file_path = "//YOUR-HA-IP_ADDRESS/config/www/azrouter_bojler.txt"
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
browser.find_element(By.CSS_SELECTOR, '#app > div > main > div > nav > header > div > button.v-app-bar__nav-icon.primary--text.v-btn.v-btn--icon.v-btn--round.theme--light.v-size--default > span > i').click()
browser.implicitly_wait(5)
browser.find_element(By.CSS_SELECTOR, '#app > div.v-application--wrap > main > div > nav > nav > div.v-navigation-drawer__content > div > a:nth-child(2) > div.v-list-item__content > div').click()

browser.implicitly_wait(5)

# Monitor watt usage and write to file
prev_value = ""
while True:
    search_bojler = browser.find_element(By.CSS_SELECTOR, bojler_temp_selector)
    bojler_teplota = str(search_bojler.text)
    bojler_teplota = bojler_teplota.split("/")[0]
    print(bojler_teplota)

    if prev_value != bojler_teplota:
        print(f"\r{bojler_teplota}", end="")
        prev_value = bojler_teplota
        
        with open(output_file_path, "w") as f:
            f.write(bojler_teplota)
    
    time.sleep(refresh_interval)

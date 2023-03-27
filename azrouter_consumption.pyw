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
watt_selector = "div.col-md-3:nth-child(2) > div:nth-child(1) > div:nth-child(2) > span:nth-child(2)"
output_file_path = "//YOUR-HA-IP_ADDRESS/config/www/azrouter.txt"
ser = Service(r"C:\geckodriver.exe") # You can choose whatever path you want, it will just create .txt file there

# Set up Firefox driver
options = FirefoxOptions()
options.add_argument("--headless")
browser = webdriver.Firefox(service=ser, options=options)
browser.get(login_url)

# Login
search_elem_user = browser.find_element(By.CSS_SELECTOR, "#input-25")
search_elem_user.send_keys(username)

search_elem_pw = browser.find_element(By.CSS_SELECTOR, "#input-28")
search_elem_pw.send_keys(password)

browser.find_element(By.CSS_SELECTOR, ".v-btn").click()

browser.implicitly_wait(5)

# Monitor watt usage and write to file
prev_value = ""
while True:
    search_watt = browser.find_element(By.CSS_SELECTOR, watt_selector)
    watt_text = str(search_watt.text)
    watt_value = watt_text.split("(", 1)[0].strip()[:-2]

    if prev_value != watt_value:
        print(f"\r{watt_value}", end="")
        prev_value = watt_value

        with open(output_file_path, "w") as file:
            file.write(watt_value)

    time.sleep(refresh_interval)

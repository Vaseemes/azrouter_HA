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
output_file_path = "//YOUR-HA-IP_ADDRESS/config/www/azrouter.txt" # Change IP
output_file_path2 = "//YOUR-HA-IP_ADDRESS/config/www/azrouter_bojler_nahrivani.txt" # Change IP
watt_selector1 = "div.col-md-3:nth-child(2) > div:nth-child(1) > div:nth-child(2) > span:nth-child(2)"
watt_selector2 = "#app > div > main > div > main > div > div > div > div > div:nth-child(2) > div > div.v-card__text > div > div.d-flex.col.col-12 > div.pb-7.pr-5.display-3"
ser = Service(r"C:\geckodriver.exe") # You can choose whatever path you want, it will just create .txt file there (geckodriver.exe doesn't have to be there)

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
prev_value1 = ""
prev_value2 = ""
while True:
    search_watt1 = browser.find_element(By.CSS_SELECTOR, watt_selector1)
    watt_text1 = str(search_watt1.text)
    watt_value1 = watt_text1.split("(", 1)[0].strip()[:-2]

    search_watt2 = browser.find_element(By.CSS_SELECTOR, watt_selector2)
    watt_text2 = str(search_watt2.text)
    watt_value2 = watt_text2.split("(", 1)[0].strip()[:-2]

    if prev_value1 != watt_value1:
        print(f"\r{watt_value1}", end="")
        prev_value1 = watt_value1

        with open(output_file_path, "w") as file:
            file.write(watt_value1)

    if prev_value2 != watt_value2:
        print(f"\r{watt_value2}", end="")
        prev_value2 = watt_value2

        with open(output_file_path2, "w") as f:
            f.write(watt_value2)

    time.sleep(refresh_interval)

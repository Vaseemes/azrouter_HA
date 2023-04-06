import time
from playwright.sync_api import Playwright, sync_playwright

# Constants
login_url = "http://azrouter.local/#/"
username = "YOUR-USERNAME"
password = "YOUR-PASSWORD"
refresh_interval = 5 # you can change this
output_file_path = "//YOUR-HA-IP_ADDRESS/config/www/azrouter.txt" # Change IP
output_file_path2 = "//YOUR-HA-IP_ADDRESS/config/www/azrouter_bojler_nahrivani.txt" # Change IP
watt_selector1 = "div.col-md-3:nth-child(2) > div:nth-child(1) > div:nth-child(2) > span:nth-child(2)"
watt_selector2 = "#app > div > main > div > main > div > div > div > div > div:nth-child(2) > div > div.v-card__text > div > div.d-flex.col.col-12 > div.pb-7.pr-5.display-3"

# Set up Playwright browser
with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(login_url)

    # Login
    page.fill("#input-25", username)
    page.fill("#input-28", password)
    page.click(".v-btn")

    # Monitor watt usage and write to file
    prev_value1 = ""
    prev_value2 = ""
    while True:
        try:
            search_watt1 = page.query_selector(watt_selector1)
            watt_text1 = str(search_watt1.inner_text())
            watt_value1 = watt_text1.split("(", 1)[0].strip()[:-2]

            search_watt2 = page.query_selector(watt_selector2)
            watt_text2 = str(search_watt2.inner_text())
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

        except Exception as e:
            print(f"\nError occurred: {e}")
            time.sleep(10)
            continue

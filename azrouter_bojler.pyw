from playwright.sync_api import Playwright, sync_playwright
import time


# Constants
login_url = "http://azrouter.local/#/devices"
username = "YOUR-USERNAME"
password = "YOUR-PASSWORD"
refresh_interval = 180 # you can change this
bojler_temp_selector = "#app > div > main > div > main > div > div > div > div > div > div > div.row.py-5.px-2.no-gutters > div:nth-child(2) > div:nth-child(1) > div > div.v-progress-linear__content > div > span"
output_file_path = "//YOUR-HA-IP_ADDRESS/config/www/azrouter_bojler.txt"

# Set up Playwright
with sync_playwright() as p:

    # Set up Chrome browser
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()

    # Navigate to login page
    page = context.new_page()
    page.goto(login_url)

    # Login
    page.fill("#input-25", username)
    page.fill("#input-28", password)
    page.click(".v-btn")

    # Wait for navigation button to be clickable
    page.wait_for_selector(".v-app-bar__nav-icon").click()

    # Wait for specific link to be clickable
    page.wait_for_selector("#app > div.v-application--wrap > main > div > nav > nav > div.v-navigation-drawer__content > div > a:nth-child(2) > div.v-list-item__content > div").click()

    # Monitor bojler temperature and write to file
    prev_value = ""
    while True:
        try:
            bojler_elem = page.wait_for_selector(bojler_temp_selector)
            bojler_teplota = str(bojler_elem.inner_text())
            bojler_teplota = bojler_teplota.split("/")[0]
            print(bojler_teplota)

            if prev_value != bojler_teplota:
                print(f"\r{bojler_teplota}", end="")
                prev_value = bojler_teplota

                with open(output_file_path, "w") as f:
                    f.write(bojler_teplota)

            time.sleep(refresh_interval)
            
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(10)
            continue

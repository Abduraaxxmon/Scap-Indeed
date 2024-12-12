from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
chrome_driver_path = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"

# driver = webdriver.Chrome()
# wait = WebDriverWait(driver, 10)
# ec = EC
# #

# options = Options()
# options.add_argument(r"--user-data-dir=C:\Users\abduk\AppData\Local\Google\Chrome\User Data\NewFolders1")  # Custom user data directory
# options.add_argument("--profile-directory=Default")  # Use the Default profile or specify another profile
#
# # Initialize the Chrome driver
# service = Service(chrome_driver_path)
# driver = webdriver.Chrome(options=options)
#
# ec = EC


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# Set the path to your Chrome profile directory
chrome_profile_path = r"C:\Users\abduk\AppData\Local\Google\Chrome\User Data\Default"  # Update this path

# Configure Chrome options
options = Options()
options.add_argument(f"user-data-dir={chrome_profile_path}")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

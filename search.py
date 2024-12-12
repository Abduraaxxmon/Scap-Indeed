import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from random import randint

def search( title, country,wait,ec,driver):

    time.sleep(randint(1,5))

    driver.get("https://www.indeed.com/")
    # time.sleep(60*30)
    time.sleep(randint(1,5))
    try:
        WebDriverWait(driver, 20).until(ec.url_contains("indeed"))
        jobs_entered_button = wait.until(ec.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div/span/div[4]/div[1]/div/div/div/div/form/div/div[1]/div[1]/div/div/span/input')))
        time.sleep(randint(1,5))
        job_location = wait.until(ec.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div/span/div[4]/div[1]/div/div/div/div/form/div/div[1]/div[3]/div/div/span/input')))

        time.sleep(randint(1,5))
        job_location.clear()
        time.sleep(randint(1, 3))
        jobs_entered_button.clear()
        time.sleep(randint(1, 3))

        # Enter data
        jobs_entered_button.send_keys(title.strip())
        time.sleep(randint(1, 3))
        job_location.clear()
        time.sleep(randint(1, 3))
        job_location.send_keys(country)
        time.sleep(randint(1, 3))

        jobs_entered_button.send_keys(Keys.ENTER)
        # time.sleep(60*60)
    except Exception as e:
        print(e)
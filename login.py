from selenium.webdriver.common.by import By

def perform_login(driver, email, password, wait, ec):
    jobs_button = wait.until(ec.element_to_be_clickable((By.XPATH, "//a[@href='https://www.linkedin.com/login']")))
    jobs_button.click()

    username_button = wait.until(ec.presence_of_element_located((By.XPATH, "//input[@name='session_key']")))
    password_button = driver.find_element(By.XPATH, "//input[@name='session_password']")

    username_button.send_keys(email)
    password_button.send_keys(password)

    sign_in_button = driver.find_element(By.XPATH, "//button[@aria-label='Sign in']")
    sign_in_button.click()
import time
import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException

service = Service(r"E:\Soft\chromedriver-win64\chromedriver.exe")

with open("config.yaml") as f:
    data = yaml.safe_load(f)

def test_contact_us_form():
    print("open link")
    driver = webdriver.Chrome(service=service)
    driver.get(data["address"])

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "mdc-text-field__input")))
    
    username_field = driver.find_element(By.CLASS_NAME, "mdc-text-field__input")
    username_field.send_keys(data["username"])

    password_fields = driver.find_elements(By.CLASS_NAME, "mdc-text-field__input")
    if len(password_fields) > 1:
        password_fields[1].send_keys(data["password"])

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.mdc-button"))).click()

    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.LINK_TEXT, "Contact"))).click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "mdc-text-field__input")))

    name_field = driver.find_element(By.XPATH, "//input[@type='text']")
    name_field.send_keys("Valera")

    email_field = driver.find_element(By.XPATH, "//input[@type='email']")
    email_field.send_keys("valera142@example.com")

    content_field = driver.find_element(By.XPATH, "//textarea")
    content_field.send_keys("test message.")

    driver.find_element(By.XPATH, "//span[contains(text(), 'Contact Us')]").click()

    try:
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        print("alert text:", alert.text)
        alert.accept()
    except TimeoutException:
        print("alert not shown")
    
    driver.quit()

test_contact_us_form()

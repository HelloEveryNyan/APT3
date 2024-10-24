import requests
import yaml
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException

service = Service(r"E:\Soft\chromedriver-win64\chromedriver.exe")

with open("config.yaml") as f:
    data = yaml.safe_load(f)

print("start ChromeDriver")
driver = webdriver.Chrome(service=service)

def test_step1(login, testtext1):
    header = {"X-Auth-Token": login}
    res = requests.get(data["address"] + "api/posts", params={"owner": "notMe"}, headers=header)
    listres = [i["title"] for i in res.json()["data"]]
    assert testtext1 in listres

def test_step2(login, post_data):
    header = {"X-Auth-Token": login}
    res = requests.post(data["address"] + "api/posts", headers=header, data=post_data)
    assert res.status_code == 200

def test_step3(login, created_post):
    header = {"X-Auth-Token": login}
    res = requests.get(data["address"] + "api/posts", params={"owner": "me"}, headers=header)
    descriptions = [i["description"] for i in res.json()["data"]]
    assert created_post["description"] in descriptions

def test_create_post_via_ui():
    post_data = {
        "title": "Заголовок поста",
        "description": "Описание поста",
        "content": "Содержимое поста"
    }

    print("open link")
    driver.get(data["address"])

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "mdc-text-field__input")))

    username_field = driver.find_element(By.CLASS_NAME, "mdc-text-field__input")
    username_field.send_keys(data["username"])

    password_fields = driver.find_elements(By.CLASS_NAME, "mdc-text-field__input")
    if len(password_fields) > 1:
        password_fields[1].send_keys(data["password"])

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.mdc-button"))).click()

    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "create-btn"))).click()

    time.sleep(2)

    try:
        title_field = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, '')]")))
        title_field.send_keys(post_data["title"])

        description_field = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea.mdc-text-field__input[aria-controls]")))
        description_field.send_keys(post_data["description"])

        content_field = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea.mdc-text-field__input[aria-describedby]")))
        content_field.send_keys(post_data["content"])

        save_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Save')]//ancestor::button")))
        save_button.click()

        time.sleep(3)

        created_title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Заголовок поста')]")))
        assert created_title.text == post_data["title"], f"Title '{post_data['title']}' not found on the page"
        
        print(f"post create with title: {created_title.text}")
    except TimeoutException:
        print("not found no one input fields.")
    except Exception as e:
        print(f"error: {e}")

    driver.quit()
    print("close browser.")

test_create_post_via_ui()
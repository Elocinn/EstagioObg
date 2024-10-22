import os
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("INSTAGRAM_USERNAME")
password = os.getenv("INSTAGRAM_PASSWORD")

def type_like_a_human(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.2, 2.0)) 
        
def click_not_now():
    try:
        not_now_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[text()='Agora não']"))
        )
        not_now_button.click()
    except Exception as e:
        print(f"'Agora não' não foi encontrado: {e}")
        
def scroll_down(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        
#LINUX 
service = Service("/usr/bin/chromedriver") 
driver = webdriver.Chrome(service=service)
#print(f"ChromeDriver Version: {driver.capabilities['chrome']['chromedriverVersion']}")
#print(f"Browser Version: {driver.capabilities['browserVersion']}") 

#WINDOWS
# Inicializando o driver do Chrome
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

try:
    driver.get("https://www.instagram.com/accounts/login/")
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")
    
    type_like_a_human(username_input, username)
    type_like_a_human(password_input, password)
    
    password_input.send_keys("\n")

    click_not_now()
    time.sleep(5)  
    click_not_now()
    
    scroll_down(driver)

    driver.find_element(By.XPATH, "//button[contains(@class, 'wpO6b')]").click()

finally:
    driver.quit()
import os
import random
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
#from bs4 import BeautifulSoup

load_dotenv()

username = os.getenv("INSTAGRAM_USERNAME")
password = os.getenv("INSTAGRAM_PASSWORD")

def type_like_a_human(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.2, 2.0)) 

def click_not_now(driver):
    try:
        not_now_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[text()='Agora não']"))
        )
        not_now_button.click()
        print("'Agora não' clicado com sucesso.")
        print("\n")
    except Exception as e:
        print(f"'Agora não' não foi encontrado: {e}")
        time.sleep(2)
        
def check_login_errors(driver):
    if is_element_present(driver, "//p[contains(text(), 'senha incorreta')]"):
        print("Erro de login: Senha incorreta.")
        return False
    elif is_element_present(driver, "//p[contains(text(), 'não corresponde a uma conta')]"):
        print("Erro de login: Nome de usuário inválido.")
        return False
    
    if is_element_present(driver, "//*[contains(@href, '/explore/')]"):
        print("\n")
        print("Login confirmado com sucesso.")
        return True
    
    print("Erro desconhecido durante o login.")
    return False

def is_element_present(driver, xpath):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return True
    except:
        return False

def get_post_details(driver):
    try:
        wait = WebDriverWait(driver, 10)
        
        user_element = driver.find_element(By.CSS_SELECTOR, "a._acan")
        username = user_element.text

        description_element = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'h1._ap3a._aaco._aacu._aacx._aad7._aade')
        ))
        description = description_element.get_attribute("innerText")

        date_element = wait.until(EC.presence_of_element_located((By.XPATH, "//time")))
        date = date_element.get_attribute("title")

        print(f"Nome de usuário que realizou postagem: {username}")
        print(f"Descrição: {description}")
        print(f"Data: {date}")

    except Exception as e:
        print("Erro ao coletar dados do post:", e)

def get_total_likes(driver):
    try:
        likes_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//section//span[contains(text(), 'curtidas') or contains(text(), 'likes')]/span"))
        )
        likes_text = likes_element.text.replace(',', '').replace('.', '')
        
        if 'K' in likes_text:
            likes = int(float(likes_text.replace('K', '')) * 1000)
        elif 'M' in likes_text:
            likes = int(float(likes_text.replace('M', '')) * 1000000)
        else:
            likes = int(likes_text)

        print(f"Número de curtidas: {likes}")
        print(f"\n")
        return likes
    except Exception as e:
        print(f"Erro ao coletar o número de curtidas: {e}")
        return 0


def collect_likes(driver):
    try:
        likers_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//section//span[contains(text(), 'curtidas') or contains(text(), 'likes')]/span"))
        )
        likers_button.click()
        print("Lista de 'likers' aberta.")
        
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@role='dialog']//ul"))
        )
        
        likers = []
        ###LINHA QUE FICA DANDO PROBLEMA
        likers_elements = driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/section[2]/div/div/a')

        for liker in likers_elements:
            likers.append(liker.text)
        
        print("Curtidores coletados:", likers)
        return likers
    except Exception as e:
        print(f"Erro ao coletar curtidas: {e}")
   
def collect_comments(driver):
    try:
        users = driver.execute_script('''
            return Array.from(document.querySelectorAll("div[role='dialog'] ul li a")).map(a => a.textContent);
        ''')

        filtered_users = [user for user in users if user and not user.startswith('@') and not any(char.isdigit() for char in user)]

        if filtered_users:
            filtered_users.pop(0)

        print(f"Lista de comentários coletada com sucesso: {len(filtered_users)} usuários.")
        for user in filtered_users:
            print(user)

    except Exception as e:
        print(f"Erro ao coletar a lista de comentários: {e}")


#ARCHLINUX 
#service = Service("/usr/bin/chromedriver") 
#driver = webdriver.Chrome(service=service)
#print(f"ChromeDriver Version: {driver.capabilities['chrome']['chromedriverVersion']}")
#print(f"Browser Version: {driver.capabilities['browserVersion']}") 

#WINDOWS
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

try:
    driver.get("https://www.instagram.com/accounts/login/")
    
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")
    
    type_like_a_human(username_input, username)
    type_like_a_human(password_input, password)
    
    password_input.send_keys("\n")

    if not check_login_errors(driver):
        print("Erro durante o login, verifique as credenciais.")
    else:   
        click_not_now(driver)
        time.sleep(5)

        driver.get("https://www.instagram.com/pucmgpocos/")

        time.sleep(5)
        first_post = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "_aagw"))
        )

        driver.execute_script("arguments[0].click();", first_post)
        print("Primeiro post acessado com sucesso.")
        print("\n")
        time.sleep(3)
        
        get_post_details(driver)
        get_total_likes(driver)
        collect_likes(driver)
        collect_comments(driver)
        
except Exception as e:
    print(f"Erro ao acessar o primeiro post: {e}")
    
finally:
    driver.quit()
    print("Navegador fechado.")

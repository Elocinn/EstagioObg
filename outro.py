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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
#from bs4 import BeautifulSoup

def is_element_present(driver, xpath):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return True
    except:
        return False
    
def type_like_a_human(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.2, 2.0)) 

def check_login_errors(driver):
    if is_element_present(driver, "//p[contains(text(), 'senha incorreta')]"):
        print("Erro de login: Senha incorreta.")
        return False
    elif is_element_present(driver, "//p[contains(text(), 'não corresponde a uma conta')]"):
        print("Erro de login: Nome de usuário inválido.")
        return False
    
    if is_element_present(driver, "//*[contains(@href, '/explore/')]"):
        print("Login confirmado com sucesso.")
        return True
    
    print("Erro desconhecido durante o login.")
    return False

def click_not_now(driver):
    try:
        not_now_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Agora não')]"))
        )
        not_now_button.click()
        print("'Agora não' clicado com sucesso.")
    except Exception as e:
        print(f"Erro ao clicar em 'Agora não': {e}")

def login(driver, username, password):
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
        return False
    else:
        click_not_now(driver)
        return True
    
def click_search_icon(driver):
    try:
        search_icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@aria-label='Pesquisar']"))
        )
        search_icon.click()
        print("Ícone de pesquisa clicado com sucesso.")
    except Exception as e:
        print(f"Erro ao clicar no ícone de pesquisa: {e}")

def type_in_search_field(driver, search_text):
    try:
        search_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Pesquisar']"))
        )
        search_field.send_keys(search_text)
        print("Texto digitado no campo de pesquisa com sucesso.")
    except Exception as e:
        print(f"Erro ao digitar no campo de pesquisa: {e}")

def click_first_search_result(driver):
    try:
        first_result = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='none']//a"))
        )
        first_result.click()
        print("Primeiro resultado de pesquisa clicado com sucesso.")
    except Exception as e:
        print(f"Erro ao clicar no primeiro resultado de pesquisa: {e}")

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
        datetime_str = date_element.get_attribute("datetime")
        
        # Converte o atributo datetime para um formato legível
        post_datetime = datetime.fromisoformat(datetime_str.replace("Z", "+00:00"))

        print(f"Nome de usuário que realizou postagem: {username}")
        print(f"Descrição: {description}")
        print(f"Data e Hora da postagem: {post_datetime.strftime('%Y-%m-%d %H:%M:%S')}")

    except Exception as e:
        print("Erro ao coletar dados do post:", e)

def get_likes_and_collect_likers(driver):
    try:
        likers_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//section//span[contains(text(), 'curtidas') or contains(text(), 'likes')]/span"))
        )
        
        driver.execute_script("arguments[0].click();", likers_button)
        print("Lista de 'likers' aberta.")
        
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@role='dialog']//ul"))
        )
        
        likers = []
        likers_elements = driver.find_elements(By.XPATH, "//div[@role='dialog']//div[@class='x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1']")
        print(f"Elementos encontrados: {len(likers_elements)}")  
        for liker in likers_elements[1:]: 
            liker_text = liker.text.strip()
            if liker_text:
                likers.append(liker_text)

        likers = list(set(likers))
        print(", ".join(likers))
        return likers
    except Exception as e:
        print(f"Erro ao coletar curtidores: {e}")
        return []

def collect_comments(driver):
    try:
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@role='dialog']//ul"))
        )
        
        comments = []
        comment_elements = driver.find_elements(By.XPATH, "//div[@role='dialog']//ul//li//span[@class='x1lliihq x193iq5w x6ikm8r x10wlt62 xlyipyv xuxw1ft']")

        for comment in comment_elements[1:]:
            comment_text = comment.text.strip()
            if comment_text and not comment_text.startswith('@') and not any(char.isdigit() for char in comment_text):
                comments.append(comment_text)
        
        comments = list(filter(None, comments))
        comments = list(set(comments))
        
        print(f"\nComentários coletados: {comments}")
        return comments
    except Exception as e:
        print(f"Erro ao coletar comentários: {e}")
    return []

def main():
    username = os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("INSTAGRAM_PASSWORD")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        if login(driver, username, password):
            time.sleep(5)
            print("Login bem-sucedido")
            click_search_icon(driver)
            type_in_search_field(driver, "pucmgpocos")
            time.sleep(2)
            click_first_search_result(driver)
            time.sleep(5)
            
            first_post = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "_aagw"))
            )
            driver.execute_script("arguments[0].click();", first_post)
            print("Primeiro post acessado com sucesso.")
            time.sleep(3)
            
            get_post_details(driver)
            get_likes_and_collect_likers(driver)
            collect_comments(driver)
            
    except Exception as e:
        print(f"Erro durante a execução: {e}")
        
    finally:
        driver.quit()
        print("Navegador fechado.")

if __name__ == "__main__":
    main()

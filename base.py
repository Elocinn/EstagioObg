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

load_dotenv()

username = os.getenv("INSTAGRAM_USERNAME")
password = os.getenv("INSTAGRAM_PASSWORD")

if not username or not password:
    raise ValueError("As variáveis de ambiente INSTAGRAM_USERNAME e INSTAGRAM_PASSWORD não estão definidas.")

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

def type_in_search_field(driver, search_text):
    try:
        search_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Pesquisar']"))
        )
        
        type_like_a_human(search_field, search_text)
        print("Texto digitado no campo de pesquisa com sucesso!")
        
    except Exception as e:
        print(f"Erro ao tentar digitar no campo de pesquisa: {e}")
        
def click_first_search_result(driver):
    try:
        # Localiza o primeiro elemento que corresponde à classe fornecida
        first_result = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "x1i10hfl.x1qjc9v5.xjbqb8w.xjqpnuy.xa49m3k.xqeqjp1.x2hbi6w.x13fuv20.xu3j5b3.x1q0q8m5.x26u7qi.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xdl72j9.x2lah0s.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x2lwn1j.xeuugli.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1n2onr6.x16tdsg8.x1hl2dhg.xggy1nq.x1ja2u2z.x1t137rt.x1q0g3np.x87ps6o.x1lku1pv.x1a2a7pz.x1dm5mii.x16mil14.xiojian.x1yutycm.x1lliihq.x193iq5w.xh8yej3"))
        )
        first_result.click()
        print("Primeiro resultado clicado com sucesso!")
        
    except Exception as e:
        print(f"Erro ao tentar clicar no primeiro resultado: {e}")
        
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
        
def get_likes(driver):
    try:
        print("Iniciando coleta de curtidas...")
        
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
        return likes
    except Exception as e:
        print(f"Erro ao coletar curtidas: {e}")
        return 0
    
def collect_likers(driver):
    try:
        print("Iniciando coleta de curtidores...")
        
        likers_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//section//span[contains(text(), 'curtidas') or contains(text(), 'likes')]/span"))
        )
        
        driver.execute_script("arguments[0].click();", likers_button)
        print("Lista de 'likers' aberta.")
        
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@role='dialog']//ul"))
        )
        
        likers = []
        #likers_elements = driver.find_elements(By.XPATH, "//div[@role='dialog']//div[@class='x1dm5mii x16mil14 xiojian x1yutycm x1lliihq x193iq5w xh8yej3']//span")
        #likers_elements = driver.find_elements(By.XPATH, "//div[@role='dialog']//div[@class='x9f619 x1ja2u2z x78zum5 x1n2onr6 x1iyjqo2 xs83m0k xeuugli x1qughib x6s0dn4 x1a02dak x1q0g3np xdl72j9']//span")
        #likers_elements = driver.find_elements(By.XPATH, "//div[@role='dialog']//div[contains(@class, 'x9f619') and contains(@class, 'x1ja2u2z')]//span[contains(@class, '_ap3a') and contains(@class, '_aaco')]")
        
        likers_elements = driver.find_elements(By.XPATH, "//div[@role='dialog']//div[@class='x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s x1q0g3np xqjyukv x6s0dn4 x1oa3qoh x1nhvcw1']")
        print(f"Elementos encontrados: {len(likers_elements)}")  
        for liker in likers_elements[1:]: 
            #liker_text = liker.get_attribute("innerHTML").strip()
            #liker_text = liker.get_attribute("href").split("/")[-2].strip()
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
        comment_elements = driver.find_elements(By.CSS_SELECTOR, "a.x1i10hfl.xjqpnuy.xa49m3k.xqeqjp1.x2hbi6w.xdl72j9.x2lah0s.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x2lwn1j.xeuugli.x1hl2dhg.xggy1nq.x1ja2u2z.x1t137rt.x1q0g3np.x1lku1pv.x1a2a7pz.x6s0dn4.xjyslct.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x9f619.x1ypdohk.x1f6kntn.xwhw2v2.xl56j7k.x17ydfre.x2b8uid.xlyipyv.x87ps6o.x14atkfc.xcdnw81.x1i0vuye.xjbqb8w.xm3z3ea.x1x8b98j.x131883w.x16mih1h.x972fbf.xcfux6l.x1qhh985.xm0m39n.xt0psk2.xt7dq6l.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1n2onr6.x1n5bzlp.xqnirrm.xj34u2y.x568u83")

        for index, element in enumerate(comment_elements):
            print(f"Elemento {index}: {element.get_attribute('outerHTML')}")
 
        for comment_element in comment_elements:
            try:
                user_name = comment_element.text.strip()
                if user_name:
                    comments.append(user_name)
            except Exception as e:
                print(f"Erro ao processar comentário: {e}")
        
        comments = list(set(comments))  # Remove duplicatas
        
        print(f"\nUsuários que comentaram: {comments}")
        return comments
    except Exception as e:
        print(f"Erro ao coletar comentários: {e}")
    return []


#ARCHLINUX 
#service = Service("/usr/bin/chromedriver") 
#driver = webdriver.Chrome(service=service)
#print(f"ChromeDriver Version: {driver.capabilities['chrome']['chromedriverVersion']}")
#print(f"Browser Version: {driver.capabilities['browserVersion']}") 

#WINDOWS
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

try:
    if login(driver, username, password):
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
        get_likes_and_collect_likers(driver)
        collect_comments(driver)
        
except Exception as e:
    print(f"Erro ao acessar o primeiro post: {e}")
    
finally:
    driver.quit()
    print(f"\n")
    print("Navegador fechado.")

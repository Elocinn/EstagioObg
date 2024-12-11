import os
import random
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


from dotenv import load_dotenv
#from bs4 import BeautifulSoup

load_dotenv()

username = os.getenv("INSTAGRAM_USERNAME")
password = os.getenv("INSTAGRAM_PASSWORD")

if not username or not password:
    raise ValueError("As variáveis de ambiente INSTAGRAM_USERNAME e INSTAGRAM_PASSWORD não estão definidas.")

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
        return True
    
    print("Erro desconhecido durante o login.")
    return False

def click_not_now(driver):
    try:
        not_now_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[text()='Agora não']"))
        )
        not_now_button.click()
    except Exception as e:
        print(f"'Agora não' não foi encontrado: {e}")
        time.sleep(2)
        

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
        tools_container = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "x1iyjqo2.xh8yej3"))
        )
        
        tools = tools_container.find_elements(By.CLASS_NAME, "x1n2onr6.x6s0dn4.x78zum5")
        
        if len(tools) > 2: 
            search_tool = tools[2]  #terceiro item
            search_tool.click()
            time.sleep(2)

    
def type_in_search_field(driver, search_text):
        search_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Pesquisar']"))
        )
        
        type_like_a_human(search_field, search_text)
        time.sleep(2)       
        

def click_first_search_result(driver):
    try:
        first_result = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "x1i10hfl.x1qjc9v5.xjbqb8w.xjqpnuy.xa49m3k.xqeqjp1.x2hbi6w.x13fuv20.xu3j5b3.x1q0q8m5.x26u7qi.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xdl72j9.x2lah0s.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x2lwn1j.xeuugli.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1n2onr6.x16tdsg8.x1hl2dhg.xggy1nq.x1ja2u2z.x1t137rt.x1q0g3np.x87ps6o.x1lku1pv.x1a2a7pz.x1dm5mii.x16mil14.xiojian.x1yutycm.x1lliihq.x193iq5w.xh8yej3"))
        )
        first_result.click()
        
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
        
        post_datetime = datetime.fromisoformat(datetime_str.replace("Z", "+00:00"))

        is_video = False
        try:
            video_element = driver.find_element(By.CSS_SELECTOR, "video")
            is_video = True
        except:
            pass

        post_type = "Vídeo" if is_video else "Foto"

        print(f"Nome de usuário que realizou postagem: {username}")
        print(f"Descrição: {description}")
        print(f"Data e Hora da postagem: {post_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Tipo de postagem: {post_type}")



    except Exception as e:
        print("Erro ao coletar dados do post:", e)
        
def get_likes(driver):
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
        return likes
    except Exception as e:
        print(f"Erro ao coletar curtidas: {e}/n")
        return 0

def open_likers_list(driver):
    try:
        likers_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//section//span[contains(text(), 'curtidas') or contains(text(), 'likes')]/span"))
        )
        driver.execute_script("arguments[0].click();", likers_button)

        WebDriverWait(driver, 40).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@role='dialog']//ul"))
        )
    except Exception as e:
        print(f"Erro ao abrir a lista de curtidores: {e}")

def collect_likers(driver):
    try:
        likers_elements = driver.find_elements(By.XPATH, "//div[@role='dialog']//div[@class='x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s x1q0g3np xqjyukv x6s0dn4 x1oa3qoh x1nhvcw1']")        
        likers = []
        
        for liker in likers_elements[1:]:  #índice 0
            liker_text = liker.text.strip()
            if liker_text and not any(keyword in liker_text for keyword in ["há", "dias", "semanas", "meses", "anos"]):
                likers.append(liker_text)

        likers = list(set(likers))
        return likers
    except Exception as e:
        print(f"Erro ao coletar curtidores: {e}")
        return []
        
def scroll_like_human_likers(driver, max_scrolls=10):
    # OS XPATHS MUDAM ENTRE NAVEGADORES
    like_list_xpath_1 = "/html/body/div[7]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div"
    like_list_xpath_2 = "/html/body/div[6]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div"
    time.sleep(1)
    for _ in range(max_scrolls):
        try:
            like_list = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, like_list_xpath_1)))
        except TimeoutException:
            try:
                like_list = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, like_list_xpath_2)))
            except TimeoutException:
                print("Não conseguiu localizar o elemento após a rolagem1.")
                return
    
    last_height = driver.execute_script("return arguments[0].scrollHeight", like_list)
    
    for _ in range(max_scrolls):
        driver.execute_script("arguments[0].scrollTop += arguments[0].offsetHeight", like_list)
        time.sleep(random.uniform(1, 3)) 
        
        try:
            WebDriverWait(driver, 5).until(EC.staleness_of(like_list)) 
        except TimeoutException:
            pass
        
        try:
            like_list = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, like_list_xpath_1)))
        except TimeoutException:
            try:
                like_list = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, like_list_xpath_2)))
            except TimeoutException:
                print("Não conseguiu localizar o elemento após a rolagem2.")
                return
        
        new_height = driver.execute_script("return arguments[0].scrollHeight", like_list)
        if new_height == last_height:
            break
        last_height = new_height

def scroll_and_collect_likers(driver, max_scrolls=10):
    all_likers = set()
    for _ in range(max_scrolls):
        scroll_like_human_likers(driver, 1)  
        likers = collect_likers(driver)
        all_likers.update(likers)
        time.sleep(random.uniform(1, 3))  
        if len(likers) == 0:
            break 
    return list(all_likers)

def collect_comments(driver):
    try:
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@role='dialog']//ul"))
        )
        
        comments = []
        comment_elements = driver.find_elements(By.CSS_SELECTOR, "a.x1i10hfl.xjqpnuy.xa49m3k.xqeqjp1.x2hbi6w.xdl72j9.x2lah0s.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x2lwn1j.xeuugli.x1hl2dhg.xggy1nq.x1ja2u2z.x1t137rt.x1q0g3np.x1lku1pv.x1a2a7pz.x6s0dn4.xjyslct.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x9f619.x1ypdohk.x1f6kntn.xwhw2v2.xl56j7k.x17ydfre.x2b8uid.xlyipyv.x87ps6o.x14atkfc.xcdnw81.x1i0vuye.xjbqb8w.xm3z3ea.x1x8b98j.x131883w.x16mih1h.x972fbf.xcfux6l.x1qhh985.xm0m39n.xt0psk2.xt7dq6l.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1n2onr6.x1n5bzlp.xqnirrm.xj34u2y.x568u83")

        for comment_element in comment_elements:
            try:
                user_name = comment_element.text.strip()
                if user_name:
                    comments.append(user_name)
            except Exception as e:
                print(f"Erro ao processar comentário: {e}")
        
        comments = list(set(comments))
        
        print(f"\nUsuários que comentaram: {comments}")
        return comments
    except Exception as e:
        print(f"Erro ao coletar comentários: {e}")
    return []

def scroll_like_human_page(driver, scroll_pause_time=2, max_scrolls=10):
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    for _ in range(max_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        time.sleep(scroll_pause_time + random.uniform(0, 2))
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height == last_height:
            break
        
        last_height = new_height
        
def exit(driver):
    try:
        actions = ActionChains(driver)
        actions.send_keys(Keys.ESCAPE).perform()
        time.sleep(1)
    except Exception as e:
        print(f"Erro ao sair do post: {e}")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

if login(driver, username, password):
    print("Login realizado com sucesso!")

click_search_icon(driver)

search_text = "napucminas"
type_in_search_field(driver, search_text)
    
click_first_search_result(driver)
time.sleep(1)


elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".x1lliihq.x1n2onr6.xh8yej3.x4gyw5p.x1ntc13c.x9i3mqj.x11i5rnm.x2pgyrj")))
#element = driver.find_element(By.XPATH, "//*[contains(@class, 'x1lliihq') and contains(@class, 'x1n2onr6') and contains(@class, 'xh8yej3') and contains(@class, 'x4gyw5p') and contains(@class, 'x1ntc13c') and contains(@class, 'x9i3mqj') and contains(@class, 'x11i5rnm') and contains(@class, 'x2pgyrj')]")

for index in range(len(elements)):
    time.sleep(1)
    print(f"Clicando no post {index + 1} de {len(elements)}")
    elements[index].click()
    time.sleep(2)
    
    print(f"Coletando dados do post {index + 1}...")
    get_post_details(driver)
    time.sleep(2)
            
    get_likes(driver)
    time.sleep(1)

    open_likers_list(driver)
    time.sleep(2)
    likers = scroll_and_collect_likers(driver,max_scrolls=5)
    print(likers)
    time.sleep(1)

    collect_comments(driver)
    time.sleep(2)
            
    driver.back()
    time.sleep(2)
        
    elements = driver.find_elements(By.CSS_SELECTOR, ".x1lliihq.x1n2onr6.xh8yej3.x4gyw5p.x1ntc13c.x9i3mqj.x11i5rnm.x2pgyrj")

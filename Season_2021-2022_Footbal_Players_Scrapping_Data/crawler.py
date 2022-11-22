from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import os


PATH = "./driver/chromedriver"
service = Service(executable_path=PATH)
options = Options()
options.headless = True #False para visualizar o navegador atuar de forma automática
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
options.add_argument(f'user-agent={user_agent}')
clear = lambda: os.system('clear')


def crawler(url,table_id):
    
    """ 
    - Recebe como argumento uma url do FBREF e uma id de tabela da liga onde 
    serão realizados os clicks em cada time, o que redireciona para a página com 
    estátistica dos jogadores. 
    - Retorna um dicionário no formato {nome do time: URL das esta-
    tísticas dos jogadores}  
    
    """
    
    equipes = []
    urls = []

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    driver.maximize_window()


    table = driver.find_element(By.ID, table_id)
    teams = table.find_elements(By.XPATH, './/td[@data-stat="squad"]/a')
    for team in teams:
        equipes.append(team.text)

    print("\n\nObtendo URLs:")

    for i in range(len(teams)):
        #Loop para obter as URLs de cada time presente na tabela  
        
        table = driver.find_element(By.ID, table_id)
        teams = table.find_elements(By.XPATH, './/td[@data-stat="squad"]/a')

        actions = ActionChains(driver)

        #ignora o erro boundary gerado por move_to_element()
        try:
            actions.move_to_element(teams[i+1]).perform()
        except:
            pass

        time.sleep(4) #espera para nao mover e clicar ao mesmo tempo

        teams[i].click() #efetua o click

        # click no AD do google quando presente. Necessita mudar para o frame do botão de fechar.
        try:
            wait=WebDriverWait(driver, 4)
            wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'aswift_2')))
            ad_button = driver.find_element(By.XPATH, '//div[contains(@id, "dismiss-button")]')
            ad_button.click()
            driver.switch_to.parent_frame()
        except:
            pass

        # recupera a URL da página com estatística dos jogadores
        page = driver.current_url

        
        print(f"{equipes[i]} ----------- {page}")

        urls.append(page)

        driver.back()
    
    driver.quit()
    clear()
    
    #gera resultado final na forma de dicionário
    urls_dic = {}
    for equipe, url in zip(equipes, urls):
        urls_dic[equipe] = url
    
    
    return urls_dic

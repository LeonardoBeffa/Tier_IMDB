import os
import re
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

os.system('cls')

caminho = 'Endereço de salvamento'
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}

url_filme = 'https://m.imdb.com/chart/top/?sort=release_date%2Cdesc'
url_serie = 'https://www.imdb.com/chart/toptv/'

dic_Filmes = {'Nome':[],'Ano':[],'Tempo':[],'Nota':[]}
dic_Serie = {'Nome':[],'Ano':[],'Tempo':[],'Nota':[]}

def tier_IMDB(dic, url_page, tipo):
    browser_options = Options()
    browser_options.add_argument('--headless')
    driver = webdriver.Firefox(options=browser_options)
    driver.get(url_page)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    page_content = driver.page_source
    soup = BeautifulSoup(page_content, 'html.parser')
    tiers = soup.find_all('div', class_=re.compile('cli-children'))

    for tier in tiers:
        h3_element = tier.find('h3', class_='ipc-title__text')
        first_space_index = h3_element.text.find(' ')
        nome = h3_element.text[first_space_index + 1:]
        ano = tier.find('span', class_=re.compile('cli-title-metadata-item')).text
        tempo = tier.find('span', class_=re.compile('cli-title-metadata-item')).find_next_sibling('span').text
        nota = tier.find('div', class_=re.compile('cli-ratings-container')).text[0:3]

        dic['Nome'].append(nome)
        dic['Ano'].append(ano)
        dic['Tempo'].append(tempo)
        dic['Nota'].append(nota)

        print(f'Nome: {nome} Ano: {ano} Tempo: {tempo} Nota: {nota}')
    
    driver.quit()
    
    df = pd.DataFrame(dic)
    df.to_csv(f'{caminho}/IMDB-Top-250-{tipo}.csv', encoding='utf-8', sep=';')

print('Incio do Programa.')
tier_IMDB(dic_Filmes, url_filme, tipo='Filmes')             
tier_IMDB(dic_Serie, url_serie, tipo='Series')
print('Fim!')

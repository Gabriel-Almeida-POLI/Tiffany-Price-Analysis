from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from datetime import date
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

options = Options()

hoje = date.today()

navegador = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


with open('precos_pedra_tiffany.csv', 'a', newline='', encoding='UTF-8') as f:
    linha = str(hoje) + '\n'
    f.write(linha)

k = 0
i = 0
compr = 1
url = 'https://www.tiffany.com.br/jewelry/shop/'
types = ['rings','necklaces-pendants','bracelets','earrings','brooches']


while k <= 5:
    if i <= 4:
        print(url + types[k] + '/sort-relevance/?page=' + str(i))
        navegador.get(url + types[k] + '/sort-relevance/?page=' + str(i))

        sleep(3)
        last_height = navegador.execute_script("return document.body.scrollHeight")

        for contador in range(20):
            navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            sleep(4)

            new_height = navegador.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break

            last_height = new_height

        site = BeautifulSoup(navegador.page_source, 'html.parser')

        produtos = site.find_all('div', class_='product-tile__details')

        for produto in produtos:
            print(produto)
            try:
                nome = produto.find('span', class_='product-tile__details_name__split').get_text().strip() + produto.find_all('span', class_='product-tile__details_name__split')[1].get_text().strip()
                preco = produto.find('p', class_='product-tile__details_price').get_text().strip()
            except:

                print('erro')

            with open('precos_pedra_tiffany.csv', 'a', newline='', encoding='UTF-8') as f:
                linha = nome + ';' + preco + '\n'
                f.write(linha)

        i = i + 1

    else:
        k = k + 1


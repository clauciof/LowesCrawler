import scrapy
import bs4
from selenium import webdriver
import pandas as pd
import csv


class LowesSpider(scrapy.Spider):
    name = "lowes"

    #informacoes do produto que serão capturadas
    urls = []
    titulos = []
    skus = []
    models = []
    marcas = []
    estrelas = [] 
    avaliacoes = []
    #offset de paginacao
    offset = 0
    
    #url de inicio usada pelo spider
    start_urls = ['https://www.lowes.com/pl/Savings/4294593284?catalog=4294857973'] 

    def parse(self, response):
        urls = []
    
        while (self.offset<=756):
            urls.append('https://www.lowes.com/pl/Savings/4294593284?offset='+str(self.offset)+'&catalog=4294857973')
            self.offset = self.offset + 36
            
        for url in urls:
            self.urls = []
            self.titulos = []
            self.skus = []
            self.models = []
            self.marcas = []
            self.estrelas = [] 
            self.avaliacoes = []

            #configurando webdriver do selenium
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166")


            #build do browser
            driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='C:\\Users\\clauc\\Downloads\\CursoICMCPython\\InstaScraping\\chromedriver.exe')
            driver.get(url)
            soup = bs4.BeautifulSoup(driver.page_source, 'lxml')


            hrefs = soup.find_all('a', href=True) #capturando cada <a> contendo urls #ok
            Ids = soup.find_all('span', class_="tooltip-custom")#ok
            reviews = soup.find_all('span', class_="styles__TotalWrap-sc-5hhhh2-4 gmWgqG total") #ok
            stars = soup.find_all('div', class_="styles__RatingDiv-sc-5hhhh2-2 ElZBP") #estrelas de avaliaçao do produto, vao de 0 a 5 #ok
            marcas_span = soup.find_all('span', class_="sc-1b7wdu0-9 cjoVtZ")#ok
            titulos_span = soup.find_all('span', class_="sc-1b7wdu0-10 fcieOM")#ok
            
            #avalaiacoes e estrelas
            self.estrelas = [float(s['aria-label'].split()[0]) for s in stars]
            self.avaliacoes = [r.text for r in reviews]
            
            #capturando urls válidas dos produtos
            urls = ['https://www.lowes.com'+href['href'] for href in hrefs[23:] if '/pd/' in href['href']]
            self.urls = list(dict.fromkeys(urls))      #eliminando duplicados   
        

            #separando marcas e titulos de cada <span> capturada
            self.marcas = [m.text for m in marcas_span]
            
            for titulos_ in titulos_span:
                aux = ''
                for t in titulos_.text.split()[1:]:
                    aux = aux+" "+t
                self.titulos.append(aux)
            

            #separando Id unico e o Modelo
            i = 0
            for id_ in Ids:
                if (i%2 == 0):
                    self.skus.append(id_.text.split()[1])
                else:
                    self.models.append(id_.text.split()[1])
                i = i + 1

            #salvando em um csv
            self.create_csv(self.skus, self.models, self.marcas, self.titulos, self.estrelas, self.avaliacoes, self.urls)     
        

    def create_csv(self, skus, models, marcas, titulos, estrelas, avaliacoes, urls):
        data = self.trata_nulos(skus, models, marcas, titulos, estrelas, avaliacoes, urls) #trata dados que vieram nulos 
        df = pd.DataFrame(data=data)

        with open('lowes.csv', 'a') as f:
            df.to_csv(f, header=f.tell()==0, index=False)
        
        return 1


    def trata_nulos(self, skus, models, marcas, titulos, estrelas, avaliacoes, urls):
        #trata tamanhos diferentes:
        if len(skus)<36:
            for i in range(0, 36-len(skus)):
                skus.append("N/D")
        if len(models)<36:
            for i in range(0, 36-len(models)):
                models.append("N/D")
        if len(marcas)<36:
            for i in range(0, 36-len(marcas)):
                marcas.append("N/D")
        if len(titulos)<36:
            for i in range(0, 36-len(titulos)):
                titulos.append("N/D")
        if len(estrelas)<36:
            for i in range(0, 36-len(estrelas)):
                estrelas.append(float(-1))
        if len(avaliacoes)<36:
            for i in range(0, 36-len(avaliacoes)):
                avaliacoes.append(float(-1))
        if len(urls)<36:
            for i in range(0, 36-len(urls)):
               urls.append("N/D")            

        data = { 'Id':skus, 'Titulo':titulos, 'Modelo':models, 'Marca':marcas, 'Estrelas':estrelas, 'Avaliacoes':avaliacoes, 'Url':urls}
        return data
    
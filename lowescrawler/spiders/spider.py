import scrapy
from bs4 import BeautifulSoup
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
        soup = BeautifulSoup(response.body, 'lxml')
        descricao_span = response.xpath('//span[@class="sc-1b7wdu0-10 fcieOM"]//text()').getall() #capturando cada <span> contendo marca e descricao dos produtos
        hrefs = soup.find_all('a', href=True) #capturando cada <a> contendo urls
        Ids =  response.xpath('//span[@class="tooltip-custom"]//text()').getall() #selecionando as <span> que contem os Ids e Models
        reviews = response.xpath('//span[@class="styles__TotalWrap-sc-5hhhh2-4 gmWgqG total"]//text()').getall() #quantidade de reviews
        stars = soup.find_all('div', class_="styles__RatingDiv-sc-5hhhh2-2 ElZBP") #estrelas de avaliaçao do produto, vao de 0 a 5
        
        #avalaiacoes e estrelas
        self.estrelas = [float(s['aria-label'].split()[0]) for s in stars]
        self.avaliacoes = [int(r) for r in reviews]
        
        #capturando urls válidas dos produtos
        urls = ['https://www.lowes.com'+href['href'] for href in hrefs[23:] if '/pd/' in href['href']]
        self.urls = list(dict.fromkeys(urls))      #eliminando duplicados   
       
        #separando marcas e descricao de cada <div> capturada
        self.marcas = [descricao_span[i] for i in range(0, len(descricao_span), 3)]
        self.titulos = [descricao_span[i+2] for i in range(0, len(descricao_span), 3)]
        
        #separando Id unico e o Modelo
        self.skus = [Ids[i+1] for i in range(0,len(Ids),4)]
        self.models = [Ids[i+3] for i in range(0,len(Ids),4)]

        #salvando em um csv
        self.create_csv(self.skus, self.models, self.marcas, self.titulos, self.estrelas, self.avaliacoes, self.urls)     
        
        #segue para a proxima pagina
        while (self.offset<=756):
            self.offset = self.offset + 36
            proxima_url = 'https://www.lowes.com/pl/Savings/4294593284?offset='+str(self.offset)+'&catalog=4294857973'       
            yield scrapy.Request( proxima_url, callback=self.parse)


    def create_csv(self, skus, models, marcas, titulos, estrelas, avaliacoes, urls):
        data = { 'Id':skus, 'Titulo':titulos, 'Modelo':models, 'Marca':marcas, 'Estrelas':estrelas, 'Avaliacoes':avaliacoes, 'Url':urls}
        df = pd.DataFrame(data=data)

        with open('lowes.csv', 'a') as f:
            df.to_csv(f, header=f.tell()==0, index=False)
        
        return 1

    
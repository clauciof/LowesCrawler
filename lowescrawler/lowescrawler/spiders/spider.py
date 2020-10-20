import scrapy
from bs4 import BeautifulSoup

class LowesSpider(scrapy.Spider):
    name = "lowes"

    #informacoes do produto que serão capturadas
    urls = []
    titulos = []
    skus = []
    models = []
    marcas = []
    precos = []
    avaliacoes = [] 
    n_avaliacaos = []
    delivery_infos = []
    availables = []
    
    #url de inicio usada pelo spider
    start_urls = ['https://www.lowes.com/pl/Savings/4294593284?catalog=4294857973'] 

    

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        descricao_span = response.xpath('//span[@class="sc-1b7wdu0-10 fcieOM"]//text()').getall() #capturando cada <span> contendo marca e descricao dos produtos
        hrefs = soup.find_all('a', href=True) #capturando cada <a> contendo urls
        Ids =  response.xpath('//span[@class="tooltip-custom"]//text()').getall() #selecionando as <span> que contem os Ids e Models

        #capturando urls válidas dos produtos
        urls = [href['href'] for href in hrefs[23:] if '/pd/' in href['href']]
        urls = list(dict.fromkeys(urls))      #eliminando duplicados

        #for url in urls:
        #    captura_preco(url)
       
        #separando marcas e descricao de cada <div> capturada
        self.marcas = [descricao_span[i] for i in range(0, len(descricao_span), 3)]
        self.titulos = [descricao_span[i+2] for i in range(0, len(descricao_span), 3)]
        
        #separando Id unico e o Modelo
        self.skus = [Ids[i+1] for i in range(0,len(Ids),4)]
        self.models = [Ids[i+3] for i in range(0,len(Ids),4)]

        print(self.skus, self.models)
        print(self.marcas, self.titulos)

            
    def captura_preco(self, url):
        #request na url
        #parser do preco
        #self.precos.append(preco)
        pass
       
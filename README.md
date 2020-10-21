# LowesCrawler
Spider desenvolvido para capturar dados de produtos do https://www.lowes.com/

## Descrição 
Spider construído em Python com o framework Scrapy. Acessa o site https://www.lowes.com/ e captura as seguintes informaçoes:
#### Id | Titulo | Modelo | Marca | Estrelas | Avaliacoes | URL

No final obtem-se um arquivo csv com os dados obtidos

### Pré Requisitos

Python3 e bibliotecas BeautifulSoup4, Pandas e Scrapy.

#### Instalação
```
pip install pandas
pip install Scrapy
pip install bs4
```

### Execução
O código do spider se encontra em 'LowesCrawler/lowescrawler/spiders/spider.py'

No diretório /spiders executar o comando:
```
scrapy runspider spider.py
```
ou
```
scrapy crawl lowes
```


# Amostras
![alt Text](https://github.com/clauciof/imagens/blob/master/analise1.png)


![alt Text](https://github.com/clauciof/imagens/blob/master/analise2.png)


## Autor

* **Cláucio Gonçalves Mendes de Carvalho Filho** - (https://www.linkedin.com/in/cl%C3%A1ucio-filho-646501132/)


# -*- coding: utf-8 -*-
import scrapy
'''
//*[@class="vaga hlisting"]/header/h2/a acha as a caixa das vagas
//article/header/h2/a/@href - pega ons links

titulo da vaga - //article/header/h1/span
cidade - //article/div[1]/dl[2]/dd/abbr
salario - //article/div[1]/dl[1]/dd (somente o dinheiro, n teem falando "faixa salaria de tanto e o dinheiro")
descrição - //article/div[2]/div[2]/p

botão de proximo - //*[@id="resultado-busca-vagas"]/footer/div[2]/ul/li[9]/a/@href
'''

class ProcuravagaSpider(scrapy.Spider):
    name = 'procuraVaga'
    #allowed_domains = ['www.manager.com.br/empregos-desenvolvedor-javascript/']
    start_urls = ['http://www.manager.com.br/empregos-desenvolvedor-javascript/']


    def parse(self, response):
        lista= response.xpath('//*[@class="lista-resultado-busca"]')

        for itemlita in lista:
            url=itemlita.xpath('//article/header/h2/a/@href').extract_first()
            yield scrapy.Request(url=url, callback=self.pega_info)
        proxpag=response.xpath('//*[@id="resultado-busca-vagas"]/footer/div[2]/ul/li[9]/a/@href')

        if proxpag:
            yield scrapy.Request(url=proxpag.extract_first(),callback=self.parse)


    def pega_info(self,response):
        titulovaga=response.xpath('//article/header/h1/span/text()').extract_first()
        salario=response.xpath('//article/div[1]/dl[1]/dd')
        cidade=response.xpath('//article/div[1]/dl[2]/dd/abbr')
        descriacao=response.xpath('//article/div[2]/div[2]/p')

        yield {
            'titulovaga':titulovaga,
            'salario': salario,
            'cidade': cidade,
            'descriacao': descriacao,
        }
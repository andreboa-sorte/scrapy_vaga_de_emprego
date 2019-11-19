# -*- coding: utf-8 -*-
import scrapy
#pip isntall scrapy
'''
(todos os xpath, montados e ultilizados no codigo)

//*[@class="vaga hlisting"]/header/h2/a - acha a caixa das vagas
//article/header/h2/a/@href - pega os links

titulo da vaga - //article/header/h1/span
cidade - //article/div[1]/dl[2]/dd/abbr
salario - //article/div[1]/dl[1]/dd (somente o dinheiro, n tem falando "faixa salaria de tanto e o dinheiro")
descrição - //article/div[2]/div[2]/p

botão de proximo - //*[@title="Vagas de Emprego de Desenvolvedor Javascript - Página Seguinte"]/a/@href
'''


class ProcuravagaSpider(scrapy.Spider):
    name = 'procuraVaga'
    #allowed_domains = ['www.manager.com.br/empregos-desenvolvedor-javascript/']
    start_urls = ['http://www.manager.com.br/empregos-desenvolvedor-javascript/'] #o link q sera "scrapydo"

    def parse(self, response):
        lista = response.xpath('//*[@class="lista-resultado-busca"]') #pega a caixa "grande" onde esta os resultados da busca

        for itemlita in lista: #um laço de repetição para pegar todos os dados da "caixa grande"
            url = itemlita.xpath('//article/header/h2/a/@href').extract_first() #pega todos os urls de cada proposta de emprego
            yield scrapy.Request(url=url, callback=self.pega_info) #manda outro requeste para a pagina, para pegar os dados da pagina de propsota de emprego
                                                                   #manda o resultado desse requeste, para o metodo "pega_info" por meio do callback
                                                                    #o "yield" é o comando ultilizado para ele fazer uma função ou interação
        proxpag = response.xpath('//*[@title="Vagas de Emprego de Desenvolvedor Javascript - Página Seguinte"]/a/@href')#se existir um botão de proxima pagina, ele pega o link da proxima pagina e bota na variavel

        if proxpag:#se existir o botão ele executa a função abaixo
            yield scrapy.Request(url=proxpag.extract_first(), callback=self.parse)#manda um request para a proxima pagina e passa os dados parap o prorio metodo, criando um "loop"

    def pega_info(self, response):
        #aqui nesse metodo é pego os dados que se deseja exrair e é botado nas variaveis
        titulovaga = response.xpath('//article/header/h1/span/text()').extract_first()
        salario = response.xpath('//article/div[1]/dl[1]/dd/text()').extract_first()
        cidade = response.xpath('//article/div[1]/dl[2]/dd/abbr/@title').extract_first()
        descriacao = response.xpath('//article/div[2]/div[2]/p/text()').extract_first()

        yield { #depois de coletados, as informações são organizadas para q possão ser salvas e são salvas depois
            'titulovaga': titulovaga,
            'salario': salario,
            'cidade': cidade,
            'descriacao': descriacao,
        }

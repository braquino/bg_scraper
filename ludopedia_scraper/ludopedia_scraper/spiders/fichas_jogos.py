# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
import os

class FichasSpider(scrapy.Spider):
    name = 'fichas_jogos'
    # import the newest file
    rank_path = sorted([x for x in os.listdir() if 'ludo_rankings' in x], reverse=True)[0]
    lista_jogos = pd.read_csv(rank_path)
    start_urls = lista_jogos['links'].values

    custom_settings = {'FEED_URI': "ludo_fichas_%(time)s.csv",
                       'FEED_FORMAT': 'csv'}

    def parse(self, response):

        jogo = response.xpath('//div[@class="jogo-top-main"]/h3/a/text()').extract_first()
        idade = response.xpath('//div[@class="jogo-top-main"]/ul/li[1]/text()').extract_first()
        tempo_jogo = response.xpath('//div[@class="jogo-top-main"]/ul/li[2]/text()').extract_first()
        n_jogadores = response.xpath('//div[@class="jogo-top-main"]/ul/li[3]/text()').extract_first()
        designers = str(response.xpath('//div[@class="jogo-top-main"]/div[@class="hidden-xs"]/span/a/text()').extract())
        editoras = str(response.xpath('//div[@class="jogo-top-main"]/span[@class="info-span text-sm"]/a/text()').extract())
        tenho = response.xpath('//button[@id="btn-colecao-fl-tem"]/text()').extract_first()[7:-1]
        quero = response.xpath('//button[@id="btn-colecao-fl-tem"]/text()').extract_first()[7:-1]
        tive = response.xpath('//button[@id="btn-colecao-fl-teve"]/text()').extract_first()[6:-1]
        favoritos = response.xpath('//button[@id="btn-colecao-fl-favorito"]/text()').extract_first()[10:-1]
        joguei = response.xpath('//button[@id="btn-colecao-fl-jogou"]/text()').extract_first()[8:-1]

        # create a dictionary to store the scraped info
        scraped_info = {
            'jogo': jogo
            , 'idade': idade
            , 'tempo_jogo': tempo_jogo
            , 'n_jogadores': n_jogadores
            , 'designers': designers
            , 'editoras': editoras
            , 'tenho': tenho
            , 'quero': quero
            , 'tive': tive
            , 'favoritos': favoritos
            , 'joguei': joguei
            , 'link': response.request.url
        }
        yield scraped_info






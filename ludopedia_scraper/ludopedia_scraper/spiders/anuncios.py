# -*- coding: utf-8 -*-
import scrapy


class AnunciosSpider(scrapy.Spider):
    name = 'anuncios'
    #allowed_domains = ['www.ludopedia.com.br/anuncios/']
    start_urls = ['https://www.ludopedia.com.br/anuncios/']

    custom_settings = {'FEED_URI': "ludo_anuncios_%(time)s.csv",
                       'FEED_FORMAT': 'csv'}
    encoding='latin1'

    def parse(self, response):
        tipos = response.css(".box-anuncio-title::text").extract()
        jogos = response.xpath('//a[@class="link-elipsis"]/text()').extract()
        cidade = response.xpath('//dl[@style="margin: 0px; margin-bottom:10px; font-size:90%"]/dd[1]/text()').extract()
        preco = response.xpath('//dd[@class="proximo_lance"]/text()').extract()
        row_data = zip(tipos, jogos, cidade, preco)
        for item in row_data:
            # create a dictionary to store the scraped info
            scraped_info = {
                'tipos': item[0],
                'jogos': item[1],
                'cidade': item[2],
                'preco': item[3],
            }
            yield scraped_info

            next_page = response.xpath('//li[@class="hidden-xs"]/a[@title="Próxima Página"]/@href').extract_first()
            if next_page:
                yield scrapy.Request(
                    response.urljoin(next_page),
                    callback=self.parse)
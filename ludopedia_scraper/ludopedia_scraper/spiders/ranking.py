# -*- coding: utf-8 -*-
import scrapy


class RankingSpider(scrapy.Spider):
    name = 'ranking'
    #allowed_domains = ['www.ludopedia.com.br/anuncios/']
    start_urls = ['https://www.ludopedia.com.br/ranking/']

    custom_settings = {'FEED_URI': "ludo_rankings_%(time)s.csv",
                       'FEED_FORMAT': 'csv'}
    encoding='latin1'

    def parse(self, response):
        ranks = response.xpath('//span[@class="rank"]/text()').extract()
        jogos = response.xpath('//h4[@class="media-heading"]/a/text()').extract()
        anos = response.xpath('//h4[@class="media-heading"]/small/i/text()').extract()
        links = response.xpath('//h4[@class="media-heading"]/a/@href').extract()
        scores = response.xpath('//div[@class="rank-info"]/span[1]/b/text()').extract()
        scores_medios = response.xpath('//div[@class="rank-info"]/span[2]/b/text()').extract()
        n_scores = response.xpath('//div[@class="rank-info"]/span[3]/a/b//text()').extract()

        row_data = zip(ranks, jogos, anos, links, scores, scores_medios, n_scores)
        for item in row_data:
            # create a dictionary to store the scraped info
            scraped_info = {
                  'ranks': item[0]
                , 'jogos': item[1]
                , 'anos': item[2]
                , 'links': item[3]
                , 'scores': item[4]
                , 'scores_medios': item[5]
                , 'n_scores': item[6]
            }
            yield scraped_info

            next_page = response.xpath('//li[@class="hidden-xs"]/a[@title="Próxima Página"]/@href').extract_first()
            if next_page:
                yield scrapy.Request(
                    response.urljoin(next_page),
                    callback=self.parse)
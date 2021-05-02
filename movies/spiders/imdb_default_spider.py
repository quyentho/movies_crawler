# -*- coding: utf-8 -*-
import scrapy
import logging

class ImdbDefaultSpiderSpider(scrapy.Spider):
    name = 'imdb_default_spider'
    allowed_domains = ['imdb.com']
    start_urls = ['https://m.imdb.com/feature/genre/?fbclid=IwAR1zFHoB1ajPSweIWYfH-hBxUO8Fa_roDPoBBqxPc_lD-6dgB_qi6PAnTGk']

    def parse(self, response):
        gendre_urls = response.xpath("//div[@class='image']/a/@href").getall()

        for page in gendre_urls:
            if page:
                yield response.follow(url = page, callback=self.parse_movie)
    
    def parse_movie(self,response):
        movie_urls = response.xpath("//h3[@class='lister-item-header']/a/@href").getall()
        for page in movie_urls:
            yield response.follow(url = page, callback=self.parse_item)

        next_page = response.xpath("(//a[@class='lister-page-next next-page'])[2]/@href").get()
        if next_page:
            yield response.follow(url = next_page, callback=self.parse_movie)
    
    def parse_item(self, response):
        title =  response.xpath("normalize-space(//div[@class='title_wrapper']/h1/text())").get()
        year = response.xpath("//div[@class='title_wrapper']/h1/span/a/text()").get()
        duration = response.xpath("normalize-space((//time)[1]/text())").get()
        rating = response.xpath("//div[@class='ratingValue']/strong/span/text()").get()
        release_date = response.xpath("normalize-space((//div[@id='titleDetails']/div/h4[contains(text(),'Release Date')]/parent::div/text())[2])").get()
        country = response.xpath("(//div[@id='titleDetails']/div/h4[contains(text(),'Country:')]/following-sibling::a/text())").get()
        storyline = response.xpath("normalize-space(//div[@id='titleStoryLine']/div/p/span/text())").get()
        cast = response.xpath("//div[@id='titleCast']//tr[contains(@class,'odd') or contains(@class,'even')]/td[2]/a/text()").getall()

        cast_normalize=[] 
        for cas in cast:
            cast_normalize.append(cas.strip())
        
        yield{
            'Title' : title,
            'Year' : year,
            'Duration' : duration,
            'Rating': rating,
            'Movie_url' : response.url,
            'Released_Date' : release_date,
            'Country' : country,
            'Storyline' : storyline,
            'Languages' : response.xpath("(//div[@id='titleDetails']/div/h4[contains(text(),'Language:')]/following-sibling::a/text())").getall(),
            'Gendres': response.xpath("(//div[@class='see-more inline canwrap'])[2]/a/text()").getall(),
            'Directors' : response.xpath("(//div[@class='credit_summary_item'])[1]/a/text()").getall(),
            'Writers' : response.xpath("(//div[@class='credit_summary_item'])[2]/a/text()").getall(),
            'Cast' : cast_normalize,
            'Award': response.xpath("normalize-space(//span[@class='awards-blurb']/b/text())").getall()
        }

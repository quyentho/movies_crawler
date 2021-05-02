# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.shell import inspect_response
class ImdbSpider(CrawlSpider):
    name = 'imdb'
    allowed_domains = ['imdb.com']
    start_urls = ['https://m.imdb.com/feature/genre/?fbclid=IwAR1zFHoB1ajPSweIWYfH-hBxUO8Fa_roDPoBBqxPc_lD-6dgB_qi6PAnTGk']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=("//div[@class='image']/a"))),
        Rule(LinkExtractor(restrict_xpaths=("//h3[@class='lister-item-header']/a")), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths=("(//a[@class='lister-page-next next-page'])[2]")))
    )

    def parse_item(self, response):

        title =  response.xpath("normalize-space(//div[@class='title_wrapper']/h1/text())").get()
        year = response.xpath("//div[@class='title_wrapper']/h1/span/a/text()").get()
        duration = response.xpath("normalize-space((//time)[1]/text())").get()
        rating = response.xpath("//div[@class='ratingValue']/strong/span/text()").get()
        release_date = response.xpath("normalize-space((//div[@id='titleDetails']/div/h4[contains(text(),'Release Date')]/parent::div/text())[2])").get()
        country = response.xpath("(//div[@id='titleDetails']/div/h4[contains(text(),'Country:')]/following-sibling::a/text())").get()
        storyline = response.xpath("normalize-space(//div[@id='titleStoryLine']/div/p/span/text())").get()
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
            'Cast' : response.xpath("normalize-space(//div[@id='titleCast']/table//tr[contains(@class,'odd') or contains(@class,'even')]/td[2]/a/text())").getall(),
            'Award': response.xpath("normalize-space(//span[@class='awards-blurb']/b/text())").getall()
        }

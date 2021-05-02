# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/search/title/?genres=drama&groups=top_250&sort=user_rating,desc']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=("//h3[@class='lister-item-header']/a")), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths=("(//a[@class='lister-page-next next-page'])[2]")))
    )

    def parse_item(self, response):
        yield{
            'Title' : response.xpath("normalize-space(//div[@class='title_wrapper']/h1/text())").get(),
            'Year' : response.xpath("//div[@class='title_wrapper']/h1/span/a/text()").get(),
            'Duration' : response.xpath("normalize-space((//time)[1]/text())").get(),
            'Gendres': response.xpath("(//div[@class='see-more inline canwrap'])[2]/a/text()").get(),
            'Rating': response.xpath("//div[@class='ratingValue']/strong/span/text()").get(),
            'Movie_url' : response.url,
            'Released_Date' : response.xpath("(//div[@id='titleDetails']/div[4]/text())[2]").get(),
            'Language' : response.xpath("(//div[@id='titleDetails']/div[3]/a/text())").get(),
            'Storyline' : response.xpath("//div[@id='titleStoryLine']/div/p/span/text()").get(),
            'Director' : response.xpath("(//div[@class='credit_summary_item'])[1]/a/text()").get(),
            'Writer' : response.xpath("(//div[@class='credit_summary_item'])[2]/a/text()").get(),
            'Cast' : response.xpath("//div[@id='titleCast']/table/tbody/tr[contains(@class,'odd') or contains(@class,'even')]/td[2]/a/text()").get(),
            'Award': response.xpath("normalize-space(//span[@class='awards-blurb']/b/text())").get()
        }
import scrapy
from news.items import NewsItem 
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader

class AllnewsSpider(scrapy.Spider):
    name = 'reuters'
    allowed_domains = ['reuters.com/']

    start_urls = ["https://www.reuters.com/"]

    def parse(self, response):
        for article in [response.xpath('//*[@id="main-content"]/div[1]/div/div[1]/div/div[2]/a')
                        ,response.xpath('//*[@id="main-content"]/div[1]/div/div[1]/div/div[1]/div[2]/a')]:
            for article2 in article:
                link = article2.xpath('.//@href').get()
                yield response.follow(link, callback=self.parse_info, dont_filter=True)



    def parse_info(self, response):
        FrontPageArticles = NewsItem()
        FrontPageArticles["link"] = response.url
        FrontPageArticles["title"] = response.xpath('//*[@id="fusion-app"]/div/div[2]/div/div[1]/article/div/header/div/div[1]/h1/text()').get()
        FrontPageArticles["tag"] =  response.xpath('//*[@id="fusion-app"]/div/div[2]/div/div[1]/article/div/header/div/div[1]/h4/span/a/text()').get()
        FrontPageArticles["date"] = response.xpath('//*[@id="fusion-app"]/div/div[2]/div/div[1]/article/div/header/div/time/span[1]/text()').get()
        FrontPageArticles["last_updated"] = response.xpath('//*[@id="fusion-app"]/div/div[2]/div/div[1]/article/div/header/div/time/span[3]/text()').get()
        yield FrontPageArticles




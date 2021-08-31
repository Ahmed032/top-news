import scrapy
from news.items import NewsItem 


class CnnSpider(scrapy.Spider):
    name = 'cnn'
    allowed_domains = ['edition.cnn.com']
    start_urls = ["https://edition.cnn.com/data/ocs/container/coverageContainer_94666ABA-6F11-0405-F645-CF22729BC16F:list-hierarchical-horizontal-simple/views/containers/common/container-manager.html"]

    def parse(self, response):
        for i in response.xpath('//*[@id="coverageContainer_94666ABA-6F11-0405-F645-CF22729BC16F"]/div/ul/li')[1:-1]:
            link = i.xpath('.//article/div/div/h3/a/@href').get()
            yield response.follow(link, callback=self.parse_info, dont_filter=True)

    def parse_info(self, response):
        FrontPageArticles = NewsItem()
        FrontPageArticles["title"] = response.css('h1.pg-headline::text').get()
        FrontPageArticles["last_updated"] = response.css("p.update-time::text").re(r'\d+\sGMT')[0]
        FrontPageArticles["date"] = response.css("p.update-time::text").re(r'.\w+\s\d+\,\s\d+')[0].strip()
        FrontPageArticles["link"] = response.url
        FrontPageArticles["tag"] = response.css('meta[name="section"]::attr("content")').get()
        yield FrontPageArticles




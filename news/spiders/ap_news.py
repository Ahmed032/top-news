import scrapy
from news.items import NewsItem 


class ApNewsSpider(scrapy.Spider):
    name = 'ap-news'
    allowed_domains = ['apnews.com']
    start_urls = ['https://apnews.com/hub/ap-top-news/']

    def parse(self, response):
        for i in response.xpath('/html/body/div[1]/div/main/div[3]/div/article/div/div')[1:]:
            link = i.xpath('./a/@href').get()
            yield response.follow(link, callback=self.parse_info, dont_filter=True)

    def parse_info(self, response):
        FrontPageArticles = NewsItem()
        FrontPageArticles["title"] = response.xpath('//*[@id="root"]/div/main/div[3]/div/div[4]/div[1]/h1/text()').get()
        FrontPageArticles["date"] = response.xpath('//*[@id="root"]/div/main/div[3]/div/div[4]/div[2]/span[2]/@title').re(r'\d{4}-\d{2}-\d{2}')[0]
        FrontPageArticles["link"] = response.url
        FrontPageArticles["tag"] = response.css('meta[property="article:tag"]::attr("content")')[0].get()
        FrontPageArticles["last_updated"] = None
        FrontPageArticles["source"] = "AP NEWS"
        yield FrontPageArticles

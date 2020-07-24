import scrapy
from scrapy_splash import SplashRequest


class TravelAgainSpider(scrapy.Spider):
    name = 'travel'
    allowed_domains = ['iwilltravelagain.com']
    start_urls = [
        'https://iwilltravelagain.com/'
    ]


    def __init__(self):
        self.declare_xpath()

    def declare_xpath(self):
        self.getAllRegions = '//*[@id="menu-item-regions-2"]/ul/li/a[@class="sub-menu-item-link"]/@href'
        self.getLocation = '//*[@id="activity-grid-1"]/div[2]/div[3]/div[1]/div/article/div/div[2]/div[2]/a/@href' #JS
        self.getName = '//*[@id="content"]/section[1]/div/div/div[1]/div/h1/text()'
        self.getCategory = '//*[@id="content"]/section[2]/div/div[2]/div[1]/div/ul/li[1]/div[2]/span[2]/text()'
        self.getLocationPlace = '//*[@id="content"]/section[2]/div/div[2]/div[1]/div/ul/li[2]/div[2]/span[2]/text()'
        self.getLocationState = '//*[@id="content"]/section[2]/div/div[2]/div[1]/div/ul/li[2]/div[2]/span[3]/text()'
        self.getWebsite = '//*[@id="content"]/section[2]/div/div[1]/div/aside/div[2]/div[2]/a/@href' #JS

    def parse(self, response):
        """ The function makes request to each region url"""
        for href in response.xpath(self.getAllRegions):
            url = response.urljoin(href.extract())
            yield SplashRequest(url=url, callback=self.parse_region)

    def parse_region(self, response):
        """ The function makes request to each location on the region level"""
        for href in response.xpath(self.getLocation):
            url = response.urljoin(href.extract())
            yield SplashRequest(url=url, callback=self.parse_location)

    def parse_location(self, response):
        """ The function extracts required data from each location page"""
        item = TravelagainItem()

        name = response.xpath(self.getName).extract()[0]
        category = response.xpath(self.getCategory).extract()[0]
        location_place = response.xpath(self.getLocationPlace).extract()[0]
        location_state = response.xpath(self.getLocationState).extract()[0]
        website = response.xpath(self.getWebsite).extract()

        item['name'] = name
        item['category'] = category
        item['location'] = location_place + ', ' + location_state
        item['website'] = website

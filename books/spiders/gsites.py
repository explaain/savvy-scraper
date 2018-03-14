# -*- coding: utf-8 -*-
import scrapy



class GoogleSitesSpider(scrapy.Spider):
  name = 'gsites'

  def __init__(self, site='', page='', result_queue=None, *args, **kwargs):
        super(GoogleSitesSpider, self).__init__(*args, **kwargs)
        loginUrl = 'https://facebook.com'
        # loginUrl = 'https://accounts.google.com/signin/v2/identifier'
        # site = 'https://sites.google.com/explaain.com/ourfirstwiki/'
        # page = 'home'
        # self.start_urls = [site + page]
        self.start_urls = [loginUrl]

  def parse(self, response):
    print('123123123')
    print('123123123')
    print('123123123')
    print('123123123')
    for mainBit in response.css('body'):
      yield {'main': mainBit.extract()}
    for mainBit in response.css('div[role=main]'):
      yield {'main': mainBit.extract()}




# class GSitesSpider(scrapy.Spider):
#     name = "gsites"
#     allowed_domains = ["gsites.toscrape.com"]
#     start_urls = [
#         'http://gsites.toscrape.com/',
#     ]
#
#     def parse(self, response):
#         for book_url in response.css("article.product_pod > h3 > a ::attr(href)").extract():
#             yield scrapy.Request(response.urljoin(book_url), callback=self.parse_book_page)
#         next_page = response.css("li.next > a ::attr(href)").extract_first()
#         if next_page:
#             yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
#
#     def parse_book_page(self, response):
#         item = {}
#         product = response.css("div.product_main")
#         item["title"] = product.css("h1 ::text").extract_first()
#         item['category'] = response.xpath(
#             "//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()"
#         ).extract_first()
#         item['description'] = response.xpath(
#             "//div[@id='product_description']/following-sibling::p/text()"
#         ).extract_first()
#         item['price'] = response.css('p.price_color ::text').extract_first()
#         yield item

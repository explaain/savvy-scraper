# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import scrapy, requests


class GoogleSitesSpider(scrapy.Spider):
  name = 'gsites'
  start_urls = [
    # 'https://sites.google.com/explaain.com/ourfirstwiki/home',
    # 'https://sites.google.com/explaain.com/ourfirstwiki/home',
  ]

  # def __init__(self, category=None, *args, **kwargs):
  #   super(GoogleSitesSpider, self).__init__(*args, **kwargs)
  #   self.start_urls = ['http://www.example.com/categories/%s' % category]
  #   # ...
  # allowed_domains = ["example.com"]
  # start_urls = (
  #   'http://www.example.com/',
  # )

  # def parse(self, response):
  #   # use lxml to get decent HTML parsing speed
  #   soup = BeautifulSoup(response.text, 'lxml')
  #   yield {
  #     "url": response.url,
  #     "title": soup.h1.string
  #   }


# class GoogleSitesSpider(scrapy.Spider):
#   name = 'gsites'
#
  def __init__(self, url_login=None, url_auth='', login='', pwd='', *args, **kwargs):
    super(GoogleSitesSpider, self).__init__(*args, **kwargs)
    print('\n\nSTARTING:\n')
    print(url_login, url_auth, login, pwd)
    # self.start_urls = start_urls
    if url_login:
      print('url_login', url_login)
      self.ses = requests.session()
      login_html = self.ses.get(url_login)
      soup_login = BeautifulSoup(login_html.content).find('form').find_all('input')
      my_dict = {}
      for u in soup_login:
        if u.has_attr('value'):
          my_dict[u['name']] = u['value']
      # override the inputs without login and pwd:
      my_dict['Email'] = login
      my_dict['Passwd'] = pwd
      self.ses.post(url_auth, data=my_dict)
      print(1111)
      scrapy.Request('https://sites.google.com/explaain.com/ourfirstwiki/home',
                                callback=self.parse_page1)
      print(2222)
    else:
      print(3333)
      scrapy.Request('https://sites.google.com/explaain.com/ourfirstwiki/home',
                                callback=self.parse_page1)
      # for inputField in response.css('html'):
      #   print('yielding')
      #   yield {'main': inputField.extract()}
#
#
  def get(self, URL):
    print('\n\n\nHELLO\n\n\n')
    yield self.ses.get(URL).text

  def parse(self, response):
    # url_login = 'https://accounts.google.com/ServiceLogin'
    # url_auth = 'https://accounts.google.com/ServiceLoginAuth'
    #
    # self.ses = requests.session()
    # login_html = self.ses.get(url_login)
    # soup_login = BeautifulSoup(login_html.content).find('form').find_all('input')
    # my_dict = {}
    # for u in soup_login:
    #   if u.has_attr('value'):
    #     my_dict[u['name']] = u['value']
    # # override the inputs without login and pwd:
    # my_dict['Email'] = 'jeremy@explaain.com'
    # my_dict['Passwd'] = 'ainola4$ENGE'
    # self.ses.post(url_auth, data=my_dict)
    #

    # check login succeed before going on
    print('after_login')

    return scrapy.Request('https://sites.google.com/explaain.com/ourfirstwiki/home',
                              callback=self.parse_page)

  def parse_page(self, response):
    print('parse_page')
    for inputField in response.css('html'):
      print('yielding')
      yield {'main': inputField.extract()}

  def get123(self, URL):
    print('get123')
    return scrapy.Request('https://sites.google.com/explaain.com/ourfirstwiki/home',
                              callback=self.parse_page1)

  def parse_page1(self, response):
    print('parse_page1')
    for inputField in response.css('html'):
      print('yielding')
      yield {'main': inputField.extract()}


  # def __init__(self, site='', page='', result_queue=None, *args, **kwargs):
  #       super(GoogleSitesSpider, self).__init__(*args, **kwargs)
  #       # loginUrl = 'https://accounts.google.com/signin/v2/identifier'
  #       site = 'https://sites.google.com/explaain.com/ourfirstwiki/'
  #       page = 'home'
  #       self.start_urls = [site + page]
  #       # self.start_urls = [loginUrl]
  #
  # def parse(self, response):
  #   print('123123123')
  #   print('123123123')
  #   print('123123123')
  #   print('123123123')
  #   return scrapy.FormRequest.from_response(
  #     response,
  #     formdata={'email': 'jeremy@explaain.com', 'password': 'ainola4$ENGE'},
  #     callback=self.after_login
  #   )
  # def after_login(self, response):
  #   # check login succeed before going on
  #   print('after_login')
  #
  #   for inputField in response.css('html'):
  #     yield {'main': inputField.extract()}
  #   # for inputField in response.css('input[type="email"]'):
  #   #   yield {'main': inputField.extract()}
  #   # for mainBit in response.css('div[role=main]'):
  #   #   yield {'main': mainBit.extract()}
  #
  #   # if 'authentication failed' in response.body:
  #   #   self.logger.error('Login failed')
  #   #   return
  #
  #   # continue scraping with authenticated session...



url_login = 'https://accounts.google.com/ServiceLogin'
url_auth = 'https://accounts.google.com/ServiceLoginAuth'

session = GoogleSitesSpider(url_login, url_auth, 'jeremy@explaain.com', 'ainola4$ENGE')
print(session.get('https://sites.google.com/explaain.com/ourfirstwiki/home'))
# print(session.get123('https://sites.google.com/explaain.com/ourfirstwiki/home'))
# print(session.get('http://plus.google.com'))

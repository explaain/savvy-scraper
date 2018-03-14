# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import scrapy, requests, html2text
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

class SessionGoogle:
  def __init__(self, url_login, url_auth, login, pwd):
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
    resres = self.ses.post(url_auth, data=my_dict)
    print('resres')
    print(resres)
    print(type(resres))
    print(dir(resres))
    print(html2text.html2text(resres.content.decode('utf-8')))

  def get(self, URL):
    return self.ses.get(URL).text


class GoogleSitesSpider(scrapy.Spider):
  name = 'gsites'
  # allowed_domains = ['sites.google.com/explaain.com']
  start_urls = [
    'https://sites.google.com/explaain.com/ourfirstwiki/home',
  ]

  rules = (Rule(LinkExtractor(), callback='parse_item'))

  def __init__(self, url_login=None, url_auth='', login='', pwd='', *args, **kwargs):
    super(GoogleSitesSpider, self).__init__(*args, **kwargs)

    url_login = 'https://accounts.google.com/ServiceLogin'
    url_auth = 'https://accounts.google.com/ServiceLoginAuth'

    self.mySession = SessionGoogle(url_login, url_auth, 'testsavvy3@gmail.com', 'nakedtest9')

  def parse(self, response):
    print('parse')
    homepage = self.mySession.get('https://sites.google.com/explaain.com/ourfirstwiki/home')
    yield {'main': homepage}
    for link in homepage.css('a'):
      print('link')
      print(link)
      # yield {'main': inputField.extract()}

  def parse_item(self, response):
    print('parse_item')
    yield {'main1': self.mySession.get('https://sites.google.com/explaain.com/ourfirstwiki/home')}
    # for inputField in response.css('html'):
    #   print('yielding')
    #   yield {'main': inputField.extract()}

# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import scrapy, requests

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
    self.ses.post(url_auth, data=my_dict)

  def get(self, URL):
    return self.ses.get(URL).text


class GoogleSitesSpider(scrapy.Spider):
  name = 'gsites'
  start_urls = [
    'https://sites.google.com/explaain.com/ourfirstwiki/home',
  ]

  def __init__(self, url_login=None, url_auth='', login='', pwd='', *args, **kwargs):
    super(GoogleSitesSpider, self).__init__(*args, **kwargs)

    url_login = 'https://accounts.google.com/ServiceLogin'
    url_auth = 'https://accounts.google.com/ServiceLoginAuth'

    self.mySession = SessionGoogle(url_login, url_auth, 'jeremy@explaain.com', 'ainola4$ENGE')

  def parse(self, response):
    print('parse')
    yield {'main': self.mySession.get('https://sites.google.com/explaain.com/ourfirstwiki/home')}
    # for inputField in response.css('html'):
    #   print('yielding')
    #   yield {'main': inputField.extract()}

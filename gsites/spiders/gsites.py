# -*- coding: utf-8 -*-
import pprint, time, calendar, scrapy, requests, html2text
from bs4 import BeautifulSoup
from scrapy.spiders import Rule
# from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from algoliasearch import algoliasearch

pp = pprint.PrettyPrinter(indent=4)

googleSitesUrl = 'https://sites.google.com/'
urlLogin = 'https://accounts.google.com/ServiceLogin'
urlAuth = 'https://accounts.google.com/ServiceLoginAuth'

organisationID = 'explaain'
specificSiteID = 'explaain.com'
myEmail = 'testsavvy3@gmail.com'
myPassword = 'nakedtest9'
homepageExtension = '/ourfirstwiki/home'

specificGoogleSitesUrl = googleSitesUrl + specificSiteID



client = algoliasearch.Client('D3AE3TSULH', '1b36934cc0d93e04ef8f0d5f36ad7607') # This API key allows everything
algoliaScrapedIndex = client.init_index(organisationID + '__Scraped')

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
    print(html2text.html2text(resres.content.decode('utf-8'))[:1000])

  def get(self, URL):
    return self.ses.get(URL).text


class GoogleSitesSpider(scrapy.Spider):
  name = 'gsites'
  start_urls = [
    specificGoogleSitesUrl + homepageExtension,
  ]

  def __init__(self, *args, **kwargs):
    super(GoogleSitesSpider, self).__init__(*args, **kwargs)

    self.mySession = SessionGoogle(urlLogin, urlAuth, myEmail, myPassword)

  def parse(self, response):
    print('parse')
    home_url = specificGoogleSitesUrl + homepageExtension
    homepage = self.mySession.get(home_url)
    main = store_page(home_url, homepage)
    print(html2text.html2text(main))
    # yield {'main': main}
    urls = [link.css('::attr(href)').extract_first() for link in Selector(text=homepage).css('a')]
    internalUrls = [url for url in urls if url and (url[0] == '/' or specificGoogleSitesUrl in url)]
    uniqueInternalUrls = list(set(internalUrls))
    fullUrls = [googleSitesUrl[:-1] + url if url[0] == '/' else url for url in uniqueInternalUrls]
    print('Full Internal Urls:', fullUrls)
    for url in fullUrls:
      page = self.mySession.get(url)
      mainSection = store_page(url, page)
      print(html2text.html2text(mainSection))
      # yield {'main': mainSection}

def store_page(url, page):
  sel = Selector(text=page)
  title = sel.css('title ::text').extract_first()
  main_html = sel.css('div[role=main]').extract_first()
  page_dict = {
    'objectID': url,
    'url': url,
    'fileType': 'html',
    'title': title,
    'source': specificGoogleSitesUrl,
    'service': 'gsites',
    'content': main_html,
    'organisationID': organisationID,
    'modified': calendar.timegm(time.gmtime()), # Not ideal!!
    'created': calendar.timegm(time.gmtime()), # Definitely not right!!!!
  }
  pp.pprint(page_dict)
  algoliaScrapedIndex.save_object(page_dict)
  return main_html

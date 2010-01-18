#!/usr/bin/env python

import cgi
import datetime
import wsgiref.handlers
import htmllib
import sgmllib
import logging
import urllib
import os
import time
import re

from google.appengine.ext import db
from google.appengine.ext import search
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.api import urlfetch
from google.appengine.api import memcache 
from google.appengine.ext.webapp import template

class Utils():
    stopwords = [
    'a',
    'about',
    'above',
    'across',
    'after',
    'again',
    'against',
    'all',
    'almost',
    'alone',
    'along',
    'already',
    'also',
    'although',
    'always',
    'among',
    'an',
    'and',
    'another',
    'any',
    'anybody',
    'anyone',
    'anything',
    'anywhere',
    'are',
    'area',
    'areas',
    'around',
    'as',
    'ask',
    'asked',
    'asking',
    'asks',
    'at',
    'away',
    'b',
    'back',
    'backed',
    'backing',
    'backs',
    'be',
    'became',
    'because',
    'become',
    'becomes',
    'been',
    'before',
    'began',
    'behind',
    'being',
    'beings',
    'best',
    'better',
    'between',
    'big',
    'both',
    'but',
    'by',
    'c',
    'came',
    'can',
    'cannot',
    'case',
    'cases',
    'certain',
    'certainly',
    'clear',
    'clearly',
    'come',
    'could',
    'd',
    'did',
    'differ',
    'different',
    'differently',
    'do',
    'does',
    'done',
    'down',
    'down',
    'downed',
    'downing',
    'downs',
    'during',
    'e',
    'each',
    'early',
    'either',
    'end',
    'ended',
    'ending',
    'ends',
    'enough',
    'even',
    'evenly',
    'ever',
    'every',
    'everybody',
    'everyone',
    'everything',
    'everywhere',
    'f',
    'face',
    'faces',
    'fact',
    'facts',
    'far',
    'felt',
    'few',
    'find',
    'finds',
    'first',
    'for',
    'four',
    'from',
    'full',
    'fully',
    'further',
    'furthered',
    'furthering',
    'furthers',
    'g',
    'gave',
    'general',
    'generally',
    'get',
    'gets',
    'give',
    'given',
    'gives',
    'go',
    'going',
    'good',
    'goods',
    'got',
    'great',
    'greater',
    'greatest',
    'group',
    'grouped',
    'grouping',
    'groups',
    'h',
    'had',
    'has',
    'have',
    'having',
    'he',
    'her',
    'here',
    'herself',
    'high',
    'high',
    'high',
    'higher',
    'highest',
    'him',
    'himself',
    'his',
    'how',
    'however',
    'i',
    'if',
    'important',
    'in',
    'interest',
    'interested',
    'interesting',
    'interests',
    'into',
    'is',
    'it',
    'its',
    'itself',
    'j',
    'just',
    'k',
    'keep',
    'keeps',
    'kind',
    'knew',
    'know',
    'known',
    'knows',
    'l',
    'large',
    'largely',
    'last',
    'later',
    'latest',
    'least',
    'less',
    'let',
    'lets',
    'like',
    'likely',
    'long',
    'longer',
    'longest',
    'm',
    'made',
    'make',
    'making',
    'man',
    'many',
    'may',
    'me',
    'member',
    'members',
    'men',
    'might',
    'more',
    'most',
    'mostly',
    'mr',
    'mrs',
    'much',
    'must',
    'my',
    'myself',
    'n',
    'necessary',
    'need',
    'needed',
    'needing',
    'needs',
    'never',
    'new',
    'new',
    'newer',
    'newest',
    'next',
    'no',
    'nobody',
    'non',
    'noone',
    'not',
    'nothing',
    'now',
    'nowhere',
    'number',
    'numbers',
    'o',
    'of',
    'off',
    'often',
    'old',
    'older',
    'oldest',
    'on',
    'once',
    'one',
    'only',
    'open',
    'opened',
    'opening',
    'opens',
    'or',
    'order',
    'ordered',
    'ordering',
    'orders',
    'other',
    'others',
    'our',
    'out',
    'over',
    'p',
    'part',
    'parted',
    'parting',
    'parts',
    'per',
    'perhaps',
    'place',
    'places',
    'point',
    'pointed',
    'pointing',
    'points',
    'possible',
    'present',
    'presented',
    'presenting',
    'presents',
    'problem',
    'problems',
    'put',
    'puts',
    'q',
    'quite',
    'r',
    'rather',
    'really',
    'right',
    'right',
    'room',
    'rooms',
    's',
    'said',
    'same',
    'saw',
    'say',
    'says',
    'second',
    'seconds',
    'see',
    'seem',
    'seemed',
    'seeming',
    'seems',
    'sees',
    'several',
    'shall',
    'she',
    'should',
    'show',
    'showed',
    'showing',
    'shows',
    'side',
    'sides',
    'since',
    'small',
    'smaller',
    'smallest',
    'so',
    'some',
    'somebody',
    'someone',
    'something',
    'somewhere',
    'state',
    'states',
    'still',
    'still',
    'such',
    'sure',
    't',
    'take',
    'taken',
    'than',
    'that',
    'the',
    'their',
    'them',
    'then',
    'there',
    'therefore',
    'these',
    'they',
    'thing',
    'things',
    'think',
    'thinks',
    'this',
    'those',
    'though',
    'thought',
    'thoughts',
    'three',
    'through',
    'thus',
    'to',
    'today',
    'together',
    'too',
    'took',
    'toward',
    'turn',
    'turned',
    'turning',
    'turns',
    'two',
    'u',
    'under',
    'until',
    'up',
    'upon',
    'us',
    'use',
    'used',
    'uses',
    'v',
    'very',
    'w',
    'want',
    'wanted',
    'wanting',
    'wants',
    'was',
    'way',
    'ways',
    'we',
    'well',
    'wells',
    'went',
    'were',
    'what',
    'when',
    'where',
    'whether',
    'which',
    'while',
    'who',
    'whole',
    'whose',
    'why',
    'will',
    'with',
    'within',
    'without',
    'work',
    'worked',
    'working',
    'works',
    'would',
    'x',
    'y',
    'year',
    'years',
    'yet',
    'you',
    'young',
    'younger',
    'youngest',
    'your',
    'yours',
    'z',
    # added custom values 
    'http',
    'www',
    'https',
    '://',
    'com'
    ]

class Constants:
  BOOKMARK_SEARCH_MEMCACHE_KEY = 'BOOKMARK_SEARCH_MEMCACHE_KEY'
  MAX_LIFE = 86400 * 31 
  MIN_COUNTER = 1 
  KEYWORD_LIMIT = 10 

class MyParser(sgmllib.SGMLParser):

    def parse(self, s):
        self.feed(s)
        self.close()

    def __init__(self, verbose=0):
        sgmllib.SGMLParser.__init__(self, verbose)
        self.hyperlinks = []
        self.descriptions = []
        self.inside_a_element = 0
        self.starting_description = 0

    def start_a(self, attributes):
        glink = False
        for name, value in attributes:
            if name == "class":
              if value == "l":
                glink = True
        if glink == False:
          return
        for name, value in attributes:
            if name == "href":
                self.hyperlinks.append(value)
                self.inside_a_element = 1
                self.starting_description = 1

    def end_a(self):
        self.inside_a_element = 0

    def get_hyperlinks(self):
        return self.hyperlinks

    def get_descriptions(self):
        return self.descriptions

    def handle_data(self, data):
        if self.inside_a_element:
            if self.starting_description:
                self.descriptions.append(data)
                self.starting_description = 0
            else:
                self.descriptions[-1] += data

class Bookmark(search.SearchableModel):
  user = db.UserProperty()
  text = db.TextProperty()
  url = db.StringProperty(multiline=False)
  date = db.DateTimeProperty(auto_now_add=True)
  counter = db.IntegerProperty()

class Home(webapp.RequestHandler):
  def get(self):
    myuser = users.get_current_user() 
    if myuser is None:
      url = users.create_login_url("http://nomorebookmarks.appspot.com")
      self.redirect(url)
    bookmarks = Bookmark.all().order('-counter').fetch(limit=20)
    template_values = {
      'query': '',
      'list_title': 'Favourites',
      'bookmarks': bookmarks,
      'anchors': [],
      'nickname': myuser
      }
    path = os.path.join(os.path.dirname(__file__), 'home.html')
    self.response.out.write(template.render(path, template_values))

class Bookmarks(webapp.RequestHandler):
  def get(self):
    myuser = users.get_current_user() 
    if myuser is None:
      url = users.create_login_url("http://nomorebookmarks.appspot.com")
      self.redirect(url)
    bookmarks = Bookmark.all().order('-counter')
    template_values = {
      'query': '',
      'list_title': 'All Bookmarks',
      'bookmarks': bookmarks,
      'anchors': [],
      'nickname': myuser
      }
    path = os.path.join(os.path.dirname(__file__), 'home.html')
    self.response.out.write(template.render(path, template_values))

class Clean(webapp.RequestHandler):
  def get(self):
    myuser = users.get_current_user() 
    if myuser is None:
      url = users.create_login_url("http://nomorebookmarks.appspot.com")
      self.redirect(url)
    bookmarks = Bookmark.all()
    for bookmark in bookmarks:
      bookmark.delete()
    template_values = {
      'query': '',
      'list_title': 'All Bookmarks Deleted',
      'bookmarks': [],
      'anchors': [],
      'nickname': myuser
      }
    path = os.path.join(os.path.dirname(__file__), 'home.html')
    self.response.out.write(template.render(path, template_values))

class Search(webapp.RequestHandler):
  def strip_query(self, query):
    #arr = query.split(" ")
    arr = re.split('\W+', query)
    newarr = []
    c = 0
    for a in arr:
      found = False
      for b in Utils.stopwords:
        if(b == a):
          found = True
          logging.info("search word is stop word: " + a)
          break
      if(not found):
        newarr.append(a)
        c += 1
        if(c == Constants.KEYWORD_LIMIT):
          logging.info("word limit reached: " + a)
          break
        logging.info("search word is OK: " + a)
    newstr = ""
    for c in newarr:
      newstr += c
      newstr += " "
    logging.info("stripped query: " + newstr)
    return newstr

  def query(self, query):
    myuser = users.get_current_user() 
    if myuser is None:
      url = users.create_login_url("http://nomorebookmarks.appspot.com")
      self.redirect(url)
    url = "http://www.google.it/search?site=&hl=it&btnG=Cerca&lr=&q=" + urllib.quote(query)
    arr = [] 
    result = urlfetch.fetch(url)
    if result.status_code == 200:
      myparser = MyParser()
      myparser.parse(result.content)
      hrefs = myparser.get_hyperlinks()
      labels = myparser.get_descriptions()
      l = len(hrefs)
      ll = len(labels)
      if ll < l:
        l = ll
      bookmarks = self.bookmark_query(query, myuser)
      for x in range(l):
        found = False
        for bookmark in bookmarks:
          if(bookmark.url == hrefs[x]):
            found = True
            break
        if(found):
          continue
        arr.append({"url":hrefs[x], "text":labels[x]})
    return arr

  def numeric_sort_reverse(self, x, y):
    if x.counter > y.counter:
      return -1 
    elif x.counter == y.counter:
      return 0
    else: # x<y
      return 1
  def numeric_sort(self, x, y):
    if x.counter > y.counter:
      return 1
    elif x.counter == y.counter:
      return 0
    else: # x<y
      return -1

  def bookmark_query(self, query, user):
    if len(query) > 2:
     query = self.strip_query(query)
     bms2 = memcache.get(Constants.BOOKMARK_SEARCH_MEMCACHE_KEY + query)
     if(bms2 is None):
      logging.info("BOOKMARK_SEARCH_MEMCACHE_KEY from datastore, query " + query)
      #bms = Bookmark.all().search(query).order('-counter').fetch()
      bms = Bookmark.all().search(query).fetch(limit=1000)
      bms2 = filter( lambda x: x.user == user,  bms )
      bms2.sort(cmp=self.numeric_sort_reverse)
      memcache.add(Constants.BOOKMARK_SEARCH_MEMCACHE_KEY + query, bms2, 3)
     else:
      logging.info("BOOKMARK_SEARCH_MEMCACHE_KEY from memcache, query " + query)
     return bms2 
    else:
     return []
    
  def get(self):
    myuser = users.get_current_user() 
    if myuser is None:
      url = users.create_login_url("http://nomorebookmarks.appspot.com")
      self.redirect(url)
    query = self.request.get('query')
    bookmarks = self.bookmark_query(query, myuser)
    anchors = self.query(query)
    template_values = {
      'query': query,
      'list_title': 'Search results for ' + query,
      'bookmarks': bookmarks,
      'anchors': anchors,
      'nickname': myuser
      }
    self.response.headers['Content-Type'] = 'text/html; charset=iso-8859-1'
    path = os.path.join(os.path.dirname(__file__), 'home.html')
    self.response.out.write(template.render(path, template_values))

class Open(webapp.RequestHandler):
  def get(self):
    myuser = users.get_current_user() 
    if myuser is None:
      url = users.create_login_url("http://nomorebookmarks.appspot.com")
      self.redirect(url)
    val = self.request.get('text')
    url = self.request.get('url')
    bookmarks = Bookmark.all() 
    found = False
    for bookmark in bookmarks:
      if(bookmark.url == url):
        found = True
        bookmark.counter += 1
        bookmark.save()
      elif((bookmark.counter <= Constants.MIN_COUNTER) and ((datetime.datetime.now() - bookmark.date) > datetime.timedelta(seconds=Constants.MAX_LIFE))):
        bookmark.delete()
    if(not found):
      bookmark = Bookmark(text=val)
      bookmark.user = myuser 
      bookmark.url = url
      bookmark.counter = 1
      bookmark.save()
    self.redirect(url)

application = webapp.WSGIApplication([
  ('/', Home),
  ('/search', Search),
  ('/bookmarks', Bookmarks),
  ('/clean', Clean),
  ('/open', Open)
], debug=True)

def main():
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()


# -*- coding: UTF-8 -*-
#######################################################################
 # ----------------------------------------------------------------------------
 # "THE BEER-WARE LICENSE" (Revision 42):
 # @tantrumdev wrote this file.  As long as you retain this notice you
 # can do whatever you want with this stuff. If we meet some day, and you think
 # this stuff is worth it, you can buy me a beer in return. - Muad'Dib
 # ----------------------------------------------------------------------------
####################################################################### 

# Addon Name: Eggman
# Addon id: Eggmans
# Addon Provider: Eggman

import re
import urllib
import urlparse
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import proxy


class source:
	def __init__(self):
		self.priority = 1
		self.language = ['en']
		self.domains = ['hackimdb.com']
		self.base_link = 'https://hackimdb.com'
		self.search_link = '/title/&%s'

	def movie(self, imdb, title, localtitle, aliases, year):
		try:
			url = self.base_link + self.search_link % imdb
			return url
		except:
			return
			
	def sources(self, url, hostDict, hostprDict):
		try:
			sources = []
			r = client.request(url)
			try:
				match = re.compile('<iframe .+?src=".+?rapidvideo(.+?)"').findall(r)
				for url in match: 
					url = 'https://www.rapidvideo' + url
					
					r = client.request(url)
					match = re.compile('<source src="(.+?)" type="video/mp4" title="(.+?)"').findall(r)
					for url, quality in match:
					
						sources.append({
							'source': 'RapidVideo',
							'quality': quality,
							'language': 'en',
							'url': url,
							'direct': False,
							'debridonly': False
						})
			except:
				return
		except Exception:
			return
		return sources

	def resolve(self, url):
		return url
import urllib2
import urllib
import re
import thread
import os

from Parser import Parser

class WebSearch(object):
	'''
	get lists and pages from wikipedia
	'''
	def __init__(self):
		self.names_of_list = []
		self.pages = []
		self.wikiUrl = "https://en.wikipedia.org/wiki"
		pass

	# get all content-time pairs and return the whole list
	def __getLists(self):

		# get lists
		myUrl = self.wikiUrl + "/Lists_of_prepared_foods"
		print 'root page: ' + myUrl
		# wrap the headers
		user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
		headers = {'User-Agent' : user_agent}
		# get page
		try:
			myPage = urllib2.urlopen(urllib2.Request(myUrl, headers = headers)).read()
		except:
			print 'error at opening root page'

		'''
		'<a href="/wiki/List_of_Palestinian_dishes" title="List of Palestinian dishes">
		'''

		list = re.findall(r"a href=\"/wiki/(List_of_.*?)\" title=\"(.*?)\">", myPage, re.S)
		for x in list:
			self.names_of_list.append(x[0])
		print 'get', len(list), 'lists from root'

	def __getNamesFromLists(self, listName):
		#get foods from page of list
		myUrl = self.wikiUrl + "/" + listName
		print 'list page: ' + myUrl
		user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
		headers = {'User-Agent' : user_agent}
		# get page
		try:
			myPage = urllib2.urlopen(urllib2.Request(myUrl, headers = headers)).read()
		except:
			print 'error at page named', listName
		
		backup = r"<tr>\n<td><a href=\"/wiki/(.*?)\" title=\".*?\">.*?</a></td>.*?</tr>"
		one_list = re.findall(backup, myPage, re.S)
		names = []
		
		for item in one_list:
			names.append(item)

		print names
		return names;

	def __getPagesFromList(self, listName):
		'''
		will save pages in self.pages, thus giving each page a number
		'''
		names = self.__getNamesFromLists(listName)
		if not os.path.isdir(listName):
			os.mkdir(listName)

		for name in names:
			#get foods from page of list
			myUrl = self.wikiUrl + "/" + name
			print 'name page: ' + myUrl
			user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
			headers = {'User-Agent' : user_agent}
			# get page
			try:
				myPage = urllib2.urlopen(urllib2.Request(myUrl, headers = headers)).read()
			except:
				print 'error at page named', name
			
			self.pages.append(myPage);
			file = open(listName + '\\' + name + '.html', 'w')
			file.write(myPage);
			file.close()
	def __chooseLists(self):
		i = 0
		for listName in self.names_of_list:
			print i, listName
			i += 1
		chosen = raw_input().split(' ')
		return [int(x) for x in chosen]
			
	def run(self):
		self.__getLists()
		chosen = self.__chooseLists()
		for no in chosen:
			try:
				self.__getPagesFromList(self.names_of_list[no])
			except:
				print 'exception at %04d th list' % no
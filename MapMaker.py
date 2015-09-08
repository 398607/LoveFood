
import os
from Parser import Parser


class MapMaker(object):
	'''
	make a map of (words, anti-list)
	could be saved to (file? database?)
	run(self) returns that dict
	'''
	def __init__(self):
		self.map = {}
		self.pagePath = []
		
	def run(self):

		for parent, dirnames, filenames in os.walk(os.getcwd()):

			for dirname in dirnames:
				print 'parent is:' + parent + ' dirname is ' + dirname

			pageId = 0

			for filename in filenames:
				if 'List_of_' in parent:
					#print 'parent is:' + parent + ' filename is ' + filename
					fullPath = os.path.join(parent, filename)
					print 'full path: ' + fullPath
					self.pagePath.append(fullPath)
					try:
						self.parse(self.pagePath.__len__() - 1)
					except:
						print '-----' + fullPath + '-----error: failed to parse'

		bak = open('antiList.txt', 'w')
		for word in self.map:
			print word, self.map[word]
			bak.write(word + ':' + ' '.join([str(x) for x in self.map[word]]) + '\n')
		bak.close()

		page = open('pageId.txt', 'w')
		for id in range(0, len(self.pagePath)):
			page.write(str(id) + ' ' + self.pagePath[id] + '\n')
		page.close()

	def parse(self, pageNo):
		parser = Parser()
		file = open(self.pagePath[	pageNo], 'r')

		parser.feed(file.read())

		for word in parser.getWords():
			if word == '':
				continue
			if not word in self.map:
				self.map[word] = []
			if not pageNo in self.map[word]:
				self.map[word].append(pageNo)
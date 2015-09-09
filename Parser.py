
from HTMLParser import HTMLParser

class Parser(HTMLParser):
	'''
	get contents or plain words between <p> and </p>
	getWords(self) return a list of words.
	'''
	def __init__(self):
		HTMLParser.__init__(self)
		self.mode = False
		self.text = ""
	def getText(self):
		t = ''
		for line in self.text.split('.'):
			t += '<p>' + line + '.</p>'
		return t

	def getWords(self):
		dots = '.,?!-\%/:'
		splits = '()\'\"[]\n'
		plain = self.text
		for dot in dots:
			#print dot
			plain = plain.replace(dot, '')
		for spl in splits:
			#print spl
			plain = plain.replace(spl, ' ')
		words = plain.split(' ')
		return words

	def handle_starttag(self, tag, attrs):
		if tag == 'p':
			self.mode = True
	def handle_data(self, data):
		if self.mode:
			self.text += data
	def handle_endtag(self, tag):
		if tag == 'p':
			self.mode = False

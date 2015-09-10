from django.shortcuts import render_to_response, render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from Parser import Parser

class View(object):
	mapper = {}
	nameList = {}

	@classmethod
	def index(cls, request):
		return render_to_response("index.html")

	@classmethod
	def init(cls, request):
		if cls.mapper == {}:
			file = open("antiList.txt", "r")
			for line in file:
				word, listr = line.split(':')
				antiList = [int(x) for x in listr.split(' ')]
				cls.mapper[word] = antiList
			file.close()
			file = open("pageId.txt", "r")
			for line in file:
				id, name = line.split(' ')
				cls.nameList[int(id)] = name[0:-1]
			file.close()
		else:
			pass

	@classmethod
	@csrf_exempt
	def getList(cls, request):
		cls.init(request)
		if request.POST.has_key('str'):
			strList = request.POST['str'].split(' ')
		else:
			strList = ['']

		idList = range(0, len(cls.nameList))

		for s in strList:
			if s == '':
				continue
			if cls.mapper.has_key(s):
				idList = [x for x in idList if x in cls.mapper[s]]
			else:
				idList = []

		
		if len(idList) > 0:

			listing = []
			for id in idList:
				p = {}
				p['id'] = id
				p['add'] = cls.nameList[id].replace('\\', '/')
				p['name'] = cls.nameList[id].split('\\')[-1].split('.')[0]
				listing.append(p)

			return render_to_response('result.html', {'list' : listing, 'str' : ' '.join(strList)})
		else:
			listing = []
			return render_to_response('result.html', {'list' : listing, 'str' : ' '})

	
	@classmethod
	@csrf_exempt
	def show(cls, request):
		cls.init(request)
		if request.POST.has_key('id'):
			id = int(request.POST['id'])

			page = open(cls.nameList[id], 'r')
			name = cls.nameList[id].split('\\')[-1].split('.')[0]

			par = Parser()
			par.feed(page.read())
			text = par.getText()

			return render_to_response('show.html', {'name':name, 'text':text})
		else:
			return render_to_response('show.html', {'name':'empty doc', 'text':['']})
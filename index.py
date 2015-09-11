from django.shortcuts import render_to_response, render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from Parser import Parser

class View(object):
	mapper = {}
	nameList = {}

	@classmethod
	@csrf_exempt
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
			if len(s) == 0:
				continue
			elif cls.mapper.has_key(s):
				idList = [x for x in idList if x in cls.mapper[s]]
			else:
				idList = []
		
		if request.POST.has_key('curpage'):
			curpage = int(request.POST['curpage'])
		else:
			curpage = 0
		
		totalpage = len(idList) / 10
		if len(idList[totalpage * 10 : min(totalpage * 10 + 10, len(idList) - 1)]) == 0:
			totalpage -= 1


		if curpage < 0:
			curpage = 0
		elif curpage > totalpage:
			curpage = totalpage

		nowList = idList[curpage * 10 : min(curpage * 10 + 10, len(idList) - 1)]
		
		
		if len(nowList) > 0:

			listing = []
			for id in nowList:
				p = {}
				p['id'] = id
				p['add'] = cls.nameList[id].replace('\\', '/')
				p['name'] = cls.nameList[id].split('\\')[-1].split('.')[0]
				listing.append(p)

			return render_to_response('result.html', {'list' : listing, 'str' : ' '.join(strList), 'curpage': curpage, 'totalpage': totalpage})
		else:
			listing = []
			return render_to_response('result.html', {'list' : listing, 'str' : ' '.join(strList), 'curpage' : 0, 'totalpage' : 0})

	
	@classmethod
	@csrf_exempt
	def show(cls, request):
		cls.init(request)
		if request.POST.has_key('id'):
			id = int(request.POST['id'])
			curpage = int(request.POST['curpage'])

			page = open(cls.nameList[id], 'r')
			name = cls.nameList[id].split('\\')[-1].split('.')[0]
			str = request.POST['str']

			par = Parser()
			par.feed(page.read())
			text = par.getText()

			return render_to_response('show.html', {'name':name, 'text':text, 'str': str, 'curpage': curpage})
		else:
			return render_to_response('show.html', {'name':'empty doc', 'text':[''], 'str': '', 'curpage': 0})
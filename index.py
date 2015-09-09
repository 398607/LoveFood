from django.shortcuts import render_to_response, render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from Parser import Parser

searchPage = '''

<form method="post" action="/test/">
<input type="text" name="str">
<input type="submit" value="search">
</form>

'''

class View(object):
	mapper = {}
	nameList = {}

	@classmethod
	def index(cls, request):
		return HttpResponse(searchPage)

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
			return HttpResponse('no results')

	
	@classmethod
	@csrf_exempt
	def show(cls, request):
		if request.POST.has_key('id'):
			id = int(request.POST['id'])

			page = open(cls.nameList[id], 'r')
			name = cls.nameList[id].split('\\')[-1].split('.')[0]

			par = Parser()
			par.feed(page.read())

			return HttpResponse('<h1>' + name + '</h1>' + par.getText())
		else:
			return HttpResponse('page not exist')
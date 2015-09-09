from django.shortcuts import render_to_response, render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

searchPage = '''

<form method="post" action="/test/">
<input type="text" name="str">
<input type="submit" value="search">
</form>

'''

class View(object):
	mapper = {}

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
		else:
			pass

	@classmethod
	@csrf_exempt
	def getList(cls, request):
		cls.init(request)
		if request.POST.has_key('str'):
			s = request.POST['str']
		else:
			s = ''
		if cls.mapper.has_key(s):
			return HttpResponse(' '.join([str(x) for x in cls.mapper[s]]))
		else:
			return HttpResponse('empty')
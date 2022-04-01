from tv_series_fw.templator import render


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', style=request.get('style', None))


class About:
    def __call__(self, request):
        return '200 OK', render('about.html', style=request.get('style', None))


class PageNotExists:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class Contacts:
    def __call__(self, request):
        return '200 OK', render('contacts.html', style=request.get('style', None))


class Watch:
    def __call__(self, request):
        return '200 OK', render('watch.html', style=request.get('style', None), content=request.get('series', None))


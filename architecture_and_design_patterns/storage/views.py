from datetime import date

from tv_series_fw.templator import render
from patterns.generative_patterns import Interface, Logger
from patterns.structural_patterns import AppRoute, Debug

site = Interface()
site.categories.append(site.create_category('Драма'))
site.categories.append(site.create_category('Боевик'))
site.categories.append(site.create_category('Фантастика'))
site.categories.append(site.create_category('Комедия'))

site.free_users = ['Николай Николаев', 'Петр Петров', 'Иван Иванов']
site.subscribed_users = ['Александр Александров', 'Василий Васильев',
                         'Сергей Сергеев']

logger = Logger('main')

routes = dict()


@AppRoute(routes=routes, url='/')
class Index:
    @Debug(name='Index')
    def __call__(self, request):
        # return '200 OK', render('index.html', style=request.get('style', None))
        return '200 OK', render('index.html', objects_list=site.categories)


@AppRoute(routes=routes, url='/about/')
class About:
    @Debug(name='About')
    def __call__(self, request):
        # return '200 OK', render('about.html', style=request.get('style', None))
        return '200 OK', render('about.html')


class PageNotExists:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


@AppRoute(routes=routes, url='/series-schedule/')
class SeriesSchedule:
    """Расписание сериалов"""
    @Debug(name='SeriesSchedule')
    def __call__(self, request):
        return '200 OK', render('series-schedule.html',  data=date.today())


@AppRoute(routes=routes, url='/series-list/')
class SeriesList:
    @Debug(name='SeriesList')
    def __call__(self, request):
        logger.log("Список сериалов")
        try:
            category = site.find_category_by_id(int(request['request_params']
                                                    ['id']))
            return '200 OK', render('series-list.html',
                                    objects_list=category.serieses,
                                    name=category.name, id=category.id)
        except KeyError:
            return '200 OK', 'No series have been added yet'


@AppRoute(routes=routes, url='/create-series/')
class CreateSeries:
    """Создать сериал"""
    category_id = -1

    @Debug(name='CreateSeries')
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))
                series = site.create_series('record', name, category)
                site.serieses.append(series)

            return '200 OK', render('series-list.html',
                                    objects_list=category.serieses,
                                    name=category.name, id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create-series.html',
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


@AppRoute(routes=routes, url='/create-category/')
class CreateCategory:
    @Debug(name='CreateCategory')
    def __call__(self, request):

        if request['method'] == 'POST':

            print(request)

            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return '200 OK', render('index.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create-category.html',
                                    categories=categories)


@AppRoute(routes=routes, url='/category-list/')
class CategoryList:
    @Debug(name='CategoryList')
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category-list.html',
                                objects_list=site.categories)


@AppRoute(routes=routes, url='/copy-series/')
class CopySeries:
    @Debug(name='CopySeries')
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']
            old_series = site.get_series(name)
            if old_series:
                new_name = f'copy_{name}'
                new_series = old_series.clone()
                new_series.name = new_name
                site.serieses.append(new_series)

            return '200 OK', render('series-list.html',
                                    objects_list=site.serieses)
        except KeyError:
            return '200 OK', 'No series have been added yet'


@AppRoute(routes=routes, url='/contacts/')
class Contacts:
    @Debug(name='Contacts')
    def __call__(self, request):
        return '200 OK', render('contacts.html', style=request.get('style',
                                                                   None))


@AppRoute(routes=routes, url='/watch/')
class Watch:
    @Debug(name='Watch')
    def __call__(self, request):
        return '200 OK', render('watch.html', style=request.get('style', None),
                                content=request.get('series', None))

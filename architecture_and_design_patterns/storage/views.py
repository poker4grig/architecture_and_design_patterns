from datetime import date
import urllib.parse

from tv_series_fw.templator import render
from patterns.generative_patterns import Interface, Logger

site = Interface()
site.free_users = ['Николай Николаев', 'Петр Петров', 'Иван Иванов']
site.subscribed_users = ['Александр Александров', 'Василий Васильев',
                         'Сергей Сергеев']

logger = Logger('main')


class Index:
    def __call__(self, request):
        # return '200 OK', render('index.html', style=request.get('style', None))
        return '200 OK', render('index.html', objects_list=site.categories)


class About:
    def __call__(self, request):
        # return '200 OK', render('about.html', style=request.get('style', None))
        return '200 OK', render('about.html')


class PageNotExists:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class SeriesSchedule:
    """Расписание сериалов"""
    def __call__(self, request):
        return '200 OK', render('series-schedule.html',  data=date.today())


class SeriesList:
    def __call__(self, request):
        logger.log("Список сериалов")
        try:
            category = site.find_category_by_id(int(request['request_params']['id']))
            return '200 OK', render('series-list.html',
                                    objects_list=category.serieses,
                                    name=category.name, id=category.id)
        except KeyError:
            return '200 OK', 'No series have been added yet'


class CreateSeries:
    """Создать сериал"""
    category_id = -1

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


class CreateCategory:

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
            return '200 OK', render('create-category.html', categories=categories)


class CategoryList:
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category-list.html', objects_list=site.categories)


class CopySeries:
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

            return '200 OK', render('series-list.html', objects_list=site.serieses)
        except KeyError:
            return '200 OK', 'No series have been added yet'


class Contacts:
    def __call__(self, request):
        return '200 OK', render('contacts.html', style=request.get('style', None))


class Watch:
    def __call__(self, request):
        return '200 OK', render('watch.html', style=request.get('style', None), content=request.get('series', None))

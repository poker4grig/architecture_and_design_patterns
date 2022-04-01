# слои middleware

from datetime import date


def middleware_date(request):
    request['data'] = date.today()


films = ['Любовь и голуби (СССР, реж. В. Меньшов, 1984 год, рейтинг 8.3)',
         'Игра престолов (США, Великобритания, реж. Дэвид Наттер, 2019 год, рейтинг 9.0)',
         'Программисты (США, Великобритания, реж. Алекс Гарленд, 2020 год, рейтинг 7.4)']


def middleware_series(request):
    request['series'] = films


def middle_css(request):
    with open('templates/css/style.css') as file:
        css_file = file.read()
        request['style'] = css_file


middlewares = [middleware_date, middleware_series, middle_css]

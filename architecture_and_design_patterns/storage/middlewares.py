# слои middleware
from json import loads
from requests import get
from datetime import date


def middleware_date(request):
    request['date'] = date.today()


films = ['Побег из Шоушенка, 1994, Фрэнк Дарабонт, драма, рейтинг 8.5)',
         'Крёстный отец, 1972, Фрэнсис Форд Коппола, детектив, драма, рейтинг 9.0)',
         'Крёстный отец 2, 1974, Фрэнсис Форд Коппола, детектив, драма, рейтинг 8.0)',
         'Тёмный рыцарь, 2008, Кристофер Нолан, боевик, детектив, драма, рейтинг 8.7)',
         '12 разгневанных мужчин, 1957, Сидни Люмет, драма, детектив, рейтинг 7.9)',
         'Список Шиндлера, 1993, Стивен Спилберг,	драма, биография, исторический фильм, рейтинг 8.0)',
         'Властелин колец: Возвращение короля, 2003, Питер Джексон, фэнтези, приключение, боевик, рейтинг 8.8)',
         'Криминальное чтиво,	1994, Квентин Тарантино, чёрная комедия, драма, рейтинг 7.8)',
         'Властелин колец: Братство Кольца, 2001,	Питер Джексон, фэнтези, приключение, боевик, рейтинг 9.0)',
         'Хороший, плохой, злой, 1966, Серджо Леоне, приключение, вестерн, рейтинг 8.2)',
         'Форрест Гамп, 1994,	Роберт Земекис,	драма, мелодрама, рейтинг 8.5)',
         'Бойцовский клуб, 1999, Дэвид Финчер, драма, триллер, мистический фильм, рейтинг 8.8)',
         'Любовь и голуби (СССР, реж. В. Меньшов, 1984 год, рейтинг 8.3)',
         'Игра престолов (США, Великобритания, реж. Дэвид Наттер, 2019 год, рейтинг 9.0)',
         'Программисты (США, Великобритания, реж. Алекс Гарленд, 2020 год, рейтинг 7.4)']


def middleware_series(request):
    request['series'] = films


def middle_css(request):
    with open('templates/css/style.css') as file:
        css_file = file.read()
        request['style'] = css_file


# Регион пользователя (служба работает с перебоями)
def get_geo_info(request):
    # ip_addr = environ.get('REMOTE_ADDR', '')
    ip_addr = '91.108.35.134'
    if ip_addr:
        request_url = 'https://geolocation-db.com/jsonp/' + ip_addr
        response = get(request_url)
        result = response.content.decode()
        result = result.split("(")[1].strip(")")
        request['geo'] = loads(result)


# middlewares = [middleware_date, middleware_series, middle_css, get_geo_info]
middlewares = [middleware_date, middleware_series, middle_css]

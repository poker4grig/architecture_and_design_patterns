import copy
import urllib.parse


# абстрактный пользователь
class User:
    pass


# Пользователь без подписки
class FreeUser(User):
    pass


# Пользователь с подпиской
class SubscribedUser(User):
    pass


# порождающий паттерн Абстрактная фабрика - фабрика пользователей
class UserFactory:
    types = {
        'free': FreeUser,
        'subscribed': SubscribedUser
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_):
        return cls.types[type_]()


# порождающий паттерн Прототип - Подписки (уровень доступа)
class SeriesPrototype:

    def clone(self):
        return copy.deepcopy(self)


class Series(SeriesPrototype):
    """Класс - сериалы"""
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.serieses.append(self)


class Online(Series):
    pass


class Record(Series):
    pass


class Category:
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.serieses = []

    def series_count(self):
        result = len(self.serieses)
        if self.category:
            result += self.category.series_count()
        return result


class SeriesFactory:
    types = {
        'online': Online,
        'record': Record
    }

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


class Interface:
    def __init__(self):
        self.free_users = []
        self.subscribed_users = []
        self.serieses = []
        self.categories = []

    @staticmethod
    def create_user(type_):
        return UserFactory.create(type_)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    @staticmethod
    def create_series(type_, name, category):
        return SeriesFactory.create(type_, name, category)

    def get_series(self, name):
        for item in self.serieses:
            if item.name == name:
                return item
        return None

    @staticmethod
    def decode_value(val):
        value = urllib.parse.unquote_plus(val)
        # val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        # val_decode_str = quopri.decodestring(val_b

        return value

class SingletonByName(type):
    """Одиночка - метакласс, т.н. "Фабрика классов"""

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print('log--->', text)

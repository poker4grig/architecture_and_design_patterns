import copy
import urllib.parse
from patterns.behavioral_patterns import Subject, ConsoleWriter


# абстрактный пользователь
class User:
    def __init__(self, name):
        self.name = name


# Пользователь без подписки
class Staff(User):
    pass


# Пользователь с подпиской
class Visitor(User):
    def __init__(self, name):
        self.serieses = []
        super().__init__(name)


# порождающий паттерн Абстрактная фабрика - фабрика пользователей
class UserFactory:
    types = {
        'staff': Staff,
        'visitor': Visitor
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


# порождающий паттерн Прототип - Добавление посетителя к просмотру сериала
class SeriesPrototype:

    def clone(self):
        return copy.deepcopy(self)


class Series(SeriesPrototype, Subject):
    """Класс - сериалы"""
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.serieses.append(self)
        self.visitors = []
        super().__init__()

    def __getitem__(self, item):
        return self.visitors[item]

    def add_visitor(self, visitor: Visitor):
        self.visitors.append(visitor)
        visitor.serieses.append(self)
        self.notify()


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
        self.staffs = []
        self.visitors = []
        self.serieses = []
        self.categories = []

    @staticmethod
    def create_user(type_, name):
        return UserFactory.create(type_, name)

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

    def get_series(self, name) -> Series:
        for item in self.serieses:
            if item.name == name:
                return item
        return None

    def get_visitor(self, name) -> Visitor:
        for item in self.visitors:
            if item.name == name:
                return item

    @staticmethod
    def decode_value(val):
        value = urllib.parse.unquote_plus(val)
        # val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        # val_decode_str = quopri.decodestring(val_b
        # return val_decode_str.decode('UTF-8')
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

    def __init__(self, name, writer=ConsoleWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        text = f'log---> {text}'
        self.writer.write(text)

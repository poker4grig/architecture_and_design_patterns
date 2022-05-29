import copy
import sqlite3
import urllib.parse

from patterns.behavioral_patterns import Subject, ConsoleWriter
from patterns.architectural_patterns import DomainObject


# абстрактный пользователь
class User:
    def __init__(self, name):
        self.name = name


# Пользователь без подписки
class Staff(User):
    pass


# Пользователь с подпиской
class Visitor(User, DomainObject):
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


class VisitorMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'visitor'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            visitor = Visitor(name)
            visitor.id = id
            result.append(visitor)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, name FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Visitor
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name) VALUES (?)"
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"
        # находим id с самым большим значением (последний добавленный user)
        _id = f"SELECT * FROM {self.tablename} ORDER BY id DESC LIMIT 1"
        self.cursor.execute(_id)
        obj.id = self.cursor.fetchone()[0]
        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


connection = sqlite3.connect('patterns.sqlite')


# архитектурный системный паттерн - Data Mapper
class MapperRegistry:
    mappers = {
        'visitor': VisitorMapper,
        # 'category': CategoryMapper
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Visitor):
            return VisitorMapper(connection)
        # if isinstance(obj, Category):
        #     return CategoryMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)


# Собственные исключения
class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')

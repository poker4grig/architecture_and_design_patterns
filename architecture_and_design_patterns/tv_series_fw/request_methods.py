class ParseRequest:
    """Класс родитель, передающий наследникам метод для парсинга данных"""
    @staticmethod
    def parse_incoming_data(data: str) -> dict:
        result = dict()
        if data:
            params = data.split('&')
            for param in params:
                key, value = param.split('=')
                result[key] = value
        return result


class GetMethod(ParseRequest):
    @staticmethod
    def get_request_params(environ):
        query_string = environ['QUERY_STRING']
        params = GetMethod.parse_incoming_data(query_string)
        return params


class PostMethod(ParseRequest):
    @staticmethod
    def get_wsgi_incoming_data(dictionary: dict) -> bytes:
        content_length_data = dictionary.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        data = dictionary['wsgi.input'].read(content_length) if content_length \
            else b''
        return data

    def parse_wsgi_incoming_data(self, data: bytes) -> dict:
        result = dict()
        if data:
            data_string = data.decode(encoding='utf-8')
            result = self.parse_incoming_data(data_string)
        return result

    def get_request_params(self, environ):
        data = self.get_wsgi_incoming_data(environ)
        data = self.parse_wsgi_incoming_data(data)
        return data

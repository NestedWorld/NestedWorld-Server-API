import flask_restful as restful
from .shortcuts import Shortcuts


class Namespace(Shortcuts):

    def __init__(self, api, parent, name):
        self.api = api
        self.parent = parent
        self.name = name

    @property
    def path(self):
        path = [self.name]
        if self.parent is not None:
            path = self.parent.path + path

        return path

    @property
    def endpoint(self):
        return '.'.join(self.path)

    def add_resource(self, resource, *urls, **kwargs):
        full_urls = [''.join('/' + name for name in self.path) + url for url in urls]

        endpoint = kwargs.pop('endpoint', None) or resource.__name__.lower()
        endpoint = '%s.%s' % (self.endpoint, endpoint)
        self.api.add_resource(resource, *full_urls, endpoint=endpoint, **kwargs)

    def route(self, *urls, **kwargs):
        def wrapper(resource):
            self.add_resource(resource, *urls, **kwargs)

            return resource

        return wrapper

    def namespace(self, *args, **kwargs):
        return Namespace(self.api, self, *args, **kwargs)

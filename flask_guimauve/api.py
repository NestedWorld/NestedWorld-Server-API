from flask.ext import restful
from .shortcuts import Shortcuts

class Api(restful.Api, Shortcuts):

    def __init__(self, spec, app=None, **kwargs):
        super().__init__(app, **kwargs)
        self.spec = spec

        # Add necessary plugins to spec
        # self.spec.setup_plugin('apispec.ext.flask')
        # self.spec.setup_plugin('apispec.ext.marshmallow')

    def namespace(self, *args, **kwargs):
        from .namespace import Namespace

        return Namespace(self, None, *args, **kwargs)

    def add_resource(self, resource, *urls, **kwargs):
        super().add_resource(resource, *urls, **kwargs)
        print(resource)

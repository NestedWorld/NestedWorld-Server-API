from flask.ext import restful
from . import swagger
from .shortcuts import Shortcuts

class Api(restful.Api, Shortcuts):

    def __init__(self, spec, app=None, **kwargs):
        self.spec = spec

        # Add necessary plugins to spec
        self.spec.setup_plugin('apispec.ext.marshmallow')

        super().__init__(app, **kwargs)

    def init_app(self, app):
        super().init_app(app)

        self.add_resource(self.swagger_view(), '/swagger.json', endpoint='specs')

    def namespace(self, *args, **kwargs):
        from .namespace import Namespace

        return Namespace(self, None, *args, **kwargs)

    def add_resource(self, resource, *urls, **kwargs):
        super().add_resource(resource, *urls, **kwargs)
        swagger.process_doc(self.spec, resource, list(urls))

    def swagger_view(self):
        class SwaggerView(restful.Resource):
            api = self

            def get(self):
                return self.api.spec.to_dict()

        return SwaggerView

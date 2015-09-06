from flask.ext.restplus import Api
from flask.ext.restplus.namespace import ApiNamespace


class NestableApiNamespace(ApiNamespace):

    def __init__(self, api, parent, *args, **kwargs):
        super().__init__(api, *args, **kwargs)

        if parent is not None:
            self.path = parent.path + self.path

    def namespace(self, *args, **kwargs):
        ns = NestableApiNamespace(self.api, self, *args, **kwargs)
        self.add_namespace(ns)
        return ns

    # Proxify API methods in namespace
    def _api_proxy(name):
        def wrapper(self, *args, **kwargs):
            meth = getattr(self.api, name)
            return meth(*args, **kwargs)
        return wrapper

    abort = _api_proxy('abort')
    add_namespace = _api_proxy('add_namespace')
    doc = _api_proxy('doc')
    marshal_with = _api_proxy('marshal_with')
    model = _api_proxy('model')
    parser = _api_proxy('parser')


class Api(Api):

    def namespace(self, *args, **kwargs):
        ns = NestableApiNamespace(self, None, *args, **kwargs)
        self.add_namespace(ns)
        return ns

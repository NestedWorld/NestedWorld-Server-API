from apispec.ext.marshmallow import swagger
from functools import wraps

def process_resource(spec, resource, urls):
    operations = {}

    for method in resource.methods:
        method_name = method.lower()
        method_view = getattr(resource, method_name)

        # Define operation
        operation = {}

        if hasattr(method_view, '__doc__'):
            operation['description'] = method_view.__doc__

        # Define operation response
        responses = {200: {}}

        if hasattr(method_view, '__marshal_with__'):
            res = method_view.__marshal_with__
            process_schema(spec, res['schema'])
            responses[200]['schema'] = res['schema']

        operation['responses'] = responses

        # Define operation parameters
        if hasattr(method_view, '__accept__'):
            accept = method_view.__accept__
            process_schema(spec, accept['schema'])
            operation['parameters'] = swagger.schema2parameters(accept['schema'], spec=spec, dump=False)

        # Add operation
        operations[method_name] = operation

    for url in urls:
        spec.add_path(url, operations=operations, view=None)

def process_schema(spec, schema):
    schema_cls = schema.__class__
    name = '%s.%s' % (schema_cls.__module__, schema_cls.__qualname__)

    spec.definition(name, schema=schema_cls)

# Fix something in swagger spec generation
# FIXME: Warning, black magic. Create a PR in apispec repo to fix this.
def replace(orig_fn):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            return f(orig_fn, *args, **kwargs)
        return wrapped
    return wrapper

@replace(swagger.field2property)
def field2property(orig_fn, *args, **kwargs):
    prop = orig_fn(*args, **kwargs)

    field = args[0]
    if field.dump_only:
        prop['readOnly'] = True

    return prop

if swagger.field2property != field2property:
    swagger.field2property = field2property

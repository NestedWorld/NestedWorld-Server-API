import re
from apispec.ext.marshmallow import swagger
from functools import wraps


def process_resource(spec, resource, urls):
    operations = {}

    for method in resource.methods:
        method_name = method.lower()
        method_view = getattr(resource, method_name)

        # Define operation
        operation = {
            'responses': {200: {}},
            'parameters': [],
        }

        if hasattr(method_view, '__doc__'):
            doc = method_view.__doc__
            if doc is not None:
                doc = doc.strip()
                if '\n\n' in doc:
                    (summary, description) = doc.split('\n\n', 1)
                elif len(doc) < 120:
                    summary = doc
                    description = None
                else:
                    summary = None
                    description = doc

                if summary is not None:
                    operation['summary'] = summary.strip()
                if description is not None:
                    operation['description'] = description.strip()

        if hasattr(resource, 'tags'):
            operation['tags'] = resource.tags

        # Define operation response
        if hasattr(method_view, '__marshal_with__'):
            res = method_view.__marshal_with__
            process_schema(spec, res['schema'])
            operation['responses'][200]['schema'] = res['schema']
            operation['produces'] = ['application/json']

        # Define operation parameters
        if hasattr(method_view, '__accept__'):
            accept = method_view.__accept__
            process_schema(spec, accept['schema'])
            operation['parameters'].extend(swagger.schema2parameters(accept['schema'], spec=spec, dump=False))
            operation['consumes'] = ['application/json']

        # Add operation
        operations[method_name] = operation

    for url in urls:
        url = re.sub(r'<([^:]+:)?(?P<name>[^>]+)>', '{\g<name>}', url)
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

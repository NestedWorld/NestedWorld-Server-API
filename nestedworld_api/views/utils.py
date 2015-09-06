from flask import Blueprint


class NestableBlueprint(Blueprint):

    """
    Hacking in support for nesting blueprints, until hopefully https://github.com/mitsuhiko/flask/issues/593 will be resolved
    """

    def register_blueprint(self, blueprint, **options):
        def deferred(state):
            url_prefix = (state.url_prefix or "") + \
                (options.get('url_prefix', blueprint.url_prefix) or "")
            if 'url_prefix' in options:
                del options['url_prefix']

            state.app.register_blueprint(
                blueprint, url_prefix=url_prefix, **options)
        self.record(deferred)

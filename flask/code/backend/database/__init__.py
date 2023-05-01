from sqlalchemy import engine_from_config
from .engine import *
from .maps import initialize_sql


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.scan('database.maps')  # the "important" line
    engine = get_engine()
    initialize_sql(engine)
    # other statements here
    config.add_handler('main', '/{action}',
                       'maps.handlers:MyHandler')
    return config.make_wsgi_app()

import posixpath

from py_mini_racer import py_mini_racer
from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.exceptions import ImproperlyConfigured


def get_options():
    default = {
        'transpiler': 'npm/@babel/standalone@7.12.15/babel.min.js',
        'extensions': ['.jsx'],
        'options': {
            "presets": ["react"],
            "generatorOpts": {
                "jsescOption": {
                    "minimal": True
                }
            }
        },
        'mimetypes': {
            '.jsx': 'application/javascript'
        },
        'setup': None
    }

    if hasattr(settings, 'BABEL_TRANSPILING'):
        default.update(settings.BABEL_TRANSPILING)

    path = get_absolute_path(default['transpiler'])
    if not path:
        raise ImproperlyConfigured('BABEL_TRANSPILING.transpiler')

    if default['setup']:
        path = get_absolute_path(default['setup'])
        if not path:
            raise ImproperlyConfigured('BABEL_TRANSPILING.setup')

    mimetype_keys = list(default['mimetypes'].keys())
    for item in default['extensions']:
        if item not in mimetype_keys:
            raise ImproperlyConfigured(f'BABEL_TRANSPILING.mimetypes missing extension: {item}')

    return default


def get_absolute_path(path):
    normalized_path = posixpath.normpath(path).lstrip('/')
    return finders.find(normalized_path)


def get_file_content(path):
    file = open(path)
    code = file.read()
    file.close()
    return code


def get_transpiler(options):
    ctx = py_mini_racer.MiniRacer()
    ctx.eval(get_file_content(get_absolute_path(options['transpiler'])))

    if options['setup']:
        ctx.eval(get_file_content(get_absolute_path(options['setup'])))

    return ctx

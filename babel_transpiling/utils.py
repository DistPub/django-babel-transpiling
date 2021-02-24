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
            'plugins': ['transform-import-cssm'],
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
        'setup': ['npm/babel-plugin-transform-import-cssm@1.0.0/index.standalone.js']
    }

    if hasattr(settings, 'BABEL_TRANSPILING'):
        default.update(settings.BABEL_TRANSPILING)

    def validate_config(name, tips):
        path = get_absolute_path(name)
        if not path:
            raise ImproperlyConfigured(tips)

    validate_config(default['transpiler'], 'BABEL_TRANSPILING.transpiler')
    for name in default['setup']:
        validate_config(name, 'BABEL_TRANSPILING.setup')

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

    for name in options['setup']:
        ctx.eval(get_file_content(get_absolute_path(name)))

    return ctx

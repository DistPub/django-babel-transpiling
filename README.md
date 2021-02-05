# django-babel-transpiling
Bring babel to your django project, transpiling static .jsx files on the fly, without NodeJS require!

# Install

`pip install django-babel-transpiling`

# Config

1. Add `babel_transpiling` to your django `INSTALLED_APPS`
1. Add `babel_transpiling.middlewares.StaticFilesTranspilingMiddleware` to your django `MIDDLEWARE`
    >note the order
    ```
    [
    ...
    'babel_transpiling.middlewares.StaticFilesTranspilingMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    ... 
    ]
    ```
1. config django `STATICFILES_STORAGE = 'babel_transpiling.storage.StaticFilesTranspilingStorage'`

# Options

the default options is:

```
{
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
```

you can customize by provide `BABEL_TRANSPILING` in your django settings, for example, custom babel preset:

```
BABEL_TRANSPILING = {
    'options': {
        "presets": ["typescript"]
    }
}
```

# Babel API

You can control more by set `setup` option, for example, write custom plugin and register:

```
$ cat path/to/setup.js

// Simple plugin that converts every identifier to "LOL"
function lolizer() {
  return {
    visitor: {
      Identifier(path) {
        path.node.name = 'LOL';
      }
    }
  }
}
Babel.registerPlugin('lolizer', lolizer);
``` 

then config options:

```
BABEL_TRANSPILING = {
    'options': {
        'plugins': ['lolizer']
    },
    'setup': 'path/to/setup.js'
}
```
    
# FAQ

1. static file not get transpiled
    >if you use django `runserver` command to run server and the setting `DEBUG=True`, please add `--nostatic` option to command

1. I want use other storage
    >you should write your own storage to inherit `StaticFilesTranspilingStorage`

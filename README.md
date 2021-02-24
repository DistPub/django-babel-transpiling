# django-babel-transpiling
Bring babel to your django project, transpiling static .jsx files on the fly, without NodeJS require!

# Install

`pip install django-babel-transpiling`

# Static files transpiling config

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
1. Config django `STATICFILES_STORAGE = 'babel_transpiling.storage.StaticFilesTranspilingStorage'`

# Global Options

Default options is:

```
{
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
```

You can customize by provide `BABEL_TRANSPILING` in your django settings, for example, custom babel preset:

```
BABEL_TRANSPILING = {
    'options': {
        "filename": "index.ts",
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

Then config options:

```
BABEL_TRANSPILING = {
    'options': {
        'plugins': ['lolizer']
    },
    'setup': ['path/to/setup.js']
}
```

# Template Support

Sometimes transpiling in your template file is more make sense than static file, 
you can use `transpiling` tag to do that.

```
{% load babel_transpiling %}
...
<script>
    {% transpiling %}
      ReactDOM.render(<App/>, document.querySelector('#root'))
    {% endtranspiling %}
</script> 
...
```

Template tag also support use custom transpiling option, for example, in context there exists a `ts` option:

```
{% transpiling options=ts %}
  const anExampleVariable: string = "Hello World"
  console.log(anExampleVariable)
{% endtranspiling %}
```
    
# FAQ

1. Static file not get transpiled
    >if you use django `runserver` command to run server and the setting `DEBUG=True`, please add `--nostatic` option to command

1. I want use other storage
    >you should write your own storage to inherit `StaticFilesTranspilingStorage`

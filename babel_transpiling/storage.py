import os

from django.contrib.staticfiles.storage import StaticFilesStorage

from babel_transpiling.utils import get_options, get_transpiler


class StaticFilesTranspilingStorage(StaticFilesStorage):
    """
    Transpiling static files when execute `collectstatic` command
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.options = get_options()
        self.ctx = get_transpiler(self.options)

    def _save(self, name, content):
        origin = super()._save(name, content)
        _, file_suffix = os.path.splitext(name)

        if file_suffix not in self.options['extensions']:
            return origin

        file = open(self.path(name), 'r+')
        result = self.ctx.call('Babel.transform', file.read(), self.options['options'])
        file.seek(0)
        file.truncate()
        file.write(result['code'])
        file.close()
        return origin

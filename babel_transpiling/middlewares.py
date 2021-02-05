import os

from django.conf import settings
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

from babel_transpiling.utils import get_options, get_absolute_path, get_file_content, get_transpiler


class StaticFilesTranspilingMiddleware(MiddlewareMixin):
    """
    Transpiling static files

    Note: if you use django build-in `runserver` command?
        You **MUST** add `--nostatic` option to command to make sure static file request also pass through middleware
    """
    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.options = get_options()
        if settings.DEBUG:
            self.ctx = get_transpiler(self.options)

    def process_response(self, request, response):
        if not self.check_request(request):
            return response

        if settings.DEBUG:
            return self.transpiling(request, response)
        return self.fixup_content_type(request, response)

    def check_request(self, request):
        if not request.path.startswith(settings.STATIC_URL):
            return False

        file_path = request.path[len(settings.STATIC_URL):]
        _, file_suffix = os.path.splitext(file_path)

        if file_suffix not in self.options['extensions']:
            return False

        return True

    def transpiling(self, request, response):
        path = get_absolute_path(request.path[len(settings.STATIC_URL):])
        if not path:
            return response

        result = self.ctx.call('Babel.transform', get_file_content(path), self.options['options'])
        _, file_suffix = os.path.splitext(path)
        return HttpResponse(content=result['code'], content_type=self.options['mimetypes'][file_suffix])

    def fixup_content_type(self, request, response):
        _, file_suffix = os.path.splitext(request.path)
        response['Content-Type'] = self.options['mimetypes'][file_suffix]
        return response

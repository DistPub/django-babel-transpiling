from babel_transpiling.utils import get_options, get_transpiler
from django import template
from django.template import TemplateSyntaxError
from django.template.base import token_kwargs

register = template.Library()


@register.tag('transpiling')
def transpiling_block(parser, token):
    bits = token.split_contents()
    remaining_bits = bits[1:]
    options = token_kwargs(remaining_bits, parser, support_legacy=True)
    if remaining_bits:
        raise TemplateSyntaxError("%r received an invalid token: %r" %
                                  (bits[0], remaining_bits[0]))

    nodelist = parser.parse(('endtranspiling',))
    parser.delete_first_token()
    return TranspilingNode(nodelist, options=options)


class TranspilingNode(template.Node):
    def __init__(self, nodelist, options=None):
        self.nodelist = nodelist
        self.options = options or {}

    def __repr__(self):
        return '<%s>' % self.__class__.__name__

    def render(self, context):
        code = self.nodelist.render(context)

        options = get_options()
        options.update({key: val.resolve(context) for key, val in self.options.items()})
        transpiler = get_transpiler(options)

        result = transpiler.call('Babel.transform', code, options['options'])
        return result['code']

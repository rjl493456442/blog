from BeautifulSoup import BeautifulSoup
from django import template
from django.template.defaultfilters import stringfilter

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter

register = template.Library()

@register.filter    # Register the function as a filter
@stringfilter       # Filter expects a string as input
def highlight_code(html):
    soup = BeautifulSoup(html)
    preblocks = soup.findAll('pre')
    for block in preblocks:
        if block.has_key('class'):
            # a language has been specify
            code = ''.join([unicode(itm) for itm in block.contents])
            print block['class']
            lexer = get_lexer_by_name(block['class'])
            formatter = HtmlFormatter()
            code_hl = highlight(code, lexer, formatter)
            block.contents = [BeautifulSoup(code_hl)]
            block.name = 'code'
        else:
            # default language is text
            pass
    return unicode(soup)


#coding:utf-8

from django import template

register = template.Library()

@register.filter(name = 'sub')
def sub(var, arg):
    if not var:
        return var
    try:
        var = int(var)
        arg = int(arg)
    except TypeError:
        return var
    return var - arg



from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def aaa():
    res = "<a href='www.baidu.com'>dasdas</a>"
    return mark_safe(res)

@register.inclusion_tag('mytable.html',takes_context=True)
def mytable(context,data_list,head_list):
    print('---------',data_list)

    data = {
        'data_list':data_list,
        'head_list':head_list,
    }
    return data
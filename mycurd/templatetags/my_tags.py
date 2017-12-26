from django import template
from django.http import QueryDict
from django.utils.safestring import mark_safe
from mycurd.server.v1 import site
from django.shortcuts import reverse
from django.forms.models import ModelChoiceField,ModelMultipleChoiceField

register = template.Library()


@register.inclusion_tag('curd/mytable.html', takes_context=True)
def mytable(context,data_list,head_list):

    data = {
        'data_list':data_list,
        'head_list':head_list,
    }
    return data

@register.inclusion_tag('curd/form.html')
def myform(config,model_form_obj):
    new_form = []
    for bfield in model_form_obj:
        temp = {'is_popup': False, 'field': bfield}
        if isinstance(bfield.field, ModelChoiceField):  # 锁定多对多或外键字段
            related_class = bfield.field.queryset.model  # 字段所关联的类
            if related_class in site._registry:
                app_model_name = bfield.field.queryset.model._meta.app_label, bfield.field.queryset.model._meta.model_name
                base_url = reverse("curd:%s_%s_add" % app_model_name)  # 找到外键对应表的添加页面
                model_name = config.model_class._meta.model_name  # 当前页面的类名
                related_name = config.model_class._meta.get_field(bfield.name).rel.related_name  # 字段对象的related_name
                popup_url = "%s?_popbackid=%s&model_name=%s&related_name=%s"%(base_url, bfield.auto_id, model_name, related_name)
                temp['is_popup'] = True
                temp['popup_url'] = popup_url
        new_form.append(temp)
    return {'form': new_form}

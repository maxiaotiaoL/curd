from django.forms import ModelForm
from django.forms import widgets as wd
from django.http import QueryDict
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.conf.urls import url,include
from django.shortcuts import HttpResponse, redirect, render

from mycurd.server import v1
from crm import models


class PaymentRecordConfig(v1.CurdConfig):
    """
    缴费记录
    """

    def pay_type_display(self,obj=None,is_header=False):
        if is_header:
            return '费用类型'
        return obj.get_pay_type_display()

    list_display = ['customer','class_list',pay_type_display,'paid_fee','date','consultant']

    show_add_btn = True
    show_search_form = True

    show_comb_filter = True
    comb_filter = [
        v1.FilterOption('customer'),
        v1.FilterOption('class_list'),
        v1.FilterOption('pay_type',is_choice=True),
    ]
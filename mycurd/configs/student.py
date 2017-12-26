from django.forms import ModelForm
from django.forms import widgets as wd
from django.http import QueryDict
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.conf.urls import url,include
from django.shortcuts import HttpResponse, redirect, render

from mycurd.server import v1
from crm import models



class StudentConfig(v1.CurdConfig):
    def class_list_display(self,obj=None,is_header=False):
        if is_header:
            return '已报班级'
        return ','.join(['%s(%s期)'%(cls.course.name,cls.semester) for cls in obj.class_list.all()])

    list_display = ['customer',class_list_display,'company']
    edit_link = ['customer',]

    show_add_btn = True
    show_search_form = True

    show_comb_filter = True
    comb_filter = [
        v1.FilterOption('class_list'),
    ]
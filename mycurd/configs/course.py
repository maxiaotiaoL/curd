from django.forms import ModelForm
from django.forms import widgets as wd
from django.http import QueryDict
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.conf.urls import url,include
from django.shortcuts import HttpResponse, redirect, render

from mycurd.server import v1
from crm import models


class CourseConfig(v1.CurdConfig):
    list_display = ['id','name']
    show_add_btn = True  # 添加按钮是否显示
    show_search_form = True  # 显示搜索控件
    search_fields = ['name__contains',]  # 搜索的字段
    edit_link = ['name',]

    def multi_del(self,request):
        pk_list = request.POST.getlist('pk')
        self.model_class.objects.filter(id__in=pk_list).delete()
    multi_del.short_desc = "批量删除"

    def multi_init(self,request):
        pk_list = request.POST.getlist('pk')
    multi_init.short_desc ="批量初始化"

    show_action_list = True
    action_list = [multi_del, multi_init]
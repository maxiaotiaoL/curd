from django.forms import ModelForm
from django.forms import widgets as wd
from django.http import QueryDict
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.conf.urls import url,include
from django.shortcuts import HttpResponse, redirect, render

from mycurd.server import v1
from crm import models


class ClassListConfig(v1.CurdConfig):
    def course_semester(self,obj=None,is_header=False):
        if is_header:
            return '班级'
        return "%s(%s期)"%(obj.course.name,obj.semester)

    def num(self,obj=None,is_header=False):
        if is_header:
            return '人数'
        print(obj.id)
        print(obj.student_set.all())
        return obj.student_set.all().count()

    def display_teachers(self,obj=None,is_header=False):
        if is_header:
            return '任课老师'
        return ','.join([x.name for x in obj.teachers.all()])

    list_display = ['id',course_semester,num,'school',display_teachers,'tutor']

    edit_link = [course_semester, ]
    show_add_btn = True  # 添加按钮是否显示

    show_search_form = True  # 显示搜索控件
    search_fields = ['course__name__contains','semester__contains']  # 搜索的字段

    show_comb_filter = True
    comb_filter = [
        v1.FilterOption('school',),
        v1.FilterOption('course'),
    ]
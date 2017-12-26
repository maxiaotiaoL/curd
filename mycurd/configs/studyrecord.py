from django.forms import ModelForm
from django.forms import widgets as wd
from django.http import QueryDict
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.conf.urls import url,include
from django.shortcuts import HttpResponse, redirect, render

from mycurd.server import v1
from crm import models


class StudyRecordConfig(v1.CurdConfig):
    def record_display(self,obj=None,is_header=False):
        if is_header:
            return '出勤'
        return obj.get_record_display()

    def score_display(self,obj=None,is_header=False):
        if is_header:
            return '本届成绩'
        return obj.get_score_display()

    list_display = ['course_record','student',record_display,score_display]
    edit_link = ['course_record',]

    show_add_btn = False
    show_search_form = True

    show_comb_filter = True
    comb_filter = [
        v1.FilterOption('course_record'),
    ]


    def action_checked(self,request):
        pk_list = request.POST.getlist('pk')
        models.StudyRecord.objects.filter(pk__in=pk_list).update(record='checked')
    action_checked.short_desc ="签到"

    def action_vacate(self,request):
        pk_list = request.POST.getlist('pk')
        print(pk_list)
    action_vacate.short_desc ="请假"

    def action_late(self,request):
        pk_list = request.POST.getlist('pk')
        print(pk_list)
    action_late.short_desc ="缺勤"

    def action_noshow(self,request):
        pk_list = request.POST.getlist('pk')
        print(pk_list)
    action_noshow.short_desc ="缺勤"

    def action_leave_early(self,request):
        pk_list = request.POST.getlist('pk')
        print(pk_list)
    action_leave_early.short_desc ="早退"

    show_action_list = True
    action_list = [action_checked,action_vacate,action_late,action_noshow,action_leave_early]
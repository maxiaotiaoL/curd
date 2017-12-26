from django.forms import ModelForm
from django.forms import widgets as wd
from django.http import QueryDict
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.conf.urls import url,include
from django.shortcuts import HttpResponse, redirect, render

from mycurd.server import v1
from crm import models


class ConsultRecordConfig(v1.CurdConfig):
    list_display = ['customer','consultant','date']

    show_add_btn = True
    show_search_form = True

    comb_filter = [
        v1.FilterOption('customer')
    ]
    show_comb_filter = False

    def changelist_view(self,request,*args,**kwargs):

        # current_login_user = 1
        # customer_id = request.GET.get('customer')
        # ct = models.Customer.objects.filter(consultant=current_login_user,).count()
        # if ct:
        #     return HttpResponse('别抢客户啊...')
        return super(ConsultRecordConfig,self).changelist_view(request)
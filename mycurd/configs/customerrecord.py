from django.forms import ModelForm
from django.forms import widgets as wd
from django.http import QueryDict
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.conf.urls import url,include
from django.shortcuts import HttpResponse, redirect, render

from mycurd.server import v1
from crm import models


class CustomerConfig(v1.CurdConfig):
    def display_gender(self,obj=None,is_header=False):
        if is_header:
            return '性别'
        return obj.get_gender_display()

    def display_education(self,obj=None,is_header=False):
        if is_header:
            return '学历'
        return obj.get_education_display()

    def display_experience(self,obj=None,is_header=False):
        if is_header:
            return '工作经验'
        return obj.get_experience_display()


    def display_course(self,obj=None,is_header=False):
        if is_header:
            return '咨询课程'
        res = []
        query_str = self.request.GET.urlencode()
        params = QueryDict(mutable=True)
        params[self._query_param_key] = query_str

        for course_obj in obj.course.all():
            res.append("<a style='display:inline-block;padding:3px 5px;border:1px solid blue;margin:2px;' href='/curd/crm/customer/%s/%s/dc/?%s'>%s X</a>"%(obj.pk,course_obj.pk,params.urlencode(),course_obj.name))
        return mark_safe(''.join(res))

    def record(self,obj=None,is_header=False):
        if is_header:
            return '跟进记录'

        return mark_safe("<a href='/curd/crm/consultrecord/?customer=%s'>查看跟进记录</a>"%(obj.id))

    def delete_course(self, request, customer_id, course_id):
        """
        删除当前用户感兴趣的课程
        :param request:
        :param customer_id:
        :param course_id:
        :return:
        """
        customer_obj = self.model_class.objects.filter(pk=customer_id).first()
        customer_obj.course.remove(course_id)
        # 跳转回去时，要保留原来的搜索条件
        url = self.get_list_url()+'?'+self.request.GET.get(self._query_param_key)
        return redirect(url)


    def extra_url(self):
        """
        预留的狗子函数，用来单独为某个model类配置额外的接口
        例如报表
        :return:
        """
        app_model_name = (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        patterns = [
            url(r'^(\d+)/(\d+)/dc/$', self.wrap(self.delete_course), name="%s_%s_dc" % app_model_name),
        ]
        return patterns

    list_display = ['id','name',display_gender,display_education,display_experience,
        display_course,'consultant',record]
    show_add_btn = True  # 添加按钮是否显示
    show_search_form = True  # 显示搜索控件
    search_fields = ['name__contains',]  # 搜索的字段
    edit_link = ['name']  # 自定义搜索字段

    def multi_del(self,request):
        pk_list = request.POST.getlist('pk')
        self.model_class.objects.filter(id__in=pk_list).delete()
    multi_del.short_desc = "批量删除"

    def multi_init(self,request):
        pk_list = request.POST.getlist('pk')
    multi_init.short_desc = "批量初始化"

    show_action_list = True
    action_list = [multi_del, multi_init]

    show_comb_filter = True
    comb_filter = [
        v1.FilterOption('gender',is_choice=True),
        v1.FilterOption('education',is_choice=True),
        v1.FilterOption('experience',is_choice=True),
        v1.FilterOption('course'),
        v1.FilterOption('consultant'),
    ]
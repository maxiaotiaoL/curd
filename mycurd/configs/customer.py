
from django.db.models import Q
from django.forms import ModelForm
from django.forms import widgets as wd
from django.http import QueryDict
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.conf.urls import url,include
from django.shortcuts import HttpResponse, redirect, render

from mycurd.server import v1
from crm import models

import datetime
from xxxx import AutoSale
from django.db import transaction



class SingleModelForm(ModelForm):
    class Meta:
        model = models.Customer
        exclude = ['consultant', 'status', 'recv_date', 'last_consult_date']
        # exclude = ['status', 'recv_date', 'last_consult_date']



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
        :return:a
        """
        app_model_name = (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        patterns = [
            url(r'^(\d+)/(\d+)/dc/$', self.wrap(self.delete_course), name="%s_%s_dc" % app_model_name),
            url(r'^public/$', self.wrap(self.public_view), name="%s_%s_public" % app_model_name),
            url(r'^user/$', self.wrap(self.user_view), name="%s_%s_user" % app_model_name),
            url(r'^(\d+)/competition/$', self.wrap(self.competition_view), name="%s_%s_competition" % app_model_name),
            url(r'^single/$', self.wrap(self.single_view), name="%s_%s_single" % app_model_name),
        ]
        return patterns



    def single_view(self,request):
        """
        单条录入
        :param request:
        :return:
        """

        if request.method == 'GET':
            form = SingleModelForm()

            return render(request,'single_view.html',{'form':form})
        else:
            # 单条录入，request.POST就是所有录入的数据
            form = SingleModelForm(request.POST)
            if form.is_valid():  # 数据校验
                sale_id = AutoSale.get_sale_id()  # 获取销售ID
                if not sale_id:
                    return HttpResponse('没有销售，无法进行自动分配')
                try:
                    with transaction.atomic():
                        # 创建客户表记录 - 缺失（销售ID，销售接客时间）
                        form.instance.consultant_id = sale_id
                        form.instance.recv_date = datetime.datetime.now().date()
                        newcustomer_obj = form.save()

                        # 创建客户分配表记录 - 缺失（新创建客户的ID，顾问的ID）
                        models.CustomerDistribution.objects.create(user_id=sale_id, customer=newcustomer_obj.id,memo='系统分配')
                except Exception as e:
                    AutoSale.rollback(sale_id)
                    return HttpResponse('录入异常')

                return HttpResponse('录入成功')
            else:
                print(form.errors)
                return render(request,'single_view.html',{'form':form})

    def competition_view(self,request,customer_id):
        """
        抢单
        :param request:
        :return:
        """
        current_user_id = 6
        print(customer_id)
        now_date = datetime.datetime.now().date()
        no_follow = now_date - datetime.timedelta(days=3)  # 3天未跟进
        no_deal = now_date - datetime.timedelta(days=15)  # 15天未跟进
        # 原顾问不是自己，状态为未报名，3/15
        row_count = models.Customer.objects.filter((Q(last_consult_date__lt=no_follow)|Q(recv_date__lt=no_deal)),status=2,id=customer_id)\
            .exclude(consultant_id=current_user_id)\
            .update(recv_date=now_date,consultant_id=current_user_id,last_consult_date=now_date)

        if not row_count:
            return HttpResponse('抢单失败')

        models.CustomerDistribution.objects.create(user_id=current_user_id,customer_id=customer_id,ctime=now_date)

        return HttpResponse('抢单成功')


    def user_view(self,request):
        """
        我的客户
        :return:
        """

        current_user_id = 6
        customers = models.CustomerDistribution.objects.filter(user_id=current_user_id).order_by('status')  # 登录用户的所有客户记录
        print(customers)

        return render(request, 'user_customer.html', {'customers':customers})


    def public_view(self,request):
        """
        查看公共客户资源
        :return:
        """
        current_user_id = 6

        now_date = datetime.datetime.now().date()
        no_follow = now_date - datetime.timedelta(days=3)  # 3天未跟进
        no_deal = now_date - datetime.timedelta(days=15)  # 15天未跟进
        customer_list = models.Customer.objects.filter((Q(last_consult_date__lt=no_follow)|Q(recv_date__lt=no_deal)), status=2)

        return render(request, 'public_customer.html', {'customer_list':customer_list,'current_user_id':current_user_id})

    order_by = ['-status',]
    list_display = ['id','name',display_gender,display_education,'status',
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
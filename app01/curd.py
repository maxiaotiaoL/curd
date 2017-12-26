from django.forms import ModelForm
from django.forms import widgets as wd
from django.utils.safestring import mark_safe
from django.conf.urls import url,include
from django.shortcuts import HttpResponse, redirect, render

from mycurd.server import v1
from app01 import models

class UserInfoModelForm(ModelForm):
    class Meta:
        model = models.UserInfo
        fields = '__all__'
        error_messages = {
            'name': {
                'required': '用户名不能为空'
            }
        }

        widgets = {
            'name':wd.TextInput(attrs={'class': 'form-control'}),
            'email':wd.EmailInput(attrs={'class': 'form-control'}),
            'age':wd.TextInput(attrs={'class': 'form-control'}),
        }

class UserInfoConfig(v1.CurdConfig):
    show_add_btn = True  # 添加按钮是否显示
    list_display = ['id', 'name','email']  # 列表页面要展示的字段
    model_form_class = UserInfoModelForm  # 自定制modelform
    def extra_url(self):
        """
        扩展当前model的urlpatterns
        """
        url_patterns = [
            url(r'^func11/$', self.func11),
        ]
        return url_patterns

    def func11(self,request):
        return HttpResponse('func11')

    def delete_view(self,request,nid):
        if request.method == "GET":
            return render(request, 'curd/my_delete.html')
        else:
            self.model_class.objects.filter(pk=nid).delete()
            return redirect(self.get_list_url())

    show_search_form = True  # 显示搜索控件
    search_fields = ['email__contains', 'name__contains']  # 搜索的字段



    def multi_del(self,request):
        pk_list = request.POST.getlist('pk')
        self.model_class.objects.filter(id__in=pk_list).delete()
    multi_del.short_desc = "批量删除"

    def multi_init(self,request):
        pk_list = request.POST.getlist('pk')

    multi_init.short_desc ="批量初始化"

    show_action_list = True
    action_list = [multi_del, multi_init]

    # 组合搜索



class RoleConfig(v1.CurdConfig):
    pass
    # list_display = ['id','caption']

v1.site.register(models.UserInfo,UserInfoConfig)
v1.site.register(models.Role,RoleConfig)


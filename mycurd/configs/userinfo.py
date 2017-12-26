from django.shortcuts import HttpResponse,redirect,render

from mycurd.server import v1

class UserInfoConfig(v1.CurdConfig):
    list_display = ['id','name','username','password','email','depart']
    show_add_btn = True  # 添加按钮是否显示
    show_search_form = True  # 显示搜索控件
    search_fields = ['name__contains', 'username__contains']  # 搜索的字段

    def multi_del(self,request):
        pk_list = request.POST.getlist('pk')
        self.model_class.objects.filter(id__in=pk_list).delete()
    multi_del.short_desc = "批量删除"

    def multi_init(self,request):
        pk_list = request.POST.getlist('pk')
    multi_init.short_desc ="批量初始化"

    show_action_list = True
    action_list = [multi_del, multi_init]

    comb_filter = [
        # v1.FilterOption('depart'),
        v1.FilterOption('depart', text_func_name=lambda x: str(x), val_func_name=lambda x: x.code, )
    ]

    edit_link = ['name',]
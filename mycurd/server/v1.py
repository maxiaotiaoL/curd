from django.conf.urls import url,include
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import QueryDict
from django.shortcuts import HttpResponse,render,redirect
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.forms import ModelForm
import copy
import json

class FilterOption(object):
    def __init__(self,field_name,multi=False,condition=None,is_choice=False,text_func_name=None, val_func_name=None):
        """

        :param field_name:字段名
        :param multi:是否多选
        :param condition:显示数据的筛选条件
        :param is_choice:字段是否是choice类型（否则为外键或多对多）
        """
        self.field_name = field_name
        self.multi = multi
        self.condition = condition
        self.is_choice = is_choice
        self.text_func_name = text_func_name
        self.val_func_name = val_func_name

    def get_querySet(self,_field):
        if self.condition:
            querySet = _field.rel.to.objects.filter(**self.condition)
        else:
            querySet = _field.rel.to.objects.all()
        return querySet


    def get_choices(self,_field):
        return _field.choices


class FilterRow(object):
    """
    组合条件类
    一个对象代表一行条件
    """
    def __init__(self, option, data, request):
        self.option = option
        self.data = data
        self.request = request  # request

    def __iter__(self):
        params = copy.deepcopy(self.request.GET)
        params._mutable = True
        current_id = params.get(self.option.field_name)  # 3
        current_id_list = params.getlist(self.option.field_name)  # [1,2,3]

        if self.option.field_name in params:  # 如果传来的参数中有这个字段,代表全选没有被勾中
            # del params[self.option.field_name]
            origin_list = params.pop(self.option.field_name)  # 删除对应字段，并记录下它的值
            url = "{0}?{1}".format(self.request.path_info, params.urlencode())
            yield mark_safe('<a href="{0}" class="">全部</a>'.format(url))
            params.setlist(self.option.field_name, origin_list)  # 回复原状
        else:  # 传来的参数中没有这个字段,代表全选被勾中
            url = "{0}?{1}".format(self.request.path_info, params.urlencode())
            yield mark_safe('<a class="active" href="{0}">全部</a>'.format(url))

        for val in self.data:
            if self.option.is_choice:  # 字段是choice类型
                pk, text = str(val[0]), val[1]
            else:  # 字段是外键或多对多类型
                # pk, text = str(val.pk), str(val)
                text = self.option.text_func_name(val) if self.option.text_func_name else str(val)
                pk = str(self.option.val_func_name(val)) if self.option.val_func_name else str(val.pk)

            # 当前URL？option.field_name
            # 当前URL？gender=pk
            # self.request.path_info # http://127.0.0.1:8005/arya/crm/customer/?gender=1&id=2
            # self.request.GET['gender'] = 1 # &id=2gender=1

            if not self.option.multi:  # 单选
                params[self.option.field_name] = pk
                url = "{0}?{1}".format(self.request.path_info, params.urlencode())
                if current_id == pk:
                    yield mark_safe("<a class='active' href='{0}'>{1}</a>".format(url, text))
                else:
                    yield mark_safe("<a href='{0}'>{1}</a>".format(url, text))
            else:  # 多选 current_id_list = ["1","2"]
                _params = copy.deepcopy(params)
                id_list = _params.getlist(self.option.field_name)

                if pk in current_id_list:
                    id_list.remove(pk)
                    _params.setlist(self.option.field_name, id_list)
                    url = "{0}?{1}".format(self.request.path_info, _params.urlencode())
                    yield mark_safe("<a class='active' href='{0}'>{1}</a>".format(url, text))
                else:
                    id_list.append(pk)
                    # params中被重新赋值
                    _params.setlist(self.option.field_name, id_list)
                    # 创建URL
                    url = "{0}?{1}".format(self.request.path_info, _params.urlencode())
                    yield mark_safe("<a href='{0}'>{1}</a>".format(url, text))


class ChangeList(object):
    """
    将changelist_view函数中的功能封装到此类中
    """
    def __init__(self, config, querySet):
        self.config = config

        self.list_display = config.get_list_display()
        self.model_class = config.model_class
        self.request = config.request
        self.show_add_btn = config.get_show_add_btn()

        # action
        self.action_list = config.get_action_list()
        self.show_action_list = config.get_show_action_list()
        # search
        self.show_search_form = config.get_show_search_form()
        self.search_form_val = config.request.GET.get(config.search_key, '')

        # 组合条件
        self.comb_filter = config.get_comb_filter()
        self.edit_link = config.get_edit_link()
        self.show_comb_filter = config.get_show_comb_filter()


        from utils.pager import Pagination
        current_page = self.request.GET.get('page', 1)
        total_count = querySet.count()
        pager_obj = Pagination(current_page, total_count, self.request.path_info, self.request.GET)
        self.pager_obj = Pagination(current_page, total_count, self.request.path_info, self.request.GET)
        self.data_list = querySet[pager_obj.start:pager_obj.end]

    def gen_comb_filter(self):
        """
        生成器函数
        根据字段，获取与之关联的数据，交给FilterRow做处理
        :return:
        """

        """
        self.comb_filter = [
             FilterRow(((1,'男'),(2,'女'),)),
             FilterRow([obj,obj,obj,obj ]),
             FilterRow([obj,obj,obj,obj ]),
        ]
        """
        data_list = []
        for option in self.comb_filter:
            _field = self.model_class._meta.get_field(option.field_name)
            from django.db.models import ForeignKey,ManyToManyField
            if isinstance(_field,ForeignKey):
                row = FilterRow(option,option.get_querySet(_field),self.request)
            elif isinstance(_field,ManyToManyField):
                row = FilterRow(option,option.get_querySet(_field),self.request)
            else:
                row = FilterRow(option,option.get_choices(_field),self.request)
            data_list.append(row)
        return data_list

    def modify_actions(self):
        result = []
        for func in self.action_list:
            temp = {'name': func.__name__, 'text': func.short_desc}
            result.append(temp)
        return result



    def add_url(self):
        return self.config.get_add_url()

    def head_list(self):
        """
        构造表头
        :return:
        """
        head_list = []
        if self.list_display:
            for field_name in self.list_display:
                if isinstance(field_name, str):
                    # 根据类和字段名称，获取字段对象的verbose_name
                    verbose_name = self.model_class._meta.get_field(field_name).verbose_name
                else:
                    # 如果是函数名，执行此函数，返回要显示的表头名称
                    verbose_name = field_name(self.config, None, True)
                head_list.append(verbose_name)
        else:
            head_list.append(self.model_class._meta.model_name)
        return head_list




    def body_list(self):
        """
        列表页面的数据部分
        :return:
        """
        data_list = self.data_list
        def get_new_data():
            for row in data_list:
                temp = []
                if self.list_display:
                    for field_name in self.list_display:  # ['id','name','edit']
                        if isinstance(field_name, str):  # 处理正常字段
                            val = getattr(row, field_name)
                        else:  # 自定义的操作列
                            val = field_name(self.config, row)
                        # 用于定制编辑列
                        if field_name in self.edit_link:
                            val = self.edit_link_tag(row.pk, val)
                        temp.append(val)
                else:
                    temp.append(row)
                yield temp
        new_data_g = get_new_data()  # 返回生成器
        return new_data_g

    def edit_link_tag(self,pk,text):
        """
        自定制编辑列的a标签
        :param pk:编辑对象的主键
        :param text: 显示内容
        :return:a标签
        """
        query_str = self.request.GET.urlencode()
        params = QueryDict(mutable=True)
        params[self.config._query_param_key] = query_str
        return mark_safe("<a href='%s?%s'>%s</a>" % (self.config.get_change_url(pk), params.urlencode(), text,))


class CurdConfig(object):
    # 定制列表页面显示的列
    list_display = []
    def __init__(self,model_class,site_obj):
        self.model_class = model_class
        self.site_obj = site_obj
        self.request = None
        self._query_param_key = '_listfilter'
        self.search_key = "_q"


    def get_change_url(self,nid):
        """
        得到编辑按钮对应url
        """
        name = "curd:%s_%s_change"%(self.model_class._meta.app_label,self.model_class._meta.model_name)
        edit_url = reverse(name,args=(nid,))
        return edit_url


    def get_delete_url(self,nid):
        """
        得到删除按钮对应url
        """
        name = "curd:%s_%s_delete"%(self.model_class._meta.app_label,self.model_class._meta.model_name)
        delete_url = reverse(name,args=(nid,))
        return delete_url

    def get_add_url(self):
        """
        得到新增按钮对应url
        """
        name = "curd:%s_%s_add"%(self.model_class._meta.app_label,self.model_class._meta.model_name)
        add_url = reverse(name)
        return add_url

    def get_list_url(self):
        """列表页面对应url
        """
        name = "curd:%s_%s_changelist"%(self.model_class._meta.app_label,self.model_class._meta.model_name)
        list_url = reverse(name)
        return list_url


    def edit(self,obj=None,is_header=False):
        """
        列表页面每行的编辑按钮
        :param obj: 一条记录对象
        :param is_header: 是否作为表头显示
        :return:
        """
        if is_header:
            return '操作'
        # 获取条件，拼接url
        query_str = self.request.GET.urlencode()
        if query_str:
            params = QueryDict(mutable=True)
            params[self._query_param_key] = query_str
            return mark_safe("<a href='%s?%s'>编辑</a>" % (self.get_change_url(obj.id), params.urlencode()))
        return mark_safe("<a href='%s'>编辑</a>" % (self.get_change_url(obj.id)))  # /stark/app01/userinfo

    def checkbox(self,obj=None,is_header=False):
        """
        列表页面每行首部的checkbox
        :param obj: 一条记录对象
        :param is_header: 是否作为表头显示
        :return:
        """
        if is_header:
            return '选择'
        return mark_safe("<input type='checkbox' name='pk' value='%s'>"%obj.id)

    def delete(self,obj=None,is_header=False):
        """
        列表页面每行的删除按钮
        :param obj: 一条记录对象
        :param is_header: 是否作为表头显示
        :return:
        """
        if is_header:
            return '操作'
        return mark_safe("<a href='%s'>删除</a>"%self.get_delete_url(obj.id))

    def get_list_display(self):
        """
        获得列表页面显示的字段
        :return:
        """
        data = []
        if self.list_display:
            data.extend(self.list_display)  # 自定制要显示的字段
            # data.append(CurdConfig.edit)  # 编辑按钮
            data.append(CurdConfig.delete)  # 删除按钮
            data.insert(0,CurdConfig.checkbox)  # 行首checkbox
        return data


    #------------------------URL相关-----------------------------------------

    @property
    def urls(self):
        return self.get_urls()

    def extra_url(self):
        """
        自定义配置类重写此方法，可以扩展当前model_class的url_patterns
        :return:
        """
        url_patterns = []
        return url_patterns

    def wrap(self,view_func):
        def inner(request,*args,**kwargs):
            # 为编辑，添加，删除功能添加request，方便获取原页面的参数
            self.request = request
            return view_func(request,*args,**kwargs)
        return inner

    def get_urls(self):
        app_model_name = (self.model_class._meta.app_label, self.model_class._meta.model_name)
        url_patterns = [
            url(r'^$', self.wrap(self.changelist_view), name="%s_%s_changelist" % app_model_name),
            url(r'^add/$', self.wrap(self.add_view), name="%s_%s_add" % app_model_name),
            url(r'^(\d+)/change/$', self.wrap(self.change_view), name="%s_%s_change" % app_model_name),
            url(r'^(\d+)/delete/$', self.wrap(self.delete_view), name="%s_%s_delete" % app_model_name),
        ]
        url_patterns.extend(self.extra_url())  # 用于当前model扩展url
        return url_patterns

    #-----------------------------------------------------------------

    # 2. 是否显示添加按钮
    show_add_btn = False
    def get_show_add_btn(self):
        return self.show_add_btn

    # 搜索相关-----------------------------------------------------
    show_search_form = False
    def get_show_search_form(self):
        return self.show_search_form

    search_fields = []
    def get_search_fields(self):
        res = []
        if self.search_fields:
            res.extend(self.search_fields)
        return res

    def get_cond_Q(self):
        cond = self.request.GET.get(self.search_key,'')
        q_obj = Q()
        q_obj.connector = 'OR'
        if cond and self.get_show_search_form():
            for field in self.get_search_fields():
                q_obj.children.append((field, cond))
        return q_obj

    # actions相关 ----------------------------------------------------------

    show_action_list = False
    def get_show_action_list(self):
        return self.show_action_list

    action_list = []
    def get_action_list(self):
        res = []
        if self.action_list:
            res.extend(self.action_list)
        return res

    # 组合条件相关 ----------------------------------------------------------
    comb_filter = []
    def get_comb_filter(self):
        res = []
        if self.comb_filter:
            res.extend(self.comb_filter)
        return res


    # ------------------得到配置的编辑列------------
    edit_link = []

    def get_edit_link(self):
        res = []
        if self.edit_link:
            res.extend(self.edit_link)
        return res


    # ---------------复合搜索是否显示---------
    show_comb_filter = False
    def get_show_comb_filter(self):

        return self.show_comb_filter


    def changelist_view(self,request):
        """
        列表页面对应视图函数
        """
        # 处理action
        if request.method == 'POST' and self.get_show_action_list():
            func_name_str = request.POST.get('list_action')
            action_func = getattr(self, func_name_str)
            ret = action_func(request)
            if ret:
                return ret

        # 组合条件
        comb_condition = {}
        option_list = self.get_comb_filter()
        for key in request.GET.keys():
            value_list = request.GET.getlist(key)
            flag = False
            for option in option_list:
                if option.field_name == key:
                    flag = True
                    break

            if flag:
                comb_condition["%s__in" % key] = value_list

        querySet = self.model_class.objects.filter(self.get_cond_Q()).filter(**comb_condition).distinct()
        cl = ChangeList(self,querySet)
        return render(request, 'curd/changelist_view.html', {'cl':cl})


    # 配置model_form_class
    model_form_class = None

    def get_model_form_class(self):
        """
        得到当前类的modelForm
        """
        if self.model_form_class:
            return self.model_form_class

        # 普通青年创建model_form_class
        class TestModelForm(ModelForm):
            class Meta:
                model = self.model_class
                fields = '__all__'

        # 用type生成model_form_class
        # Meta = type('Meta',(object,),{'model':self.model_class,'fields':'__all__'})
        # TestModelForm = type('TestModelForm',(ModelForm,),{'Meta':Meta})
        return TestModelForm


    def add_view(self,request):
        """
        基于ModelForm的新增
        :param request:
        :return:
        """
        TestModelForm = self.get_model_form_class()  # 自定义的
        _popbackid = request.GET.get('_popbackid')

        if request.method == 'GET':  # 进入新增页面
            form = TestModelForm()
            return render(request, 'curd/add_view.html', {'form': form, 'config':self})
        else:  # 确认新增
            form = TestModelForm(request.POST)
            if form.is_valid():
                new_obj = form.save()  # 在数据库中创建数据
                if _popbackid:
                    # 如果是popup请求,render一个页面，写自执行函数
                    from django.db.models.fields.reverse_related import ManyToOneRel,ManyToManyRel
                    result = {'id': None, 'text': None, '_popbackid': _popbackid, 'status': False}
                    model_name = request.GET.get('model_name')
                    related_name = request.GET.get('related_name')
                    for related_obj in new_obj._meta.related_objects:  # 当前表所有外键关联的表对象
                        _model_name = related_obj.field.model._meta.model_name
                        _related_name = related_obj.related_name
                        if type(related_obj) == ManyToOneRel:
                            _field_name = related_obj.field_name
                        else:
                            _field_name = 'pk'
                        _limit_choices_to = related_obj.limit_choices_to
                        if model_name == _model_name and related_name == str(_related_name):
                            is_exists = self.model_class.objects.filter(**_limit_choices_to,pk=new_obj.pk).exists()
                            if is_exists:
                                result['status'] = True
                                result['text'] = str(new_obj)
                                result['id'] = getattr(new_obj,_field_name)
                                return render(request, 'curd/popup_response.html',{'result': json.dumps(result, ensure_ascii=False)})
                    return render(request, 'curd/popup_response.html',{'result': json.dumps(result, ensure_ascii=False)})
                else:
                    return redirect(self.get_list_url())
            return render(request, 'curd/add_view.html', {'form': form, 'config':self})

    def change_view(self,request,nid):
        """
        基于ModelForm的修改方法
        """
        obj = self.model_class.objects.filter(pk=nid).first()
        if not obj:
            return redirect(self.get_list_url())

        TestModelForm = self.get_model_form_class()
        if request.method == 'GET':  # 进入修改页面，显示所选记录的初始值
            form = TestModelForm(instance=obj)
            return render(request, 'curd/change_view.html', {'form': form,'config':self})
        else:  # 确认修改
            form = TestModelForm(instance=obj,data=request.POST)

            if form.is_valid():
                form.save()
                list_query_str = request.GET.get(self._query_param_key)
                list_url = '%s?%s'%(self.get_list_url(),list_query_str)
                return redirect(list_url)
            else:
                return render(request, 'curd/change_view.html', {'form': form})


    def delete_view(self,request,nid):
        """
        根据指定ID删除记录
        """
        self.model_class.objects.filter(pk=nid).delete()
        return redirect(self.get_list_url())


class CurdSite(object):
    """
    是一个容器，用于放置处理请求对应关系
    self._registry = {
        models.UserInfo: UserInfoConfig(models.UserInfo,self),
        models.UserType: StarkConfig(models.UserType,self),
        models.Role: StarkConfig(models.UserType,self),
    }
    """
    def __init__(self):
        self._registry = {}

    def register(self,model_class,config_class=None):
        if not config_class:
            config_class = CurdConfig
        self._registry[model_class] = config_class(model_class,self)


    def get_urls(self):
        """
        在urls.py中被调用，返回（应用+模块）与（url）的对应关系
        :return:
        """
        url_patterns = []
        for model_class,config_obj in self._registry.items():
            # 为每一个类，创建4个URL
            app_name = model_class._meta.app_label
            model_name = model_class._meta.model_name
            curd_url = url(r'^%s/%s/'%(app_name,model_name),(config_obj.urls,None,None))
            url_patterns.append(curd_url)
        return url_patterns

    @property
    def urls(self):
        return self.get_urls(), None, 'curd'

site = CurdSite()
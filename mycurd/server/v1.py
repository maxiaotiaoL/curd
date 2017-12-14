from django.conf.urls import url,include
from django.shortcuts import HttpResponse,render


class CurdConfig(object):
    list_display = []
    def __init__(self,model_class,site_obj):
        self.model_class = model_class
        self.site_obj = site_obj

    @property
    def urls(self):
        return self.get_urls()

    def get_urls(self):
        app_model_name = (self.model_class._meta.app_label, self.model_class._meta.model_name)
        url_patterns = [
            url(r'^$', self.changelist_view, name="%s_%s_changelist" % app_model_name),
            url(r'^add/$', self.add_view, name="%s_%s_add" % app_model_name),
            url(r'^(\d+)/change/$', self.change_view, name="%s_%s_change" % app_model_name),
            url(r'^(\d+)/delete/$', self.delete_view, name="%s_%s_delete" % app_model_name),
        ]
        return url_patterns

    def changelist_view(self,request,*args,**kwargs):

        # if not self.list_display:
        #     print(self.model_class._meta.__dict__)
        #     self.list_display = [self.model_class._meta.local_fields[0].verbose_name.lower(),]
        head_list = []
        if self.list_display:
            for field_name in self.list_display:
                if isinstance(field_name, str):
                    # 根据类和字段名称，获取字段对象的verbose_name
                    verbose_name = self.model_class._meta.get_field(field_name).verbose_name
                else:
                    verbose_name = field_name(self, None, True)
                head_list.append(verbose_name)
        else:
            head_list.append(self.model_class._meta.model_name)

        data_list = self.model_class.objects.all()

        def get_new_data():
            for row in data_list:
                temp = []
                if self.list_display:
                    for field_name in self.list_display:
                        if isinstance(field_name, str):
                            val = getattr(row, field_name)
                        else:
                            val = field_name(self, row)
                        temp.append(val)
                else:
                    temp.append(row)
                yield temp

        new_data_list = get_new_data()  #生成器
        print('=======',new_data_list)

        return render(request, 'changelist_view.html', {'data_list': new_data_list, 'head_list': head_list})

    def add_view(self, *args, **kwargs):
        return HttpResponse('add_view')

    def change_view(self, *args, **kwargs):
        return HttpResponse('add_view')

    def delete_view(self, *args, **kwargs):
        return HttpResponse('add_view')


class CurdSite(object):

    def __init__(self):
        self._registry = {}

    def register(self,model_class,config_class=None):
        if not config_class:
            config_class = CurdConfig
        self._registry[model_class] = config_class(model_class,self)


    def get_urls(self):
        url_patterns = []
        for model_class,config_obj in self._registry.items():
            app_name = model_class._meta.app_label
            model_name = model_class._meta.model_name
            curd_url = url(r'^%s/%s/'%(app_name,model_name),(config_obj.urls,None,None))
            url_patterns.append(curd_url)
        return url_patterns

    @property
    def urls(self):
        return self.get_urls(), None, 'curd'

site = CurdSite()
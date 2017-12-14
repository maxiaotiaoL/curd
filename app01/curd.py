from django.utils.safestring import mark_safe

print('in app01')
from mycurd.server import v1
from app01 import models

class UserInfoConfig(v1.CurdConfig):

    def edit(self,obj=None,is_header=False):
        if is_header:
            return '操作'
        return mark_safe("<a href='edit/%s'>编辑</a>"%obj.id)
    def checkbox(self,obj=None,is_header=False):
        if is_header:
            return '选择'
        return mark_safe("<input type='checkbox' name='pk' value='%s'>"%obj.id)

    list_display = [checkbox,'id','name',edit]

class RoleConfig(v1.CurdConfig):
    pass
    # list_display = ['id','caption']

v1.site.register(models.UserInfo,UserInfoConfig)
v1.site.register(models.Role,RoleConfig)
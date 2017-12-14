print('in app01')
from mycurd.server import v1
from app01 import models

v1.site.register(models.UserInfo)
v1.site.register(models.Role)
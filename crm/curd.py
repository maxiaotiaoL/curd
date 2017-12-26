from mycurd.server import v1
from crm import models

# 部门记录
from mycurd.configs.department import DepartmentConfig
v1.site.register(models.Department, DepartmentConfig)

# 用户记录
from mycurd.configs.userinfo import UserInfoConfig
v1.site.register(models.UserInfo, UserInfoConfig)

# 课程记录
from mycurd.configs.course import CourseConfig
v1.site.register(models.Course, CourseConfig)

# 学校记录
from mycurd.configs.school import SchoolConfig
v1.site.register(models.School, SchoolConfig)

# 班级记录
from mycurd.configs.classlist import ClassListConfig
v1.site.register(models.ClassList, ClassListConfig)

# 顾客记录
from mycurd.configs.customerrecord import CustomerConfig
v1.site.register(models.Customer, CustomerConfig)

# 客户跟进记录
from mycurd.configs.consultrecord import ConsultRecordConfig
v1.site.register(models.ConsultRecord, ConsultRecordConfig)

# 缴费记录
from mycurd.configs.paymentrecord import PaymentRecordConfig
v1.site.register(models.PaymentRecord, PaymentRecordConfig)

# 学生记录
from mycurd.configs.student import StudentConfig
v1.site.register(models.Student, StudentConfig)

# 老师上课记录记录
from mycurd.configs.courserecord import CourseRecordConfig
v1.site.register(models.CourseRecord, CourseRecordConfig)

# 学生学习记录
from mycurd.configs.studyrecord import StudyRecordConfig
v1.site.register(models.StudyRecord, StudyRecordConfig)




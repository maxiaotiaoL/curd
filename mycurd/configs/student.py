import json

from django.forms import ModelForm
from django.forms import widgets as wd
from django.http import QueryDict
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.conf.urls import url,include
from django.shortcuts import HttpResponse, redirect, render

from mycurd.server import v1
from crm import models



class StudentConfig(v1.CurdConfig):

    def class_list_display(self,obj=None,is_header=False):
        if is_header:
            return '已报班级'
        return ','.join(['%s(%s期)' % (cls.course.name,cls.semester) for cls in obj.class_list.all()])

    def score_view(self, request, sid):
        student_obj = models.Student.objects.get(pk=sid)
        if not student_obj:
            return HttpResponse('查无此人')
        class_list = student_obj.class_list.all()  # 学生所在班级列表
        return render(request, 'score_view.html', {'student_obj': student_obj, 'class_list': class_list})

    def get_scores(self, request, sid, cid):
        print(sid, cid)
        ret = {'status': False, 'msg': None, 'data': None}
        try:
            data = []
            record_list = models.StudyRecord.objects.filter(student_id=sid, course_record__class_obj_id=cid).order_by('course_record_id')
            for row in record_list:
                day = "day%s" % row.course_record.day_num
                data.append([day, row.score])
            ret['data'] = data
            ret['status'] = True
        except Exception as e:
            ret['msg'] = str(e)

        return HttpResponse(json.dumps(ret))


    def extra_url(self):
        app_model_name = (self.model_class._meta.app_label, self.model_class._meta.model_name)
        url_list = [
            url(r'^(?P<sid>\d+)/score_view/$', self.wrap(self.score_view), name="%s_%s_sv" % app_model_name),
            url(r'^(?P<sid>\d+)/(?P<cid>\d+)/get_scores/$', self.wrap(self.get_scores), name="%s_%s_get_scores" % app_model_name),
        ]
        return url_list

    def score_list(self,obj=None,is_header=False):
        if is_header:
            return '查看成绩'
        url = reverse("curd:crm_student_sv",args=(obj.pk,))
        return mark_safe('<a href="%s">点击查看</a>' % url)

    list_display = ['customer', class_list_display, score_list]

    edit_link = ['customer', ]
    show_add_btn = True
    show_search_form = True
    show_comb_filter = True
    comb_filter = [
        v1.FilterOption('class_list'),
    ]
from django.forms import ModelForm
from django.forms import widgets as wd
from django.http import QueryDict
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.conf.urls import url,include
from django.shortcuts import HttpResponse, redirect, render

from mycurd.server import v1
from crm import models


class CourseRecordConfig(v1.CurdConfig):
    def has_homework_display(self,obj=None,is_header=False):
        if is_header:
            return '是否作业'
        return '是' if obj.has_homework else '否'

    def kaoqin(self,obj=None,is_header=False):
        if is_header:
            return '考勤'
        return mark_safe("<a href='/curd/crm/studyrecord/?course_record=%s'>考勤管理</a>"%(obj.id))

    def display_score_list(self,obj=None,is_header=False):
        if is_header:
            return '成绩录入'
        url = reverse("curd:crm_courserecord_score_list",args=(obj.pk,))
        return mark_safe("<a href='%s'>成绩录入</a>"%(url))

    list_display = ['course_title','date','teacher',has_homework_display,kaoqin,display_score_list]
    edit_link = ['course_title',]



    def extra_url(self):
        app_model_name = (self.model_class._meta.app_label, self.model_class._meta.model_name)
        url_list = [
            url(r'^(\d+)/score_list/$', self.wrap(self.score_list), name="%s_%s_score_list" % app_model_name),
        ]
        return url_list

    def score_list(self,request,record_id):
        """
        :param request:
        :param record_id:老师上课记录ID
        :return:
        """
        if request.method == "GET":
            from django.forms import Form
            from django.forms import fields
            from django.forms import widgets

            data = []
            study_record_list = models.StudyRecord.objects.filter(course_record_id=record_id)
            for obj in study_record_list:
                # obj是对象
                TempForm = type('TempForm', (Form,), {
                    'score_%s' % obj.pk: fields.ChoiceField(choices=models.StudyRecord.score_choices),
                    'homework_note_%s' % obj.pk: fields.CharField(widget=widgets.Textarea())
                })
                data.append({'obj': obj, 'form': TempForm(initial={'score_%s' % obj.pk: obj.score, 'homework_note_%s' % obj.pk:obj.homework_note})})
            return render(request, 'score_list.html', {'data': data})
        else:
            data_dict = {}
            for key, value in request.POST.items():
                if key == "csrfmiddlewaretoken":
                    continue
                name, nid = key.rsplit('_', 1)
                if nid in data_dict:
                    data_dict[nid][name] = value
                else:
                    data_dict[nid] = {name: value}

            for nid, update_dict in data_dict.items():
                models.StudyRecord.objects.filter(id=nid).update(**update_dict)
            return HttpResponse('....')

    show_add_btn = True
    show_search_form = True

    show_comb_filter = True
    comb_filter = [
        v1.FilterOption('class_obj'),
    ]

    def multi_init(self,request):
        """
        上课记录批量初始化
        :param request:
        :return:
        """
        pk_list = request.POST.getlist('pk')
        record_list = self.model_class.objects.filter(pk__in=pk_list)
        StudyRecords = []
        for record in record_list:
            exists = models.StudyRecord.objects.filter(class_list=record.class_obj).exists()
            if exists:  # 查看班级记录是否存在
                continue
            student_list = models.Student.objects.filter(class_list=record.class_obj)  # 这个班的所有学生
            for student in student_list:
                StudyRecords.append(models.StudyRecord(course_record=record,student=student,))  # 为班里的每个学生创建学习记录
        models.StudyRecord.objects.bulk_create(StudyRecords)


    multi_init.short_desc ="批量初始化"

    show_action_list = True
    action_list = [multi_init,]
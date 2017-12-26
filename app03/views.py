from django.http import QueryDict
from django.shortcuts import render,HttpResponse,redirect

# Create your views here.
from django.utils.safestring import mark_safe

STU_LIST = []
for i in range(1,105):
    STU_LIST.append('stu_'+str(i))


def hosts_ys(request):
    stu_list = STU_LIST
    total_count = len(STU_LIST)
    per_page = 5
    current_page = int(request.GET.get('page',1))

    start = (int(current_page) - 1) * per_page
    end = int(current_page) * per_page
    stu_list = stu_list[start:end]


    page_num = divmod(total_count,per_page)
    max_page = page_num[0]
    if page_num[1]:
        max_page += 1

    page_count = 11  # 默认显示11个页码
    half = int((page_count - 1) / 2)



    if max_page <= page_count:
        page_start,page_end = 1,max_page
    else:
        if current_page <= half:
            page_start,page_end = 1,page_count
        elif current_page + half >= max_page:
            page_start, page_end = max_page-per_page+1, max_page

    print(current_page, page_start, page_end)

    page_html_list = []

    for i in range(page_start,page_end+1):
        xx = mark_safe("<a href='/hosts/?page=%s'>%s</a>"%(i,i))
        page_html_list.append(xx)



    # page_html_list = page_html_list[page_start,page_end]

    namedict = {
        'stu_list':stu_list,
        'page_html_list':page_html_list,
    }
    return render(request,'student.html',namedict)


HOST_LIST = []
for i in range(1,296):
    HOST_LIST.append('host_'+str(i)+'.com')

from pager import pager
def hosts(request):
    pager_obj = pager.Pagination(request.GET.get('page',1),len(HOST_LIST),request.path_info)
    host_list = HOST_LIST[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()


    namedict = {
        'host_list':host_list,
        'html':html,
    }
    return render(request, 'hosts.html', namedict)


USER_LIST = []
for i in range(1,377):
    USER_LIST.append('user_'+str(i))

def users(request):
    pager_obj = pager.Pagination(request.GET.get('page',1),len(USER_LIST),request.path_info)
    user_list = USER_LIST[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()

    namedict = {
        'user_list':user_list,
        'html':html,
    }
    QueryDict
    return render(request, 'users.html', namedict)
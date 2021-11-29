from django.http import JsonResponse, HttpResponse
from django.views.generic import View
from app.RoleMethod import get_school
# from openpyxl import load_workbook
from django.db.models import Q
from app.models import *


class SynchronizeSchool(View):
    """
    模块: 网络爬取全国学校信息
    接口信息:
        GET:
            None
        POST:
            None
    返回信息:
        GET:
            status: 事件操作状态
            info: 提示信息
            data: 爬取到的数据
        POST:
            None
    """

    def get(self, request):
        return JsonResponse({'status': True, 'info': '地址信息爬取成功', 'data': get_school.synchronize_school()})

    def post(self, request):
        pass


class GetSchool(View):
    """
    模块: 学校信息
    接口信息:
        GET:
            municipality_id: 城市编号
        POST:
            school_id: 学校统一编号
            school_name: 学校名
            school_describe: 学校介绍
            school_municipality: 学校所在城市编号
            school_department: 主管部门
            school_rank: 办学层次
            school_remark: 学校备注
    返回信息:
        GET:
            status: 数据请求状态
            data: 请求到的数据
        POST:
            status: 数据修改状态
            info: 提示信息
    """

    def get(self, request):
        page = request.GET.get('page')
        total = request.GET.get('total')
        text = request.GET.get('text')
        municipality_id = request.GET.get('municipality_id')
        print(page, total, text, municipality_id)
        municipality_list = dict()
        municipality = Municipality.objects.all()
        for municipality_child in municipality:
            municipality_list[municipality_child.municipality_id] = municipality_child.municipality_name
        school = School.objects.all()
        if municipality_id:
            school = school.filter(school_municipality=municipality_id)
        if text:
            school = school.filter(Q(school_name__contains=text))
        school_num = school.count()
        if total != '0':
            school = school[(int(page) - 1) * int(total): int(page) * int(total)]
        school_list = []
        for school_child in school:
            school_list.append({
                'school_id': school_child.school_id,
                'school_name': school_child.school_name,
                'school_describe': school_child.school_describe,
                'school_department': school_child.school_department,
                'school_municipality': {'municipality_id': school_child.school_municipality,
                                        'municipality_name':  municipality_list[school_child.school_municipality]},
                'school_rank': school_child.school_rank,
                'school_remark': school_child.school_remark,
            })
        return JsonResponse({'status': True, 'message': school_list, 'total': school_num})

    def post(self, request):
        school_id = request.POST.get('school_id')
        school_name = request.POST.get('school_name')
        school_describe = request.POST.get('school_describe')
        school_municipality = request.POST.get('school_municipality')
        school_department = request.POST.get('school_department')
        school_rank = request.POST.get('school_rank')
        school_remark = request.POST.get('school_remark')
        obj = School.objects.filter(school_id=school_id)
        if not obj.exists():
            obj1 = School.objects.filter(school_name=school_name)
            if obj1.exists():
                message = {'status': False, 'info': '后台已拥有此学校信息'}
            else:
                School.objects.create(
                    school_id=school_id,
                    school_name=school_name,
                    school_department=school_department,
                    school_describe=school_describe,
                    school_municipality=school_municipality,
                    school_rank=school_rank,
                    school_remark=school_remark
                )
                message = {'status': True, 'info': '学校信息添加成功'}
        else:
            school_new_name = obj.first().school_name
            message = {'status': False, 'info': f'当前编号下已有学校{school_new_name}, 请输入正确的学校统一编号'}
        return JsonResponse(message)

# class PutSchool(View):
#     def get(self,request):
#         wb = load_workbook('D:/xiazai/address_bak.xlsx')
#         ws = wb['municipality']
#         cList = ws['C'][1:]
#         aList = ws['A'][1:]
#         school_list = []
#         municipality_list = dict()
#         for it in cList:
#             a = it.value
#             b, c = a.split('/')
#             e, f = c.split('.')
#             school_list.append(e)
#
#         g = 0
#         for it in aList:
#             municipality_list[school_list[g]] = it.value
#             municipality_list[it.value] = it.value
#             g += 1
#
#         schools = School.objects.all()
#
#         for school in schools:
#             school.school_municipality = municipality_list[school.school_municipality]
#             school.save()


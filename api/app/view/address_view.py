from django.http import JsonResponse, HttpResponse
from django.views.generic import View
from app.RoleMethod import get_city
from app.models import *


class SynchronizeAddress(View):
    """
    模块: 网络爬取全国地址信息
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
        return JsonResponse({'status': True, 'info': '地址信息爬取成功', 'data': get_city.synchronize_address()})

    def post(self, request):
        pass


class GetProvince(View):
    """
    模块: 省份信息
    接口信息:
        GET:
            None
        POST:
            province_id: 省份编号
            province_name: 省份名
    返回信息:
        GET:
            status: 事件操作状态
            data: 省份相关信息
        POST:
            status: 事件操作状态
            info: 事件操作提示
    """

    def get(self, request):
        obj = Province.objects.all().values()
        return JsonResponse({'status': True, 'data': list(obj)})

    def post(self, request):
        province_id = request.POST.get('province_id')
        province_name = request.POST.get('province_name')
        obj1 = Province.objects.filter(province_id=province_id)
        if obj1.exists():
            message = {'status': False, 'info': '此编号已被其它省份使用'}
        else:
            obj2 = Province.objects.filter(province_name=province_name)
            if obj2.exists():
                message = {'status': False, 'info': '此省份信息已添加'}
            else:
                Province.objects.create(
                    province_id=province_id,
                    province_name=province_name
                )
                message = {'status': True, 'info': '省份信息添加成功'}
        return JsonResponse(message)


class GetMunicipality(View):
    """
    模块: 城市信息
    接口信息:
        GET:
            province_id: 省份编号
        POST:
            province_id: 省份编号
            municipality_id: 城市编号
            municipality_name: 城市名
    返回信息:
        GET:
            status: 事件操作状态
            data: 城市相关信息
        POST:
            status: 事件操作状态
            info: 事件操作提示
    """
    def get(self, request):
        municipalities = Municipality.objects.all()
        provinces = Province.objects.all()
        children = dict()
        for province in provinces:
            children[province.province_id] = province.province_name
        municipality_list = []
        for municipality in municipalities:
            municipality_list.append({
                'municipality_id': municipality.municipality_id,
                'municipality_name': municipality.municipality_name,
                'municipality_province': {
                    'id': municipality.municipality_province,
                    'name': children[municipality.municipality_province]
                }
            })
        return JsonResponse({'status': True, 'data': municipality_list})

    def post(self, request):
        province_id = request.POST.get('province_id')
        municipality_id = request.POST.get('municipality_id')
        municipality_name = request.POST.get('municipality_name')
        obj = Province.objects.filter(province_id=province_id)
        if obj.exists():
            obj1 = Municipality.objects.filter(municipality_id=municipality_id)
            if obj1.exists():
                message = {'status': False, 'info': '此编号已被其它城市使用'}
            else:
                obj2 = Municipality.objects.filter(municipality_name=municipality_name)
                if obj2.exists():
                    message = {'status': False, 'info': '此城市信息已添加'}
                else:
                    Municipality.objects.create(
                        municipality_id=municipality_id,
                        municipality_name=municipality_name,
                        municipality_province=province_id
                    )
                    message = {'status': True, 'info': '城市信息添加成功'}
        else:
            message = {'status': False, 'info': '请先选择省份'}
        return JsonResponse(message)


class GetAddressList(View):
    """
        模块: 城市信息
        接口信息:
            GET:
                None
        返回信息:
            GET:
                 status: 事件操作状态
                data: 城市相关信息
        """
    def get(self, request):
        data = []
        provinces = Province.objects.all()
        municipalities = Municipality.objects.all()
        children = dict()
        for province in provinces:
            children[province.province_id] = []
        for municipality in municipalities:
            municipality_list = children[municipality.municipality_province]
            municipality_list.append({
                'id': municipality.municipality_id,
                'name': municipality.municipality_name
            })
            children[municipality.municipality_province] = municipality_list
        for province in provinces:
            data.append({
                'id': province.province_id,
                'name': province.province_name,
                'children': children[province.province_id]
            })
        message = {'status': True, 'data': data}
        return JsonResponse(message)


class GetAddressMessage(View):
    """
    模块：查询地区信息
    接口信息：
        GET：
        省：province,市：municipality,区/县：district,乡/镇：township,村：village
    """
    def get(self, request):
        father = request.GET.get('father')
        father_id = request.GET.get('father_id')
        child = request.GET.get('child')
        address_num = 0
        address_list = []
        if child == 'province':
            province = Province.objects.all()
            address_num = province.count()
            for item in province:
                address_list.append({
                    'id': item.province_id,
                    'name': item.province_name,
                    'deep': 1,
                })
        elif child == 'municipality':
            municipality = Municipality.objects.filter(municipality_province=father_id)
            address_num = municipality.count()
            for item in municipality:
                address_list.append({
                    'id': item.municipality_id,
                    'name': item.municipality_name,
                    'deep': 2,
                })
        elif child == 'district':
            if father == 'province':
                district = District.objects.filter(district_province=father_id)
            elif father == 'municipality':
                district = District.objects.filter(district_municipality=father_id)
            else:
                district = District.objects.all()
            address_num = district.count()
            for item in district:
                address_list.append({
                    'id': item.district_id,
                    'name': item.district_name,
                    'deep': 3,
                })
        elif child == 'township':
            if father == 'province':
                township = Township.objects.filter(township_province=father_id)
            elif father == 'municipality':
                township = Township.objects.filter(township_municipality=father_id)
            elif father == 'district':
                township = Township.objects.filter(township_area=father_id)
            else:
                township = Township.objects.all()
            address_num = township.count()
            for item in township:
                address_list.append({
                    'id': item.township_id,
                    'name': item.township_name,
                    'deep': 4,
                })
        elif child == 'village':
            if father == 'province':
                village = Village.objects.filter(village_province=father_id)
            elif father == 'municipality':
                village = Village.objects.filter(village_municipality=father_id)
            elif father == 'district':
                village = Village.objects.filter(village_area=father_id)
            elif father == 'township':
                village = Village.objects.filter(village_township=father_id)
            else:
                village = Village.objects.all()
            address_num = village.count()
            for item in village:
                address_list.append({
                    'id': item.village_id,
                    'name': item.village_name,
                    'deep': 5,
                })
        return JsonResponse({'status': True, 'message': address_list, 'total': address_num})




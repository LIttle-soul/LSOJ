import bs4
import requests
from app.models import Province, Municipality, School
from django.db.models import Q


def get_province_list():
    response = requests.get('https://daxue.eol.cn/mingdan.shtml')
    response.encoding = 'utf-8'
    demo = response.text
    soup = bs4.BeautifulSoup(demo, "html.parser")
    soup = soup.find_all(name='div', attrs={"class": "province"})
    soup = [{'province': data.a.text, 'url': data.a['href']} for data in soup]
    return soup


def get_school_list(url='https://daxue.eol.cn/js.shtml', province_name='江苏'):
    response = requests.get(url)
    response.encoding = 'utf-8'
    demo = response.text
    soup = bs4.BeautifulSoup(demo, "html.parser")
    soup = soup.find(name='div', attrs={'class': 'tablebox'}).tbody.find_all(name='tr')
    # print(soup)
    province_id = Province.objects.filter(province_name__startswith=province_name).first().province_id
    # print(province_id)
    for data in soup[2:]:
        # print(data)
        data_list = data.find_all('td')
        school_name = data_list[1].text.strip()
        school_id = data_list[2].text
        school_department = data_list[3].text
        school_municipality = data_list[4].text.strip()
        school_rank = data_list[5].text
        school_remark = data_list[6].text if school_id != '4145010593' else ''
        if school_municipality not in ['天津市', '咸阳市']:
            if not Municipality.objects.filter(Q(municipality_name__contains=school_municipality)).exists():
                continue
            municipality_id = Municipality.objects.filter(Q(municipality_province=province_id) & Q(municipality_name__contains=school_municipality)).first().municipality_id
        else:
            municipality_id = Municipality.objects.filter(Q(municipality_name__contains=school_municipality)).first().municipality_id
        print(f'{province_id}\t{municipality_id}\t{school_id}\t{school_name}\t{school_department}\t{school_municipality}\t{school_rank}\t{school_remark}')
        # School.objects.create(
        #     school_id=school_id,
        #     school_name=school_name,
        #     school_rank=school_rank,
        #     school_remark=school_remark,
        #     school_department=school_department,
        #     school_municipality=municipality_id
        # )


def synchronize_school():
    province_list = get_province_list()
    for province in province_list:
        province_name = province.get('province')
        get_school_list(province.get('url'), province_name)
    return '学校爬取完成'

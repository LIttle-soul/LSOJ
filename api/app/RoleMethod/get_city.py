import bs4
import requests
from app.models import Province, Municipality


def fetch_city_list(url):
    response = requests.get(f"http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/{url}")
    response.encoding = "gbk"
    demo = response.text
    soup = bs4.BeautifulSoup(demo, "html.parser")
    soup = soup.body.find_all('tbody')[-1].tr.find_all('tr')[1:]
    soup = [{'name': data.find_all('td')[-1].a.text, 'url': data.find_all('td')[-1].a['href']} for data in soup]
    return soup


def fetch_province_list():
    response = requests.get("http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/index.html")
    response.encoding = "gbk"
    demo = response.text
    soup = bs4.BeautifulSoup(demo, "html.parser")
    soup = soup.body.find_all('tbody')[-1].find_all('td')[4:-1]
    soup = [{'name': data.a.text, 'url': data.a['href']} for data in soup]
    return soup


def synchronize_address():
    province_list = fetch_province_list()
    all_data = []
    for province in province_list:
        province_id = province.get('url')[:2]
        province_name = province.get('name')
        # print(f' province_id: {province_id}\t province_name: {province_name}')
        # Province.objects.create(
        #     province_id=province_id,
        #     province_name=province_name
        # )
        province_data = {
            'province_id': province_id,
            'province_name': province_name,
            'province_child': []
        }
        if province_name not in ['北京市', '天津市', '上海市', '重庆市']:
            municipality_list = fetch_city_list(province.get('url'))
            for municipality in municipality_list:
                municipality_id = municipality.get('url')[3:7]
                municipality_name = municipality.get('name')
                # Municipality.objects.create(
                #     municipality_id=municipality_id,
                #     municipality_name=municipality_name,
                #     municipality_province=province_id
                # )
                municipality_data = {'municipality_id': municipality_id, 'municipality_name': municipality_name}
                province_data['province_child'].append(municipality_data)
                print(f' municipality_id: {municipality_id}\t municipality_name: {municipality_name}\t municipality_province: {province_id}')
        else:
            municipality_id = int(province_id + '01')
            municipality_name = province_name
            # Municipality.objects.create(
            #     municipality_id=municipality_id,
            #     municipality_name=municipality_name,
            #     municipality_province=province_id
            # )
            municipality_data = {'municipality_id': municipality_id, 'municipality_name': municipality_name}
            province_data['province_child'].append(municipality_data)
            print(f'municipality_id: {municipality_id}\t municipality_name: {municipality_name}\t municipality_province: {province_id}')
        all_data.append(province_data)
    return all_data

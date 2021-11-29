import bs4
import requests
# from app.models import Province, Municipality


# 获取一级区域
def fetch_province_list(url):
    response = requests.get(f"http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/{url}")
    response.encoding = "gbk"
    demo = response.text
    soup = bs4.BeautifulSoup(demo, "html.parser")
    soup = soup.body.find_all('tbody')[-1].find_all('td')[4:-1]
    soup = [{'name': data.a.text, 'url': data.a['href']} for data in soup]
    return soup


# 获取二三四级区域
def fetch_district_list(url):
    response = requests.get(f"http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/{url}")
    response.encoding = "gbk"
    demo = response.text
    soup = bs4.BeautifulSoup(demo, "html.parser")
    soup = soup.body.find_all('tbody')[-1].tr.find_all('tr')[1:]
    data = []
    for item in soup:
        if item.find_all('td')[-1].a:
            data.append({'id': item.find_all('td')[0].a.text, 'name': item.find_all('td')[-1].a.text, 'url': item.find_all('td')[-1].a['href']})
    # [print(item) for item in data]
    return data

# 获取五级区域
def fetch_village_list(url):
    response = requests.get(f"http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/{url}")
    response.encoding = "gbk"
    demo = response.text
    soup = bs4.BeautifulSoup(demo, "html.parser")
    soup = soup.body.find_all('tbody')[-1].tr.find_all('tr')[1:]
    data = []
    for item in soup:
        village = item.find_all('td')
        data.append({'id': village[0].text, 'city_id': village[1].text, 'name': village[2].text})
    # [print(item) for item in data]
    return data

# def synchronize_address():
#     province_list = fetch_province_list()
#     all_data = []
#     for province in province_list:
#         province_id = province.get('url')[:2]
#         province_name = province.get('name')
#         # print(f' province_id: {province_id}\t province_name: {province_name}')
#         # Province.objects.create(
#         #     province_id=province_id,
#         #     province_name=province_name
#         # )
#         province_data = {
#             'province_id': province_id,
#             'province_name': province_name,
#             'province_child': []
#         }
#         if province_name not in ['北京市', '天津市', '上海市', '重庆市']:
#             municipality_list = fetch_city_list(province.get('url'))
#             for municipality in municipality_list:
#                 municipality_id = municipality.get('url')[3:7]
#                 municipality_name = municipality.get('name')
#                 # Municipality.objects.create(
#                 #     municipality_id=municipality_id,
#                 #     municipality_name=municipality_name,
#                 #     municipality_province=province_id
#                 # )
#                 municipality_data = {'municipality_id': municipality_id, 'municipality_name': municipality_name}
#                 province_data['province_child'].append(municipality_data)
#                 print(f' municipality_id: {municipality_id}\t municipality_name: {municipality_name}\t municipality_province: {province_id}')
#         else:
#             municipality_id = int(province_id + '01')
#             municipality_name = province_name
#             # Municipality.objects.create(
#             #     municipality_id=municipality_id,
#             #     municipality_name=municipality_name,
#             #     municipality_province=province_id
#             # )
#             municipality_data = {'municipality_id': municipality_id, 'municipality_name': municipality_name}
#             province_data['province_child'].append(municipality_data)
#             print(f'municipality_id: {municipality_id}\t municipality_name: {municipality_name}\t municipality_province: {province_id}')
#         all_data.append(province_data)
#     return all_data

def get_data(url, deep):
    if deep == 5:
        return
    elif deep == 1:
        temp_data = fetch_province_list(url=url)
        for item in temp_data:
            get_data()

if __name__ == '__main__':
    get_data("index.html", deep=1)

import urllib.request
import urllib.parse
import re
from bs4 import BeautifulSoup
# from fake_useragent import UserAgent
import json
import os
from pathlib import Path
import threading

# 创建文件夹
def make_dir(name):
    os.mkdir(name)

# 创建历史数据的文件
def make_all_dir(city_dict_data):
    for province in city_dict_data.keys():
        if Path("./history_data/"+province).exists():
            pass
        else:
            make_dir("./history_data/"+province)
        for city in city_dict_data[province]:
            if Path("./history_data/"+province+"/"+city).exists():
                pass
            else:
                make_dir("./history_data/"+province+"/"+city)

# 将数据写入txt文件
def write_data(name,data):
    with open(name,mode="w",encoding="utf-8") as fp:
        fp.write(json.dumps(data))

# 读取数据为字典
def read_data(name):
    with open(name,mode="r",encoding="utf-8") as fp:
        js = fp.read()
        dic = json.loads(js)
    print(dic)
    # print(dic['2021-02-01'][0])

# 根据地址，请求网页
def get_url(url,decode='GBK'):
    # ua = UserAgent()
    # head = {"User-Agent": str(ua.chrome)}   # 模拟浏览器，添加头
    try:
        # request = urllib.request.Request(url=url, headers=head)#请求网页
        request = urllib.request.Request(url=url)  # 请求网页
        fp = urllib.request.urlopen(request)
        html = fp.read().decode(decode)     # 读取网页内容并进行解码
        return html
    except Exception as e:
        print("获取网页内容失败！")
        return None

# 获取 省份:{城市:地址}并返回
def get_city():
    url = "http://www.tianqihoubao.com/aqi/"
    try:
        html = get_url(url)
    except:
        print("错误")
        return
    soup = BeautifulSoup(html,'html.parser')                                    # BeautifulSoup解析
    city_all = soup.find(name="div",attrs={'class':"citychk"})                  # 匹配第一个<div class=all>
    province = city_all.find_all(name="dl")
    str_clear = re.compile(r'\S+')                                              # 只保留字符串
    all_dict = {}
    for p in province:
        p_name = p.find(name="dt").text                                         # 获取省份名
        p_cities = p.find(name="dd")
        p_cities = p_cities.find_all(name="a")                                  # 获取该省份的所有城市
        cities_dict = {}
        for city in p_cities:                                                   # 查看该省份的所有城市
            cities_dict[str_clear.findall(city.text)[0]] = city['href']         # 以城市名为键，地址为值
        all_dict[p_name] = cities_dict                                          # 以省份名为键，{城市名:地址}为值
    print("all_dict:",all_dict)
    return all_dict

# 根据该城市的地址，获取该城市拥有哪些月份的数据，并返回
def city_histroy(city_name, city_dict_data):
    base_url = "http://www.tianqihoubao.com"
    print("city_dict_data:",city_dict_data)
    input()
    for key,value in city_dict_data.items():
        if city_name in value.keys():
            base_url += city_dict_data[key][city_name]
            break
    try:
        html = get_url(base_url)
    except:
        print("错误")
        return
    soup = BeautifulSoup(html,'html.parser')

    project_title = soup.find(name='div',attrs={'class':"box p"})
    histroy_cname = project_title.find(name='h2').text              # 获取城市名
    histroy_month = project_title.find_all("li")
    histroy_info = {}
    str_clear = re.compile(r'\S+')
    for h_m in histroy_month:
        h_m_time = str_clear.findall(h_m.text)                      # 时间为键
        h_m_href = h_m.a['href']                                    # 网页地址为值
        histroy_info[h_m_time[0]] = h_m_href

    print(histroy_info)
    return histroy_info

# 获取该月（网页）的数据
def get_month_data(soup):
    project_body = soup.find(name='div', attrs={'class': 'api_month_list'})
    project_body = project_body.find_all(name="tr")
    project_title = project_body[0]                     # 标签行
    project_detail = project_body[1:]                   # 各行数据
    str_clear = re.compile(r'\S+')                      # 只保留字符串
    title_dict = [str_clear.findall(i.text)[0] for i in project_title.find_all(name='td')]  # 获取详细的标签值
    detail_dict = {}                                    # 建立每日时间的字典
    for detail in project_detail:
        h_time = str_clear.findall(detail.find(name='td').text)[0]                                  # 以时间作为键
        detail_dict[h_time] = [str_clear.findall(i.text)[0] for i in detail.find_all(name='td')]    # 该行数据作为值

    return_dict = {}
    return_dict['title'] = title_dict
    return_dict['data'] = detail_dict
    print(return_dict)
    return return_dict              # 返回得到的数据

# 可调整下载的月份
# 下载该省份中，所有城市，所有月份的数据
def down_data(city_dict_data):                          # 下载数据
    print("city_dict_data:",city_dict_data)
    for province in city_dict_data.keys():              # 遍历每一个省份
        for city in city_dict_data[province].keys():    # 获取每个省份里的每个城市
            city_histroy_info = city_histroy(city,city_dict_data)   # 利用该城市在省份列表中的地址，获取该城市页面
            # print(city_histroy_info)        # {'时间':'地址'}   {'2021年06月': '/aqi/beijing-202106.html', '2021年05月': '/aqi/beijing-202105.html'}
            city_list = list(city_histroy_info.keys())

            ### 修改此处调整下载的月份数据
            city_list = city_list[0:42]      # 获取前42个月的数据
            # 注意注意，因为每个月更新，可能随着新加的月份增加，空白的月份时间会越多（网站可能没有更新），自己需要手动调节切片范围，
            # 把前面几个月份的切掉。

            for tim in city_list:            # 分别获取该城市每个月的地址，并获取该月份的数据
                base_url = "http://www.tianqihoubao.com"
                base_url += city_histroy_info[tim]
                filename = "./history_data/" + province + "/" + city + "/" + tim + ".txt"
                if Path(filename).exists():
                    continue
                try:
                    html = get_url(base_url)
                    soup = BeautifulSoup(html, 'html.parser')  # 解析网页信息
                except:
                    print("解析网页错误")
                data = get_month_data(soup)                 # 获取该网页中的数据
                print("下载完成",filename)
                write_data(filename,data)                   # 下载数据保存到文件中

# 可调整下载的城市
# 获取所有省份，所城市，所有月份的数据
def Histroy_time():
    city_dict_data = get_city()         # {省份:{城市:地址}}  {'热门城市': {'北京': '/aqi/beijing.html', '天津': '/aqi/tianjin.html'}}
    hot_city = ['北京','上海','天津','重庆']        # 只保留这几个热门城市，# 直辖市是在热门城市中的，热门城市中只保留直辖市，去掉其它的
    all_hot_city = list(city_dict_data['热门城市'].keys())
    for c in all_hot_city:     # 获取所有热门城市
        if c not in hot_city:
            city_dict_data['热门城市'].pop(c)       # 不在需要的热门城市列表中，则去除它

    ###  修改此处调整需要保留的省份
    remain_province = ['湖北','广东']
    remain_city = ['武汉','广州']
    ### 修改此处调整需要保留的省份
    remain_city_dict_data = {}
    for p in remain_province:
        temp_remain = {}
        for key,value in city_dict_data[p].items():
            if key in remain_city:
                temp_remain[key] = value
        remain_city_dict_data[p] = temp_remain
    city_dict_data = remain_city_dict_data

    print(city_dict_data)
    input()
    make_all_dir(city_dict_data)                  # 第一次需要建立对应的文件夹
    provinces = city_dict_data.keys()   # 获取省份列表
    thread_list = []
    for p in provinces:                 # 每一个省份建立一个线程，该线程下载该省份的所有数据
        thread_list.append(threading.Thread(target=down_data,args=({p:city_dict_data[p]},)))
    for t in thread_list:               # 多线程启动
        t.start()

# 下载历史数据
Histroy_time()
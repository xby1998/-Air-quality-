import urllib.request
import urllib.parse
import re
from bs4 import BeautifulSoup
# from fake_useragent import UserAgent    # 这个库可能会有问题，
import json
from pathlib import Path
from base_fun import get_now_time       # 自己写的，获取当前的时间

city_dict = {'热门城市': {'北京': '/aqi/beijing.html', '天津': '/aqi/tianjin.html', '上海': '/aqi/shanghai.html', '重庆': '/aqi/chongqing.html'},
             '河北': {'石家庄': '/aqi/shijiazhuang.html', '唐山': '/aqi/tangshan.html', '秦皇岛': '/aqi/qinhuangdao.html', '保定': '/aqi/baoding.html', '张家口': '/aqi/zhangjiakou.html', '邯郸': '/aqi/handan.html', '邢台': '/aqi/xingtai.html', '承德': '/aqi/chengde.html', '沧州': '/aqi/cangzhou.html', '廊坊': '/aqi/langfang.html', '衡水': '/aqi/hengshui.html'},
             '山西': {'太原': '/aqi/taiyuan.html', '大同': '/aqi/datong.html', '阳泉': '/aqi/yangquan.html', '长治': '/aqi/changzhi.html', '临汾': '/aqi/linfen.html', '晋城': '/aqi/jincheng.html', '朔州': '/aqi/shuozhou.html', '运城': '/aqi/sxyuncheng.html', '忻州': '/aqi/xinzhou.html', '吕梁': '/aqi/lvliang.html', '晋中': '/aqi/jinzhong.html'},
             '内蒙古': {'呼和浩特': '/aqi/huhehaote.html', '包头': '/aqi/baotou.html', '鄂尔多斯': '/aqi/eerduosi.html', '乌海': '/aqi/wuhai.html', '赤峰': '/aqi/chifeng.html', '通辽': '/aqi/tongliao.html', '巴彦淖尔': '/aqi/bayannaoer.html', '兴安盟': '/aqi/xinganmeng.html', '阿拉善盟': '/aqi/alashanmeng.html', '呼伦贝尔': '/aqi/hulunbeier.html', '二连浩特': '/aqi/erlianhaote.html', '锡林郭勒': '/aqi/xilinguole.html'},
             '辽宁': {'沈阳': '/aqi/shenyang.html', '大连': '/aqi/dalian.html', '丹东': '/aqi/dandong.html', '营口': '/aqi/yingkou.html', '盘锦': '/aqi/panjin.html', '葫芦岛': '/aqi/huludao.html', '鞍山': '/aqi/anshan.html', '锦州': '/aqi/jinzhou.html', '本溪': '/aqi/benxi.html', '瓦房店': '/aqi/wafangdian.html', '抚顺': '/aqi/fushun.html', '辽阳': '/aqi/liaoyang.html', '阜新': '/aqi/fuxin.html', '朝阳': '/aqi/chaoyang.html', '铁岭': '/aqi/tieling.html'},
             '吉林': {'长春': '/aqi/changchun.html', '吉林': '/aqi/jilin.html', '四平': '/aqi/siping.html', '辽源': '/aqi/liaoyuan.html', '白山': '/aqi/baishan.html', '松原': '/aqi/songyuan.html', '白城': '/aqi/baicheng.html', '延边': '/aqi/yanbian.html', '通化': '/aqi/tonghua.html'},
             '黑龙江': {'哈尔滨': '/aqi/haerbin.html', '齐齐哈尔': '/aqi/qiqihaer.html', '鸡西': '/aqi/jixi.html', '鹤岗': '/aqi/hegang.html', '双鸭山': '/aqi/shuangyashan.html', '大庆': '/aqi/daqing.html', '佳木斯': '/aqi/jiamusi.html', '七台河': '/aqi/qitaihe.html', '牡丹江': '/aqi/mudanjiang.html', '黑河': '/aqi/heihe.html', '绥化': '/aqi/suihua.html', '大兴安岭': '/aqi/daxinganling.html', '伊春': '/aqi/yichun.html', '甘南': '/aqi/hljgannan.html'},
             '江苏': {'南京': '/aqi/nanjing.html', '无锡': '/aqi/wuxi.html', '徐州': '/aqi/xuzhou.html', '常州': '/aqi/changzhou.html', '苏州': '/aqi/suzhou.html', '南通': '/aqi/nantong.html', '连云港': '/aqi/lianyungang.html', '淮安': '/aqi/huaian.html', '盐城': '/aqi/yancheng.html', '扬州': '/aqi/yangzhou.html', '镇江': '/aqi/zhenjiang.html', '泰州': '/aqi/jstaizhou.html', '宿迁': '/aqi/suqian.html', '昆山': '/aqi/kunshan.html', '海门': '/aqi/haimen.html', '太仓': '/aqi/taicang.html', '江阴': '/aqi/jiangyin.html', '溧阳': '/aqi/liyang.html', '金坛': '/aqi/jintan.html', '宜兴': '/aqi/yixing.html', '句容': '/aqi/jurong.html', '常熟': '/aqi/changshu.html', '吴江': '/aqi/wujiang.html', '张家港': '/aqi/zhangjiagang.html'},
             '浙江': {'杭州': '/aqi/hangzhou.html', '宁波': '/aqi/ningbo.html', '温州': '/aqi/wenzhou.html', '嘉兴': '/aqi/jiaxing.html', '湖州': '/aqi/huzhou.html', '金华': '/aqi/jinhua.html', '衢州': '/aqi/quzhou.html', '舟山': '/aqi/zhoushan.html', '台州': '/aqi/taizhou.html', '丽水': '/aqi/lishui.html', '绍兴': '/aqi/shaoxing.html', '义乌': '/aqi/yiwu.html', '富阳': '/aqi/zjfuyang.html', '临安': '/aqi/linan.html'},
             '安徽': {'合肥': '/aqi/hefei.html', '芜湖': '/aqi/wuhu.html', '蚌埠': '/aqi/bangbu.html', '淮南': '/aqi/huainan.html', '马鞍山': '/aqi/maanshan.html', '淮北': '/aqi/huaibei.html', '铜陵': '/aqi/tongling.html', '安庆': '/aqi/anqing.html', '黄山': '/aqi/huangshan.html', '滁州': '/aqi/chuzhou.html', '阜阳': '/aqi/fuyang.html', '宿州': '/aqi/anhuisuzhou.html', '巢湖': '/aqi/chaohu.html', '六安': '/aqi/liuan.html', '亳州': '/aqi/bozhou.html', '池州': '/aqi/chizhou.html', '宣城': '/aqi/xuancheng.html'},
             '福建': {'福州': '/aqi/fujianfuzhou.html', '厦门': '/aqi/xiamen.html', '泉州': '/aqi/quanzhou.html', '莆田': '/aqi/putian.html', '三明': '/aqi/sanming.html', '漳州': '/aqi/zhangzhou.html', '南平': '/aqi/nanping.html', '龙岩': '/aqi/longyan.html', '宁德': '/aqi/ningde.html'},
             '江西': {'南昌': '/aqi/nanchang.html', '景德镇': '/aqi/jingdezhen.html', '萍乡': '/aqi/pingxiang.html', '新余': '/aqi/xinyu.html', '鹰潭': '/aqi/yingtan.html', '赣州': '/aqi/ganzhou.html', '宜春': '/aqi/jxyichun.html', '抚州': '/aqi/fuzhou.html', '九江': '/aqi/jiujiang.html', '上饶': '/aqi/shangrao.html', '吉安': '/aqi/jian.html'},
             '山东': {'济南': '/aqi/jinan.html', '青岛': '/aqi/qingdao.html', '淄博': '/aqi/zibo.html', '枣庄': '/aqi/zaozhuang.html', '东营': '/aqi/dongying.html', '烟台': '/aqi/yantai.html', '潍坊': '/aqi/weifang.html', '济宁': '/aqi/sdjining.html', '泰安': '/aqi/taian.html', '威海': '/aqi/weihai.html', '日照': '/aqi/rizhao.html', '莱芜': '/aqi/laiwu.html', '临沂': '/aqi/linyi.html', '德州': '/aqi/dezhou.html', '聊城': '/aqi/liaocheng.html', '滨州': '/aqi/binzhou.html', '菏泽': '/aqi/heze.html', '乳山': '/aqi/rushan.html', '荣成': '/aqi/sdrongcheng.html', '文登': '/aqi/wendeng.html', '章丘': '/aqi/zhangqiu.html', '平度': '/aqi/pingdu.html', '莱州': '/aqi/laizhou.html', '招远': '/aqi/sdzhaoyuan.html', '莱西': '/aqi/laixi.html', '胶州': '/aqi/jiaozhou.html', '蓬莱': '/aqi/penglai.html', '胶南': '/aqi/jiaonan.html', '寿光': '/aqi/shouguang.html', '即墨': '/aqi/jimo.html'},
             '河南': {'郑州': '/aqi/zhengzhou.html', '洛阳': '/aqi/lvyang.html', '平顶山': '/aqi/pingdingshan.html', '鹤壁': '/aqi/hebi.html', '焦作': '/aqi/jiaozuo.html', '漯河': '/aqi/luohe.html', '三门峡': '/aqi/sanmenxia.html', '南阳': '/aqi/nanyang.html', '商丘': '/aqi/shangqiu.html', '信阳': '/aqi/xinyang.html', '周口': '/aqi/zhoukou.html', '驻马店': '/aqi/zhumadian.html', '安阳': '/aqi/anyang.html', '开封': '/aqi/kaifeng.html', '濮阳': '/aqi/puyang.html', '许昌': '/aqi/xuchang.html', '新乡': '/aqi/xinxiang.html'},
             '湖北': {'武汉': '/aqi/wuhan.html', '十堰': '/aqi/shiyan.html', '宜昌': '/aqi/yichang.html', '鄂州': '/aqi/ezhou.html', '荆门': '/aqi/jingmen.html', '孝感': '/aqi/xiaogan.html', '黄冈': '/aqi/huanggang.html', '咸宁': '/aqi/xianning.html', '黄石': '/aqi/huangshi.html', '恩施': '/aqi/enshi.html', '襄阳': '/aqi/xiangyang.html', '随州': '/aqi/suizhou.html', '荆州': '/aqi/jingzhou.html'},
             '湖南': {'长沙': '/aqi/changsha.html', '株洲': '/aqi/zhuzhou.html', '湘潭': '/aqi/xiangtan.html', '常德': '/aqi/changde.html', '张家界': '/aqi/zhangjiajie.html', '益阳': '/aqi/yiyang.html', '郴州': '/aqi/chenzhou.html', '永州': '/aqi/yongzhou.html', '怀化': '/aqi/huaihua.html', '娄底': '/aqi/loudi.html', '邵阳': '/aqi/shaoyang.html', '岳阳': '/aqi/yueyang.html', '湘西': '/aqi/xiangxi.html', '衡阳': '/aqi/hengyang.html'},
             '广东': {'广州': '/aqi/guangzhou.html', '韶关': '/aqi/shaoguan.html', '深圳': '/aqi/shenzhen.html', '珠海': '/aqi/zhuhai.html', '汕头': '/aqi/shantou.html', '佛山': '/aqi/foshan.html', '江门': '/aqi/jiangmen.html', '肇庆': '/aqi/zhaoqing.html', '惠州': '/aqi/huizhou.html', '河源': '/aqi/heyuan.html', '清远': '/aqi/gdqingyuan.html', '东莞': '/aqi/dongguang.html', '中山': '/aqi/zhongshan.html', '湛江': '/aqi/zhanjiang.html', '茂名': '/aqi/maoming.html', '梅州': '/aqi/meizhou.html', '汕尾': '/aqi/shanwei.html', '阳江': '/aqi/yangjiang.html', '潮州': '/aqi/chaozhou.html', '揭阳': '/aqi/jieyang.html', '云浮': '/aqi/yunfu.html'},
             '广西': {'南宁': '/aqi/nanning.html', '柳州': '/aqi/liuzhou.html', '北海': '/aqi/beihai.html', '桂林': '/aqi/guilin.html', '梧州': '/aqi/wuzhou.html', '防城港': '/aqi/fangchenggang.html', '钦州': '/aqi/gxqinzhou.html', '贵港': '/aqi/guigang.html', '玉林': '/aqi/guangxiyulin.html', '百色': '/aqi/baise\r\n.html', '贺州': '/aqi/hezhou.html', '河池': '/aqi/hechi.html', '来宾': '/aqi/laibin.html', '崇左': '/aqi/chongzuo.html'}, '海南': {'海口': '/aqi/haikou.html', '三亚': '/aqi/sanya.html'},
             '四川': {'成都': '/aqi/chengdu.html', '自贡': '/aqi/zigong.html', '攀枝花': '/aqi/panzhihua.html', '泸州': '/aqi/luzhou.html', '德阳': '/aqi/deyang.html', '绵阳': '/aqi/mianyang.html', '广元': '/aqi/guangyuan.html', '遂宁': '/aqi/scsuining.html', '乐山': '/aqi/leshan.html', '南充': '/aqi/nanchong.html', '眉山': '/aqi/meishan.html', '达州': '/aqi/dazhou.html', '雅安': '/aqi/yaan.html', '巴中': '/aqi/bazhong.html', '资阳': '/aqi/ziyang.html', '甘孜': '/aqi/ganzi.html', '内江': '/aqi/neijiang.html', '宜宾': '/aqi/yibin.html', '广安': '/aqi/guangan.html', '阿坝': '/aqi/aba.html', '凉山': '/aqi/liangshan.html'},
             '贵州': {'贵阳': '/aqi/guiyang.html', '六盘水': '/aqi/liupanshui.html', '遵义': '/aqi/zunyi.html', '安顺': '/aqi/anshun.html', '毕节': '/aqi/bijie.html', '铜仁': '/aqi/tongren.html', '黔西南': '/aqi/qianxinan.html', '黔南': '/aqi/qiannan.html', '黔东南': '/aqi/qiandongnan.html'},
             '云南': {'昆明': '/aqi/kunming.html', '玉溪': '/aqi/yuxi.html', '保山': '/aqi/baoshan.html', '昭通': '/aqi/zhaotong.html', '丽江': '/aqi/lijiang.html', '临沧': '/aqi/lincang.html', '西双版纳': '/aqi/xishuangbanna.html', '德宏': '/aqi/dehong.html', '怒江': '/aqi/nujiang.html', '大理': '/aqi/dali.html', '曲靖': '/aqi/qujing.html', '楚雄': '/aqi/chuxiong.html', '红河': '/aqi/honghe.html', '思茅': '/aqi/simao.html', '文山': '/aqi/wenshan.html', '普洱': '/aqi/puer.html', '迪庆': '/aqi/diqing.html'},
             '西藏': {'拉萨': '/aqi/lasa.html', '林芝': '/aqi/linzhi.html', '山南': '/aqi/shannan.html', '昌都': '/aqi/changdu.html', '日喀则': '/aqi/rikaze.html', '阿里': '/aqi/ali.html', '那曲': '/aqi/naqu.html'}, '陕西': {'西安': '/aqi/xian.html', '铜川': '/aqi/tongchuan.html', '宝鸡': '/aqi/baoji.html', '咸阳': '/aqi/xianyang.html', '渭南': '/aqi/weinan.html', '延安': '/aqi/yanan.html', '汉中': '/aqi/hanzhong.html', '榆林': '/aqi/yulin.html', '安康': '/aqi/ankang.html', '商洛': '/aqi/shanglv.html'},
             '甘肃': {'兰州': '/aqi/lanzhou.html', '嘉峪关': '/aqi/jiayuguan.html', '天水': '/aqi/tianshui.html', '武威': '/aqi/wuwei.html', '张掖': '/aqi/zhangye.html', '平凉': '/aqi/pingliang.html', '酒泉': '/aqi/jiuquan.html', '庆阳': '/aqi/gsqingyang.html', '定西': '/aqi/dingxi.html', '甘南': '/aqi/gannan.html', '临夏': '/aqi/linxia.html', '白银': '/aqi/baiyin.html', '金昌': '/aqi/jinchang.html', '陇南': '/aqi/longnan.html'}, '青海': {'西宁': '/aqi/xining.html', '海东': '/aqi/haidong.html', '果洛': '/aqi/guolv.html', '海北': '/aqi/haibei.html',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     '海南': '/aqi/hainan.html', '海西': '/aqi/haixi.html', '玉树': '/aqi/yushu.html', '黄南': '/aqi/huangnan.html'}, '宁夏': {'银川': '/aqi/yinchuan.html', '石嘴山': '/aqi/shizuishan.html', '吴忠': '/aqi/wuzhong.html', '固原': '/aqi/nxguyuan.html', '中卫': '/aqi/zhongwei.html'}, '新疆': {'乌鲁木齐': '/aqi/wulumuqi.html', '伊犁哈萨克州': '/aqi/yili.html', '克拉玛依': '/aqi/kelamayi.html', '哈密': '/aqi/hami.html', '石河子': '/aqi/shihezi.html', '和田': '/aqi/hetian.html', '五家渠': '/aqi/wujiaqu.html', '阿克苏': '/aqi/akesu.html', '阿勒泰': '/aqi/aletai.html', '喀什': '/aqi/kashi.html', '库尔勒': '/aqi/kuerle.html', '吐鲁番': '/aqi/tulufan.html', '塔城': '/aqi/tacheng.html', '博州': '/aqi/xjbozhou.html', '昌吉': '/aqi/changji.html', '克州': '/aqi/kezhou.html'}}

url1 = "http://www.86pm25.com/"
url2 = "http://www.tianqihoubao.com/aqi/"

# 抓取网页
def get_url(url,decode='GBK'):
    # ua = UserAgent()
    # head = {"User-Agent": str(ua.chrome)}
    try:
        # request = urllib.request.Request(url=url, headers=head)
        request = urllib.request.Request(url=url)
        fp = urllib.request.urlopen(request)
        html = fp.read().decode(decode)
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
    soup = BeautifulSoup(html,'html.parser')
    city_all = soup.find(name="div",attrs={'class':"citychk"})                  # 匹配第一个<div class=all>
    province = city_all.find_all(name="dl")
    str_clear = re.compile(r'\S+')                  # 只保留字符串
    all_dict = {}
    for p in province:
        p_name = p.find(name="dt").text
        p_cities = p.find(name="dd")
        p_cities = p_cities.find_all(name="a")
        cities_dict = {}
        for city in p_cities:
            cities_dict[str_clear.findall(city.text)[0]] = city['href']
        all_dict[p_name] = cities_dict
    return all_dict
# city_dict = get_city()

# 读取数据为字典
def read_data(name):
    try:
        with open(name,mode="r",encoding="utf-8") as fp:
            js = fp.read()
            dic = json.loads(js)
        return dic
    except:
        return None

# 将数据写入txt文件
def write_data(name,data):
    with open(name,mode="w",encoding="utf-8") as fp:
        fp.write(json.dumps(data))

# 根据城市名，获取当前小时更新了的数据
def Today_data_html(city_name="北京"):
    base_url = "http://www.tianqihoubao.com"
    for p in city_dict.keys():
        if city_name in city_dict[p].keys():
            base_url += city_dict[p][city_name]
    print(base_url)                                     # 找到网址
    try:
        html = get_url(base_url)
    except:
        print("获取当小时数据失败")
        return None
    soup = BeautifulSoup(html, 'html.parser')
    # 获取当天的数据
    clear_str = re.compile(r'\S+')
    Today_body = soup.find(name='div', attrs={'id': 'content', 'class': 'wdetail'})
    Today_update_time = Today_body.find(name='div', attrs={'class': 'desc'}).text
    Today_data = [clear_str.findall(data) for data in Today_update_time.split("\n")]    # 去掉一些无用的字符串
    Today_date = Today_data[1][0] + Today_data[1][1] + "  " + Today_data[1][2]          # 拼接出更新时间

    Today_num = clear_str.findall(Today_body.find(name="div", attrs={'class': 'num'}).text)[0]  # AQI并去除无关符号
    Today_status = clear_str.findall(Today_body.find(name="div", attrs={'class': 'status'}).text)[0]  # 空气质量等级并去除无关符号

    Today_feature = clear_str.findall(Today_body.find(name="div", attrs={'class': 'feature'}).text)

    Today_object = [tx.text for tx in Today_body.find(name="div", attrs={'class': 'txt01'}).find_all(name="li")]
    Today_pollute = {'PM2_5':Today_object[0],'CO':Today_object[1],'SO2':Today_object[2],
                     'PM10':Today_object[3],'OO':Today_object[4],'NO2':Today_object[5]}

    Today_data = {'Today_date': Today_date, 'Today_num': Today_num, 'Today_status': Today_status,
                  'Today_city': city_name,'Today_status': Today_status, 'Today_feature1': Today_feature[0],
                  'Today_feature2': Today_feature[1],'Today_pollute': Today_pollute}
    return Today_data

# 获取当前小时的城市数据
def get_Today_data(city_name):
    filename = "./Today_data/"+city_name+".txt"
    Today_data = read_data(filename)                # 先在本地文件中查看是否有缓存的当天的数据
    if Today_data:                                  # 如果有当天的数据
        print("获取到当日数据",Today_data)
        now_hour = get_now_time().split(' ')[-1].split(":")[0]
        file_hour = Today_data['Today_date'].split(' ')[-1].split(":")[0]
        if now_hour == file_hour:                   # 文件中的仍然是最新数据，则直接返回
            return Today_data
    new_Today_data = Today_data_html(city_name)     # 否则重新爬取数据并读取
    if new_Today_data:                              # 获取数据成功
        print("更新本地数据最新数据：",new_Today_data)
        write_data(filename,new_Today_data)             # 写入到本地
        return new_Today_data
    return Today_data                               # 没有获取数据成功，使用以前的老数据

# 获取各项指标
def get_time_AQI(dic):
    city_title = dic['title']
    city_data = dic['data']
    AQI_dict = {}                       # AQI字典
    cate_list = []                      # 空气质量统计列表
    cate_dict = {}                      # 空气质量分类字典
    for ti in city_data.keys():
        AQI_dict[ti] = int(city_data[ti][2])
        cate_list.append(city_data[ti][1])
    for c in set(cate_list):
        cate_dict[c] = 0                # 初始化指数类别种类
    for cate in cate_list:              # 计算各空气质量种类的占比
        cate_dict[cate] += 1

    # 饼图内容
    cate = []
    for key, value in cate_dict.items():
        cate.append({'name': key, 'value': value})  # 转换为饼图需要的格式

    # 折线图内容
    city_time = list(AQI_dict.keys())   # 时间列表
    city_AQI = list(AQI_dict.values())  # AQI值列表
    return city_time,city_AQI,cate

# 获取当年的历史数据
def get_years_data(file_year,year):
    year_dict = {}
    month = ['01月','02月','03月','04月','05月','06月','07月','08月','09月','10月','11月','12月']
    for m in month:
        filename = file_year +"/"+year+m+".txt"
        if Path(filename).exists():                 # 如果该月份的文件存在，则读取
            dic = read_data(filename)
            city_time, city_AQI,cate = get_time_AQI(dic)
            year_dict[year+m] = {'city_time':city_time,'city_AQI':city_AQI,'cate':cate}
    return year_dict

# 获取城市历史数据
def Histroy_data(city_name="北京",tim="2020年02月"):
    print("获取历史数据：",(city_name,tim))
    filename = "./history_data/"
    file_year = "./history_data/"
    for p in city_dict.keys():
        if city_name in city_dict[p].keys():
            filename += p
            file_year += p
    filename = filename + "/"+city_name+"/"+tim+".txt"             # 生成历史数据文件的路径
    file_year = file_year + "/"+city_name                          # 生成年份数据文件的路径
    year = tim.split('年')[0] +"年"

    dic = read_data(filename)                                      # 读取当月的历史数据
    if dic==None:                                                  # 如果读取当月数据失败，返回空
        return None
    city_time,city_AQI,cate = get_time_AQI(dic)                    # 获取当月时间，AQI，空气质量分类（折线图、饼图）
    Today_data = get_Today_data(city_name)                         # 该城市当时的空气质量
    year_dict = get_years_data(file_year,year)                     # 获取该年的数据（折线图）
    return_dict =  {'Today_data':Today_data,'city_time':city_time,'city_AQI':city_AQI,'cate':cate,'year_dict':year_dict}
    print("获取历史数据成功：",return_dict)
    return return_dict

# 从pm86网站获取实时数据
def pm25_86(province_name):
    print("正在获取数据",province_name)
    base_url = "http://www.86pm25.com/paiming.htm"
    try:
        html = get_url(base_url,"utf-8")
    except:
        print("获取网页内容失败！")
        return None
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find(name="table",attrs={"id":"goodtable"})
    Today_time = soup.find(name="div",attrs={"class":"weilai"}).find_all(name="div")[1].text    # 更新时间

    tbody = table.find_all(name="tr")
    title = tbody[0].text
    province_dict={}                                        # 以省为键，各个城市的数据为值

    for tr in tbody[1:]:                                    # 获取每个城市的数据
        td = tr.find_all(name="td")
        p = td[2].text                                      # 省份名
        p = p.split("省")[0]
        p = p.split("市")[0]
        if p in province_dict.keys():
            province_dict[p].append([td[1].text,int(td[3].text),td[4].text,td[5].text])
        else:
            province_dict[p]=[[td[1].text, int(td[3].text), td[4].text, td[5].text]]

    province_city_AQI_dict = {}                             # 获取各个省份的AQI数据
    pie_cate_dict = {}                                      # 获取每个省空气质量分类情况
    for p, c in province_dict.items():
        province_city_AQI_dict[p] = []
        pie_cate_dict[p] = []
        for every_c in c:
            # AQI
            city_AQI_dict = {'name': every_c[0], 'value': every_c[1]}
            province_city_AQI_dict[p].append(city_AQI_dict)
            # 空气质量分类
            flag = True
            for index in range(len(pie_cate_dict[p])):                   # 查看该省的已有分类
                if pie_cate_dict[p][index]['name']==every_c[2]:
                    pie_cate_dict[p][index]['value'] += 1
                    flag = False
                    break
            if flag:
                pie_cate_dict[p].append({'name':every_c[2],'value':1})  # 如果未找到该分类，则添加该分类

    map_data = []
    pie_data = []
    rank_data = {"pro_name":[],"data":[]}
    if province_name=="全国":                                 # 如果是全国的，AQI计算每个省的均值，空气质量重新统计和
        # AQI
        for p,c in province_city_AQI_dict.items():
            value_sum = 0
            for evety_c in c:
                value_sum += evety_c['value']
            map_data.append({'name':p,'value':int(value_sum/len(c))})
        # 空气质量分类
        for p,c in pie_cate_dict.items():
            for evety_c in c:
                flag = True
                for index in range(len(pie_data)):
                    if pie_data[index]['name'] == evety_c['name']:
                        pie_data[index]['value'] += evety_c['value']
                        flag = False
                        break
                if flag:
                    pie_data.append(evety_c)
    else:
        map_data = province_city_AQI_dict[province_name]    # 如果是单个省的，直接返回该省的数据
        pie_data = pie_cate_dict[province_name]
    map_data = sorted(map_data, key=lambda keys: keys['value']) # 对AQI排序，生成排序字典

    for p in map_data:
        rank_data['pro_name'].append(p['name'])
        rank_data['data'].append(p['value'])
    return {'p_name':province_name,'Today_time':Today_time,'map_data':map_data,'pie_data':pie_data,'rank_data':rank_data}


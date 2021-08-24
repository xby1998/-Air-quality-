from flask import Flask, request, render_template,jsonify
from datetime import timedelta
from base_fun import get_now_time,read_data
from web_data import Histroy_data,pm25_86

# 配置设置
app = Flask(__name__)
app.config['DEBUG']= True                                       # DEBUG模式
app.config['SEND_FILE_MAX_AGE_DEFAULT']= timedelta(seconds=1)   # 默认缓存控制的最大期限，以秒计

# 城市空气质量查询
@app.route('/visual_histroy',methods=['post','get'])    # 路由地址、请求的方式包括“post”和“get”
def get_histroy():
    return render_template("histroy_time.html")         # 展示网页

# 全国空气质量查询
@app.route('/visual_current',methods=['post','get'])
def get_current():
    return render_template("current_time.html")

# 获取城市空气质量查询的数据更新响应
@app.route('/data',methods=['post','get'])
def get_cur_data():
    if request.method == "POST":
        return_dict = Histroy_data(request.values.get('city'), request.values.get('time'))
        return jsonify(return_dict)
    else:
        return_dict = Histroy_data("北京","2021年01月")
        return jsonify(return_dict)
# 获取地图json文件内容的响应
@app.route('/geo_map',methods=['post','get'])
def get_map():
    province_name = request.values.get('province_name')
    print("获取地图：",province_name)
    filename = "./static/js/province/"+province_name+".json"
    return_dict = read_data(filename)
    return jsonify(return_dict)
# 获取全国空气质量查询的数据更新响应
@app.route('/data_country',methods=['post','get'])
def get_country_data():
    if request.method == "POST":
        return_dict = pm25_86(request.values.get('province_name'))
        if return_dict:
            print("获取到数据：",return_dict)
            return jsonify(return_dict)
        else:
            return None
    else:
        return_dict = pm25_86('全国')
        if return_dict:
            print("获取到数据：", return_dict)
            return jsonify(return_dict)
        else:
            return None
# 实时时间的更新
@app.route('/time',methods=['post','get'])
def get_time():
    if request.values.get('name') == '现在':
        return get_now_time()

if __name__ == '__main__':
    app.run(debug=True)

import time
import json
def get_now_time():
    time_now = time.strftime("%Y{}%m{}%d{} %X")
    return time_now.format("-","-"," ")             # 格式化

# 读取数据为字典
def read_data(name):
    try:
        with open(name,mode="r",encoding="utf-8") as fp:
            js = fp.read()
            dic = json.loads(js)                    # 加载为json格式
        return dic
    except:
        return None
import yaml
import requests


class Tools:
    @staticmethod
    def read_config(filename='config.yaml'):    # yaml配置文件读取
        with open(filename, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config

    @staticmethod       # 接口返回信息转json
    def get_json(url,cookie=None):
        url = url
        bda = requests.get(url, cookies=cookie, verify=False).json()
        return bda

    @staticmethod       # 配置文件类别区分提取
    def get_config(key):
        config = Tools.read_config()
        return config[key]

    @staticmethod
    def cookie_set():       # cookie字段提取转换
        cookie_b = Tools.get_config('bilibili')['cookie'].encode("utf-8").decode("latin1")
        cookies = {}  # 初始化cookies字典变量
        for line in cookie_b.split(';'):  # 按照字符：进行划分读取
            # 其设置为1就会把字符串拆分成2份
            name, value = line.strip().split('=', 1)
            cookies[name] = value  # 为字典cookies添加内容
        return cookies



# a = Tools.cookie_set()
# print(a)
import yaml, ddt, requests, json, unittest, configparser

from config import setting
from public.models.log import Log

con = configparser.ConfigParser()
con.read(setting.CONFIG_DIR, encoding='utf-8')
# 区分测试or线上环境的逻辑，暂无必要
# env = con.get("ENVIRONMENT", "ENV")
# if env == 'local':
#     _url = con.get("WebURL", "XCC_110_URL")
# else:
#     _url = con.get("WebURL", "XCC_URL")

# _url = con.get("WebURL", "XCC_URL")
_url = con.get("WebURL", "XCC_110_URL")

try:
    data = open(setting.TEST_DATA_YAML + '/api/business_data.yaml', encoding='utf-8')
    testData = yaml.load(data, Loader=yaml.FullLoader)
except FileNotFoundError as file:
    log = Log()
    log.error("文件不存在：{}".format(file))


@ddt.ddt
class ItemDownShelfTest(unittest.TestCase):

    @ddt.data(*testData)
    def test_business_registration(self, data_yaml):
        print('正在登陆：' + data_yaml['phone'])
        # 登陆
        url = _url + '/blade-auth/oauth/token'
        # 请求参数
        payload = {
            "username": data_yaml['phone'],
            "password": data_yaml['password'],
            "grant_type": "password"
        }
        headers = {"Authorization": "Basic d2ViOndlYl9rdW5oZW5n"}
        # form表单形式，参数用data
        res = requests.post(url, data=payload, headers=headers, verify=False)
        token = ''
        if res.status_code == 200:
            result = json.loads(res.text)
            token = result['access_token']
        else:
            print("登陆失败，接口返回：" + res.text)

        # 查询商品id
        url = _url + '/kunheng-business/bus-goods/list?goodsType=1&current=1&size=100'
        headers = {"Authorization": "Basic d2ViOndlYl9rdW5oZW5n",
                   "blade-auth": "bearer " + token}
        res = requests.get(url=url, headers=headers, verify=False)
        ids = []
        if res.status_code == 200:
            result = json.loads(res.text)
            data = result['data']['records']
            ids = []
            for i in enumerate(data):
                id = i[1]['goodsId']
                ids.append(id)
            print(ids)
        else:
            print("查询失败，接口返回：" + res.text)

        # 下架商品
        if len(ids) > 0:
            url = _url + '/kunheng-business/bus-goods/batch-drop-off'
            # 请求参数
            data = {
                "goodsIds": ids,
                "upperStatus": "0"
            }
            headers = {"Authorization": "Basic d2ViOndlYl9rdW5oZW5n",
                       "blade-auth": "bearer " + token,
                       "Content-Type": "application/json;charset=UTF-8"
                       }
            res = requests.post(url, json=data, headers=headers, timeout=300, verify=False)
            print(res.text)
        else:
            print("结束...")


if __name__ == '__main__':
    unittest.main()

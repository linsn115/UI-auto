import unittest
import os, datetime
from BeautifulReport import BeautifulReport

from public.models.sendMessage import SendMessage
from public.page_obj.base import con

root_dir = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
test_dir = root_dir + '/testcase'
report_dir = root_dir + '/report'
env = con.get("ENVIRONMENT", "ENV")

# 执行用例
discover = unittest.defaultTestLoader.discover(test_dir, '*.py', None)
data = ''

if env == 'local':
    now = datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S')
    filename = '测试报告' + str(now)
else:
    filename = 'testReport'
    # 发送钉钉消息
    data = {
        "actionCard": {
            "title": "星查查UI测试报告展示",
            "text": "![screenshot](https://kh-3-dev.oss-cn-hangzhou.aliyuncs.com/000000/upload/20201224/68cf50d2336c84fbcbbf566a14707385.png)游客仅查看报告，登录后即享更多操作，测试账号:ceshi，密码：123456，有问题钉钉联系测试人员",
            "btnOrientation": "0",
            "singleTitle": "阅读报告",
            "singleURL": "http://192.168.2.15:8080/job/test_project_xcc/HTML_20Report/"
        },
        "msgtype": "actionCard"
    }
# 输出报告
BeautifulReport(discover).report(description='星查查UI自动化测试', filename=filename, log_path=report_dir)
if env != 'local':
    SendMessage().send_message(data)

import os, sys

from BeautifulReport import BeautifulReport

import unittest, ddt, yaml
from config import setting
from public.models import myunit, connectMysql
from public.page_obj.loginPage import Login
from public.models.log import Log

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    f = open(setting.TEST_DATA_YAML + '/' + 'login_data.yaml', encoding='utf-8')
    testData = yaml.load(f, Loader=yaml.FullLoader)
except FileNotFoundError as file:
    log = Log()
    log.error("文件不存在：{0}".format(file))


@ddt.ddt
class LoginTest(myunit.UITest):

    @BeautifulReport.add_test_img("test_login")
    @ddt.data(*testData)
    def test_login(self, datayaml):
        """
        登录测试
        """
        log = Log()
        log.info("当前执行测试用例ID-> {} ; 测试点-> {}".format(datayaml['id'], datayaml['detail']))
        # 调用登录方法
        Login(self.driver).user_login_phone_password(datayaml['data']['phone'], datayaml['data']['password'])
        po = Login(self.driver)
        # 登录成功
        if datayaml['screenshot'] == 'phone_password_success':
            # 跳过新手引导
            Login(self.driver).skip()
            log.info("检查点:登陆成功后用户名-> {}".format(po.get_username()))
            # 连接数据库查询当前登陆用户名
            username = \
                connectMysql.select_sql_by_parameter("name", "blade_user", "phone", datayaml['data']['phone'])['name'][
                    0]
            # 校验数据库存的用户名是否与页面展示一致
            self.assertEqual(username, po.get_username(),
                             "当前登陆用户不是手机号{}注册用户:{}".format(datayaml['data']['phone'], username))

        # 密码不正确或密码为空
        if datayaml['screenshot'] == 'password_empty_or_error':
            log.info("检查点:登陆失败的错误提示-> {}".format(po.password_empty_or_error_hint()))
            self.assertEqual(po.password_empty_or_error_hint(), datayaml['check'][0],
                             "异常登录，返回实际结果是->: {}".format(po.password_empty_or_error_hint()))
            log.info("异常登录，返回实际结果是->: {}".format(po.password_empty_or_error_hint()))

        # 手机号不正确或手机号为空
        if datayaml['screenshot'] == 'phone_empty_or_error':
            log.info("检查点:登陆失败的错误提示-> {}".format(po.phone_empty_or_error_hint()))
            p = po.phone_empty_or_error_hint()
            print(p)
            self.assertEqual(po.phone_empty_or_error_hint(), datayaml['check'][0],
                             "异常登录，返回实际结果是->: {}".format(po.phone_empty_or_error_hint()))
            log.info("异常登录，返回实际结果是->: {}".format(po.phone_empty_or_error_hint()))


if __name__ == '__main__':
    unittest.main()

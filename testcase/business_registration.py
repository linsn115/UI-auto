import os, sys
from BeautifulReport import BeautifulReport

from public.page_obj.anchor.AnchorAuditManagePage import AnchorAuditManage
from public.page_obj.business.BusinessRegistrationManagePage import BusinessRegistrationManage
import unittest, ddt, yaml
from config import setting
from public.models import myunit, screenshot, connectMysql
from public.page_obj.loginPage import Login
from public.models.log import Log

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    data = open(setting.TEST_DATA_YAML + '/business/business_registration_data.yaml', encoding='utf-8')
    testData = yaml.load(data, Loader=yaml.FullLoader)
except FileNotFoundError as file:
    log = Log()
    log.error("文件不存在：{}".format(file))


@ddt.ddt
class BusinessRegistrationTest(myunit.UITest):

    @BeautifulReport.add_test_img("test_business_registration")
    @ddt.data(*testData)
    def test_business_registration(self, data_yaml):
        """
        商家报名主播-主播审核商品&排期测试
        """
        log = Log()
        log.info("当前执行测试用例ID-> {} ; 测试点-> {}".format(data_yaml['id'], data_yaml['detail']))
        # 商家登录
        Login(self.driver).user_login_phone_password(data_yaml['login_data']['business_phone'],
                                                     data_yaml['login_data']['business_password'])
        # 打开商家业务中心
        Login(self.driver).open_user_business_center(True)
        # 商家：商品报名
        BusinessRegistrationManage(self.driver).products_registration(data_yaml)
        # 退出商家账号
        Login(self.driver).user_logout()
        # 主播登录
        Login(self.driver).phone_password_login(data_yaml['login_data']['anchor_phone'],
                                                data_yaml['login_data']['anchor_password'])
        # 打开主播业务中心
        Login(self.driver).open_user_business_center(False)
        # 主播：审核商品
        AnchorAuditManage(self.driver).anchor_audit_products(data_yaml['product_data'])
        if data_yaml['product_data']['recheck'] == '通过':
            # 主播:商品排期-新建场次
            schedule_name = AnchorAuditManage(self.driver).product_schedule(data_yaml['product_data'])
            # 连接数据库校验刚新建的场次是否存在
            # obj = connectMysql.get_sql_query("SELECT * FROM anc_broadcast where topic='{}'".format(schedule_name))
            obj = connectMysql.select_sql_by_parameter("*", "anc_broadcast", "topic", schedule_name)
            self.assertTrue(len(obj) > 0, "数据库查询不到新建的场次名为{}".format(schedule_name))
            # 选择场次
            AnchorAuditManage(self.driver).select_activity()
            # 校验场次名称是否与新建场次名称一致
            self.assertEqual(AnchorAuditManage(self.driver).schedule_name_get_text(), schedule_name, msg='直播名称不一致')
            # 确认排期
            AnchorAuditManage(self.driver).schedule_submit()


if __name__ == '__main__':
    unittest.main()

import os, sys
from time import sleep
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from public.page_obj.base import Page

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


class BusinessRegistrationManage(Page):
    """
    星查查商家中心-报名管理下所有页面
    """
    url = '/'

    def open_product_registration(self):
        """
        打开商家中心-报名管理-商品报名
        """
        product = self.find_element(*self.product_registration)
        ActionChains(self.driver).move_to_element(product).click().perform()
        sleep(1)

    def search_anchor(self, anchor_name):
        """
        根据名称查找主播
        :param anchor_name:主播名称
        :return:
        """
        self.find_element(*self.anchor_name_input).send_keys(anchor_name)
        self.find_element(*self.search_btn).click()
        sleep(1)

    def products_registration(self, data):
        """
         商家报名主播选择商品功能
        :param data: 数据源
        """
        self.open_product_registration()
        self.search_anchor(data['login_data']['anchor_name'])
        choose_anchor = self.find_elements(*self.choose_anchor_btn)
        ActionChains(self.driver).move_to_element(choose_anchor[0]).click().perform()
        self.find_element(*self.next_btn).click()
        self.find_element(*self.choose_product_btn).click()
        self.find_element(*self.product_input).send_keys(data['product_data']['product_name'])
        sleep(1)
        self.find_element(*self.search_btn).click()
        # 选择符合商品名的第一个商品
        sleep(1)
        goods = self.find_elements(*self.goods_checkbox)
        goods[1].click()
        self.find_element(*self.submit_btn).click()
        self.find_element(*self.next_btn).click()
        # 提交报名
        self.find_element(*self.submit_registration_btn).click()

    # 定位器，通过元素属性定位元素对象
    #  商品报名按钮
    product_registration = (By.XPATH, "//div[contains(text(),'商品报名')]")
    #  主播名称输入框
    anchor_name_input = (By.XPATH, "//input[@placeholder='请输入主播名称']")

    #  选择主播按钮
    choose_anchor_btn = (By.XPATH, "//button[@class='el-button combtn el-button--primary el-button--small']/span")
    #  下一步按钮
    next_btn = (By.XPATH, "//div[@class='czbtn next']")
    #  选择商品按钮
    choose_product_btn = (By.XPATH, "//div[@class='flex btntit']//span[.='选择商品']")
    #  商品名输入框
    product_input = (By.XPATH, "//input[@placeholder='请输入商品名称']")
    #  商品名搜索按钮
    search_btn = (By.XPATH, "//span[.='查询']")
    #  商品选择框
    goods_checkbox = (By.XPATH, "//span[@class='el-checkbox__inner']")
    #  确定按钮
    submit_btn = (By.XPATH, "//span[.='保存']")
    #  选择对接人下拉框
    docking_people = (By.XPATH, "//input[@placeholder='请选择对接人']")
    #  选择对接人下拉列表
    docking_people_list = (
        By.XPATH, "//body/div[@class='el-select-dropdown el-popper']//li[@class='el-select-dropdown__item']")
    #  提交报名按钮
    submit_registration_btn = (By.XPATH, "//span[.='提交报名']")
    #  提交报名按钮
    success_flag = (By.XPATH, "//div[.='报名成功']]")

    # 校验=====================
    # 登录成功用户名
    user_login_success_loc = (By.XPATH, "//div[@class='el-form-item__error']")

    # 登录成功用户名
    def user_login_success_hint(self):
        return self.find_element(*self.user_login_success_loc).text

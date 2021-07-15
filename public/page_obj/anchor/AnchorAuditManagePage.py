import datetime
import os, sys
from time import sleep
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from public.page_obj.base import Page

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


class AnchorAuditManage(Page):
    """
    星查查主播中心
    """
    url = '/'
    now = datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S')

    def anchor_audit_products(self, data):
        """
        主播审核商品+商品排期
        :param data: 商品信息
        """
        # 打开主播中心-审核管理-报名商品
        self.find_element(*self.anchor_audit).click()
        sleep(1)
        # 切换初审页面
        self.find_element(*self.first_trial_page).click()
        # 查找初审商品
        self.search_product(data["product_name"])
        self.open_approval_page()
        if data["first_trial"] == '通过':
            # 通过
            self.find_element(*self.consent_button).click()
            self.find_element(*self.submit_button).click()
            sleep(3)
            # 复审
            self.recheck_approval(data["recheck"], data["product_name"], data["remake"])
        else:
            # 不通过
            self.find_element(*self.veto_button).click()
            self.find_element(*self.remake_textarea).send_keys(data["remake"])
            self.find_element(*self.submit_button).click()
        sleep(3)

    def search_product(self, product_name):
        """
        星查查主播后台-审核管理-报名商品-根据商品名查询商品并打开审批页面
        :param product_name: 商品名
        """
        self.find_element(*self.search_product_business_input).send_keys(product_name)
        self.find_element(*self.search_button).click()
        sleep(2)

    def open_approval_page(self):
        """
        星查查主播后台-审核管理-报名商品-打开列表第一个商品的审批页面
        """
        approval_list = self.find_elements(*self.approval_buttons)
        approval = approval_list[0]
        ActionChains(self.driver).move_to_element(approval).click().perform()
        sleep(1)

    def recheck_approval(self, recheck, product_name, remake):
        """
        复审商品
        :param recheck: 复审意见
        :param product_name: 商品名称
        :param remake: 复审备注
        """
        # 打开复审页面
        self.find_element(*self.recheck_page).click()
        # 查找复审商品
        self.search_product(product_name)
        self.open_approval_page()
        if recheck == '通过':
            # 通过
            self.find_element(*self.consent_button).click()
        else:
            # 不通过
            self.find_element(*self.veto_button).click()
            self.find_element(*self.remake_textarea).send_keys(remake)

        self.find_element(*self.submit_button).click()
        sleep(3)

    def product_schedule(self, data):
        """
        新建活动场次
        :param data: 商品信息
        :return schedule_title: 创建活动的名称
        """
        # 打开工作台
        self.find_element(*self.workbench).click()
        sleep(1)
        self.find_element(*self.schedule_page).click()
        # 查找排期商品-工作台
        self.find_element(*self.search_product_input).send_keys(data["product_name"])
        self.find_element(*self.search_button).click()
        schedule_list = self.find_elements(*self.product_schedule_button)
        schedule_list[0].click()
        # 新建活动
        self.find_element(*self.add_schedule_button).click()
        # 新建活动
        schedule_title = data["title"] + self.now
        self.find_element(*self.schedule_title_input).send_keys(schedule_title)
        self.find_element(*self.plan_date_input).send_keys(data["plan_date"])
        self.find_element(*self.plan_date_input).send_keys(Keys.ENTER)
        self.find_element(*self.submit_button_schedule).click()
        sleep(2)
        # self.find_element(*self.principal_input).click()
        # principal_select_list = self.find_elements(*self.principal_select)
        # principal_select_list[0].click()
        # self.find_element(*self.plan_time_input).click()
        # self.find_element(*self.plan_time_confirm_button).click()
        # investment_time_list = self.find_elements(*self.investment_time)
        # investment_time_list[0].send_keys(data["investment_start_time"])
        # investment_time_list[1].send_keys(data["investment_end_time"])
        # self.find_element(*self.planned_merchandise_number).send_keys(data["product_number"])
        # self.find_element(*self.planned_merchandise_number).send_keys(Keys.PAGE_DOWN)
        # sleep(1)
        # self.find_element(*self.submit_button).click()
        # 查询最新场次列表
        self.find_element(*self.schedule_list_search_input).send_keys(schedule_title)
        self.find_element(*self.schedule_list_search_button).click()
        sleep(1)
        return schedule_title

    def select_activity(self):
        # 选择场次
        schedule_list_select_list = self.find_elements(*self.schedule_list_select)
        schedule_list_select_list[0].click()
        self.find_element(*self.schedule_list_next_step).click()

    def schedule_submit(self):
        # 确认排期
        self.find_element(*self.schedule_submit_button).click()

    # 定位器，通过元素属性定位元素对象
    # 报名商品
    anchor_audit = (By.XPATH, "//div[contains(text(),'报名商品')]")
    # 搜索报名商品/商家输入框
    search_product_business_input = (By.XPATH, "//input[@placeholder='请输入商品/商家名称']")
    # 搜索商品输入框
    search_product_input = (By.XPATH, "//input[@placeholder='请输入商品名称/商家名称']")
    # 搜索按钮
    search_button = (By.XPATH, "//button[@class='el-button el-button--info el-button--mini']/span[.='查询']")
    # 初审页面
    first_trial_page = (By.XPATH, "//div[@class='screen-div-item' and contains(text(),'初审')]")
    # 审批按钮
    approval_buttons = (By.XPATH, "//button[@role-per='endCheck']/span[.=' 审批 ']")
    # 通过按钮
    consent_button = (By.XPATH, "//span[.='通过']")
    # 不通过按钮
    veto_button = (By.XPATH, "//span[.='不通过']")
    # 提交按钮
    submit_button = (By.XPATH, "//span[.='提交']")
    # 备注输入框
    remake_textarea = (By.XPATH, "//textarea[@placeholder='请输入备注']")
    # 工作台
    workbench = (By.XPATH, "//span[.='工作台 ']")
    # 复审页面
    recheck_page = (By.XPATH, "//div[@class='screen-div-item' and contains(text(),'复审')]")
    # 排期页面
    schedule_page = (By.XPATH, "//button[@class='el-button el-button--default el-button--mini']/span[.='商品排期']")
    # 商品排期按钮
    product_schedule_button = (By.XPATH, "//button[@class='el-button el-button--text']/span[contains(text(),'商品排期')]")
    # 创建活动场次按钮-审核管理
    add_schedule_button = (By.XPATH, "//span[@class='addtag']")
    # 场次名称
    schedule_title_input = (By.XPATH, "//label[.='名称']/..//input")
    # 计划日期
    plan_date_input = (By.XPATH, "//label[.='计划日期']/..//input")
    # 新增场次确定按钮
    submit_button_schedule = (By.XPATH, "//button[@class='el-button el-button--info el-button--mini']/span[.='确定']/..")



    # 负责人下拉框
    principal_input = (By.XPATH, "//label[.='负责人']/..//input")
    # 负责人选择列表
    principal_select = (By.XPATH, "//body/div[4]//li")
    # 计划时间
    plan_time_input = (By.XPATH, "//label[.='计划时间']/../div/div")
    # 计划时间-确认按钮
    plan_time_confirm_button = (By.XPATH, "//button[@class='el-time-panel__btn confirm']")
    # 招商时间-时间区间
    investment_time = (By.XPATH, "//label[.='招商时间']/..//input")
    # 计划商品数
    planned_merchandise_number = (By.XPATH, "//label[.='计划商品数']/..//input")
    # 商品排期-查询按钮
    schedule_list_search_button = (By.XPATH, "//div[@class='el-dialog']//span[.='查询']")
    # 商品排期-活动名称输入框
    schedule_list_search_input = (By.XPATH, "//input[@placeholder='请输入活动名称']")
    # 商品排期-活动列表选择按钮
    schedule_list_select = (By.XPATH, "//div[@class='right_item']")
    # 商品排期-下一步按钮
    schedule_list_next_step = (By.XPATH, "//span[.='下一步']")
    # 商品排期-确定排期
    schedule_submit_button = (By.XPATH, "//button[@class='el-button el-button--info']")

    # 校验====================
    # 商品排期-直播名称
    schedule_name = (By.XPATH, "//div[@class='table_cont flex']/div[3]")

    def schedule_name_get_text(self):
        # 获取直播名称
        return self.find_element(*self.schedule_name).text

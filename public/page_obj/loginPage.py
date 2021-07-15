import os, sys
from time import sleep

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from selenium.webdriver.common.by import By
from public.page_obj.base import Page


class Login(Page):
    """
    首页&用户登录页面
    """
    url = '/'

    def user_login_phone_password(self, phone, password):
        """
        用户登录
        :param phone: 手机号
        :param password: 密码
        """
        self.open()
        self.phone_password_login(phone, password)

    def phone_password_login(self, phone, password):
        """
        用户登录:手机号+密码
        :param phone: 手机号
        :param password: 密码
        """
        self.find_element(*self.sign_and_login_button).click()
        self.find_element(*self.check_password_button).click()
        self.find_element(*self.login_phone_input).send_keys(phone)
        self.find_element(*self.login_password_input).send_keys(password)
        self.find_element(*self.login_user_button).click()
        sleep(1)

    def skip(self):
        self.find_element(*self.skip_button).click()

    def open_user_business_center(self, flag):
        """
        打开业务中心
        """
        self.find_element(*self.skip_button).click()
        self.find_element(*self.business_center_button).click()
        if flag:
            self.find_element(*self.skip_button).click()
        sleep(2)

    def user_logout(self):
        """
        用户退出登录
        :return:
        """
        self.find_element(*self.user_button).click()
        self.find_element(*self.logout_button).click()
        self.find_element(*self.alert_sure_button).click()
        self.driver.refresh()

    # 定位器，通过元素属性定位元素对象
    # 注册&登录按钮
    sign_and_login_button = (By.XPATH, "//div[@class='login']")
    # 选择密码登录
    check_password_button = (By.XPATH, "//span[.='密码登录']")
    # 手机号输入框
    login_phone_input = (By.XPATH, "//input[@placeholder='请输入手机号码/用户账号']")
    # 密码输入框
    login_password_input = (By.XPATH, "//input[@placeholder='请输入密码']")
    # 单击登录
    login_user_button = (By.XPATH, "//div[@class='btns-box']/button")
    # 跳过按钮
    skip_button = (By.XPATH, "//button[@class='driver-close-btn']")
    # 用户面板
    user_button = (By.XPATH, "//div[@class='user flex']/div[2]/p")
    # 业务中心按钮
    business_center_button = (By.XPATH, "//body/div/header[2]//p[contains(text(),'业务中心 ')]")
    # 退出登录按钮
    logout_button = (By.XPATH, "//div[@class='login-out']")
    # 二次弹窗确认按钮
    alert_sure_button = (
        By.XPATH, "//button[@class='el-button el-button--default el-button--small el-button--primary ']/span")

    # 校验
    # 密码不正确或密码为空
    phone_password_error_hint_loc = (By.XPATH, "//div[@class='el-form-item__error']")
    # 手机号不正确或手机号为空
    phone_empty_or_error_loc = (By.XPATH, "//div[@role='alert']/p")
    # 登陆用户名
    username = (By.XPATH, "//div[@id='guide4']/p")

    # 密码不正确或密码为空
    def password_empty_or_error_hint(self):
        return self.find_element(*self.phone_password_error_hint_loc).text

    # 手机号不正确或手机号为空
    def phone_empty_or_error_hint(self):
        return self.find_element(*self.phone_empty_or_error_loc).text

    # 登陆成功-用户名
    def get_username(self):
        return self.find_element(*self.username).text

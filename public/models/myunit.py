import unittest, os

from selenium import webdriver
from config import setting

path = setting.CHROME_DRIVER + '/' + 'chromedriver.exe'
img_path = setting.PIC_DIR


class UITest(unittest.TestCase):

    def save_img(self, img_name):  # 错误截图方法，这个必须先定义好
        """
         传入一个img_name, 并存储到默认的文件路径下
           :param img_name:
          :return:
      """
        self.driver.get_screenshot_as_file('{}\\{}.png'.format(img_path, img_name))

    def setUp(self):
        self.driver = webdriver.Chrome(executable_path=path)
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()

    # def tearDown(self):
    #     self.driver.quit()

# class APITest(unittest.TestCase):

# def setUp(self):

# def tearDown(self):

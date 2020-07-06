import json
import time

import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class TestCookies:

    def setup_class(self):
        # self.option = Options()
        # self.option.debugger_address = "localhost:9222"
        self.driver = webdriver.Chrome()
        self.driver.get("https://work.weixin.qq.com/wework_admin/loginpage_wx")

    # 手动登录成功后获取cookies
    def test_get_cookies(self):
        time.sleep(30)
        cookies = self.driver.get_cookies()
        with open("cookies.json", "w") as f:
            json.dump(cookies, f)

    # 在浏览器中加入cookies
    def test_add_cookies(self):
        time.sleep(3)
        cookies = json.load(open("cookies.json"))
        for cookie in cookies:
            if 'expiry' in cookie.keys():
                cookie.pop("expiry")
            self.driver.add_cookie(cookie)
        # time.sleep(10)

    def test_weixin(self):
        # 添加验证显示首页元素（可点击）的显式等待逻辑，同时设置首页不显示则重复刷新，定位首页元素不为空则跳出循环
        while True:
            self.driver.refresh()
            ele01 = WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable
                                                         ((By.ID, "menu_index")))
            if ele01 is not None:
                break
        # 添加导入通讯录操作时的显式等待，通过判断元素可点击进行等待判断
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable
                                             ((By.CSS_SELECTOR, ".index_service_cnt_itemWrap:nth-child(2)")))
        self.driver.find_element(By.CSS_SELECTOR, ".index_service_cnt_itemWrap:nth-child(2)").click()

        # 添加上传文件元素的显式等待，通过判断元素加载成功进行等待判断
        WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located
                                             ((By.ID, "js_upload_file_input")))

        self.driver.find_element(By.ID, "js_upload_file_input").send_keys \
            ("C:\\Users\\90619\\PycharmProjects\\pythoncode04\\data\\通讯录批量导入模板.xlsx")

        # 添加上传文件名称元素的显式等待，通过判断元素名称加载成功进行等待判断
        WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located
                                             ((By.ID, "upload_file_name")))
        ele = self.driver.find_element_by_id("upload_file_name").text
        assert ele == '通讯录批量导入模板.xlsx'

    # def teardown_class(self):
    #     self.driver.quit()

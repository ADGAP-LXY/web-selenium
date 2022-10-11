# 开发时间：2022/10/10
# 定义PO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import *
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    _loc_msg = '//p[@class="prompt-msg"]'

    def __init__(self, driver: webdriver.chrome):
        self._driver = driver
        self._wait = WebDriverWait(driver, 10)

    # 实现元素的定位
    def __getattr__(self, item):
        key = f"_loc_" + item
        xpath = getattr(self, key)

        if xpath is not None:
            # 根据xpath进行元素定位
            return self.get_element(xpath)
        raise AttributeError("元素不存在~~")

    def get_element(self, xpath):
        """元素定位会自动等待"""
        el = self._wait.until(
            visibility_of_element_located(
                (
                    By.XPATH,
                    xpath,
                )
            )
        )

        return el

    def alert_ok(self):
        # 等待alert出现
        alert = self._wait.until(alert_is_present())
        # 点击确定
        alert.accept()


# 定义一个page：LoginPage -》继承BasePage
class LoginPage(BasePage):
    _loc_username = '//input[@placeholder="请输入用户名/手机/邮箱"]'
    _loc_password = '//input[@placeholder="请输入登录密码"]'
    _loc_btn = '//button[text()="登录"]'

    def login(self, username, password):
        self.username.sent_keys(username)
        self.password.sent_keys(password)
        self.btn.click()

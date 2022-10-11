# 开发时间：2022/10/9
import time

import pytest
from selenium.webdriver import Keys
from webdriver_helper import get_webdriver
from pages import *


# 夹具 参数：session 作用域：整个会话
@pytest.fixture(scope='session')
def driver():
    """未登录"""
    driver = get_webdriver()
    # 将窗口最大化
    driver.maximize_window()
    driver.get('http://101.34.221.219:8010/')
    # 前置
    yield driver
    # 后置
    print('执行结束啦～～～')
    driver.quit()


# 夹具 参数：session 作用域：整个会话
@pytest.fixture(scope='session')
def user_driver():
    """已登录"""
    driver = get_webdriver()
    # 将窗口最大化
    driver.maximize_window()
    # 打开登录页面
    driver.get('http://101.34.221.219:8010/')
    # 点击登录按钮
    driver.find_element(By.XPATH, '//a[text()="登录"]').click()
    # 输入账号
    driver.find_element(By.XPATH, '//input[@placeholder="请输入用户名/手机/邮箱"]').send_keys("lxy")
    # 输入密码
    driver.find_element(By.XPATH, '//input[@placeholder="请输入登录密码"]').send_keys("qwert12345")
    # 点击登录按钮
    driver.find_element(By.XPATH, '//button[text()="登录"]').click()
    time.sleep(0.5)
    # 前置
    yield driver
    # 后置
    print('执行结束啦～～～')
    driver.quit()


# 正例
def test_login_ok(driver):
    # 点击登录按钮
    driver.find_element(By.XPATH, '//a[text()="登录"]').click()
    # 输入账号
    driver.find_element(By.XPATH, '//input[@placeholder="请输入用户名/手机/邮箱"]').send_keys("lxy")
    # 输入密码
    driver.find_element(By.XPATH, '//input[@placeholder="请输入登录密码"]').send_keys("qwert12345")
    # 点击登录按钮
    driver.find_element(By.XPATH, '//button[text()="登录"]').click()
    time.sleep(0.5)
    # 获取系统提醒
    msg = driver.find_element(By.XPATH, '//p[@class="prompt-msg"]').text
    # 断言
    assert msg == '登录成功'


# 反例
def test_login_fail(driver):
    # 删除浏览器的缓存
    driver.delete_all_cookies()
    # 刷新页面
    driver.refresh()
    # 点击登录按钮
    driver.find_element(By.XPATH, '//a[text()="登录"]').click()
    # 输入账号
    driver.find_element(By.XPATH, '//input[@placeholder="请输入用户名/手机/邮箱"]').send_keys("lxy")
    # 输入密码
    driver.find_element(By.XPATH, '//input[@placeholder="请输入登录密码"]').send_keys("qwert123456")
    # 点击登录按钮
    driver.find_element(By.XPATH, '//button[text()="登录"]').click()
    time.sleep(0.5)
    # 获取系统提醒
    msg = driver.find_element(By.XPATH, '//p[@class="prompt-msg"]').text
    # 断言
    assert msg == '密码错误'


# PO
def test_login_fail_2(driver):
    # 删除浏览器的缓存
    driver.delete_all_cookies()
    # 刷新页面
    driver.refresh()
    # 打开页面，实例化Page
    driver.get('http://101.34.221.219:8010/?s=user/logininfo.html')
    page = LoginPage(driver)
    # 调用Page方法，完成交互
    page.login("lxy", "qwert123456")
    # 获取系统提示
    assert page.msg.text == '密码错误'


def test_order_ok(user_driver):
    # 打开选购页面
    user_driver.get('http://101.34.221.219:8010/')
    # 选择首字段为vivo的a标签
    user_driver.find_element(By.XPATH, '//a[starts-with(text(),"vivo")]').click()
    # 切换到跳转后的页面进行后续操作
    user_driver.switch_to.window(user_driver.window_handles[-1])
    # 用鼠标点击添加购物品数量，并输入购买个数为：2
    user_driver.find_element(By.ID, "text_box").send_keys(Keys.RIGHT)
    time.sleep(0.5)
    user_driver.find_element(By.ID, "text_box").send_keys(Keys.BACK_SPACE)
    user_driver.find_element(By.ID, "text_box").send_keys('2')
    # 点击'立即购买'
    user_driver.find_element(By.XPATH, '//button[@title="点此按钮到下一步确认购买信息"]').click()
    time.sleep(1)
    # 处理弹窗提醒，点击确认
    user_driver.switch_to.alert.accept()
    # 点击货到付款
    user_driver.find_element(By.XPATH, '//span[text()="货到付款"]').click()
    time.sleep(1)
    # 处理弹窗提醒，点击确认
    user_driver.switch_to.alert.accept()
    # 点击'提交订单'
    user_driver.find_element(By.XPATH, '//button[@title="点击此按钮，提交订单"]').click()
    time.sleep(1)
    # 处理弹窗提醒，点击确认
    # user_driver.switch_to.alert.accept()
    # 获取系统提醒
    msg = user_driver.find_element(By.XPATH, '//p[@class="prompt-msg"]').text
    # 断言
    assert msg == '操作成功'


def test_order_fail():
    pass

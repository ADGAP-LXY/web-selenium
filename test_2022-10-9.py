import pdb
import time

from webdriver_helper import get_webdriver
from selenium.webdriver.common.by import By
# driver = get_webdriver()
# driver.get('https://www.youtube.com/')
# time.sleep(10)
# driver.quit() #手动关闭浏览器
import pytest


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


def test_demo1():
    with get_webdriver() as driver:  # 打开浏览器；with：可以自动关闭浏览器
        # 将窗口最大化
        driver.maximize_window()
        driver.get('http://101.34.221.219:8010/')
        # driver.maximize_window()  # 最大化窗口
        # time.sleep(2)
        # 测试动作、断言
        driver.find_element(By.XPATH, '//a[text()="登录"]').click()
        driver.find_element(By.XPATH, '//input[@placeholder="请输入用户名/手机/邮箱"]').send_keys("lxy")
        driver.find_element(By.XPATH, '//input[@placeholder="请输入登录密码"]').send_keys("qwert12345")
        driver.find_element(By.XPATH, '//button[text()="登录"]').click()
        time.sleep(0.5)
        # 获取系统信息
        msg = driver.find_element(By.XPATH, '//p[@class="prompt-msg"]').text
        # pdb.set_trace()
        assert msg == "登录成功"
        time.sleep(2)
        # 等待加载页面后，选择一件物品购买
        driver.find_element(By.XPATH, '//a[starts-with(text(),"vivo")]').click()
        time.sleep(0.5)
        # 切换窗口
        # print(driver.window_handles)
        # print(driver.current_window_handle)
        driver.switch_to.window(driver.window_handles[-1])
        # print(driver.current_url)
        # pdb.set_trace()  # 程序会在这行代码停止，我们可以在终端进行调试
        time.sleep(1)
        driver.find_element(By.ID, "text_box").send_keys('2')
        time.sleep(1)
        driver.find_element(By.XPATH, '//button[@title="点此按钮到下一步确认购买信息"]').click()
        time.sleep(1)
        # 等待弹窗，处理弹窗
        driver.switch_to.alert.accept()  # 点击确认
        driver.find_element(By.XPATH, '//span[text()="货到付款"]').click()
        time.sleep(1)
        # 又会出现弹窗，需要处理
        driver.switch_to.alert.accept()  # 点击确认
        driver.find_element(By.XPATH, '//button[@title="点击此按钮，提交订单"]').click()
        # 弹出操作成功，进行断言
        time.sleep(1)
        msg = driver.find_element(By.XPATH, '//p[@class="prompt-msg"]').text
        # pdb.set_trace()
        assert msg == "操作成功"

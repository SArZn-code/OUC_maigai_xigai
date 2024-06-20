import requests
from selenium.webdriver import EdgeOptions
from selenium.webdriver import Edge
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import time
import json



def sele_enter():
    url = 'https://my.ouc.edu.cn/'
    option = EdgeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option('useAutomationExtension', False)
    driver = Edge(service=Service(f"E:桌面/web spider/msedgedriver.exe"),options=option)
    n = 0
    while True:
        n += 1
        driver.get(url)

        time.sleep(5)

        user_input = driver.find_element(by=By.XPATH, value='/html/body/div/div/div[2]/div[3]/div/div/div[1]/div[1]/form/div[1]/div/div/input')
        pw_input = driver.find_element(by=By.XPATH, value='/html/body/div/div/div[2]/div[3]/div/div/div[1]/div[1]/form/div[2]/div/div/input')
        login_btn = driver.find_element(by=By.XPATH, value='/html/body/div/div/div[2]/div[3]/div/div/div[1]/div[1]/form/div[3]/div/button')

        user_input.send_keys('22220001037')
        pw_input.send_keys('Ouc!#049010')
        time.sleep(1)
        login_btn.click()
        # bb平台2次点击进入
        time.sleep(3)
        b = driver.find_element(by=By.XPATH, value='/html/body/div/div/div[2]/div/div[2]/div[1]/div/div/div[1]/div/div/div/div[3]/div')
        b.click()
        time.sleep(3)
        c = driver.find_element(by=By.XPATH, value='/html/body/div/div/div[2]/div/div[2]/div[2]/div/div[1]/section/div/div[6]/div/div/p')
        c.click()
        print('bb平台进入')

        #新页面转化, 点击确认
        time.sleep(30)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(30)
        c1 = driver.find_element(by=By.XPATH, value='/html/body/div[8]/div/div/div/div/div/div/div[2]/button')
        c1.click()
        print('新页面进入')

        #毛概
        time.sleep(3)
        d = driver.find_element(by=By.XPATH, value='/html/body/div[5]/div/div/div/div[2]/div/div/div/div[3]/div[2]/div[2]/div/div[6]/ul/li[9]/a')
        d.click()
        print('毛概进入')

        # # 侧边栏
        # time.sleep(10)
        # d1 = driver.find_element(by=By.XPATH, value='xx')
        # d1.click()
        # print('侧边栏进入')

        #第三课
        time.sleep(30)
        e = driver.find_element(by=By.XPATH, value='/html/body/div[5]/div[3]/nav/div/div[2]/div[1]/div[2]/ul/li[6]/a')
        e.click()
        print('第三次测试进入')

        #考试
        time.sleep(10)
        f = driver.find_element(by=By.XPATH, value='/html/body/div[5]/div[3]/div/div/div/div/div[2]/ul/li/div[1]/h3/a')
        f.click()
        print('考试进入')

        #新考试
        time.sleep(10)
        g = driver.find_element(by=By.XPATH, value='/html/body/div[5]/div[3]/div/div/div/div/div[2]/div[2]/div[3]/div/p/input[2]')
        g.click()
        print('进入新提交考试')
        #开始新提交
        time.sleep(10)
        h = driver.find_element(by=By.XPATH, value='/html/body/div[5]/div[3]/div/div/div/div/div[2]/div[2]/a[3]')
        h.click()
        print('开始新提交')

        #开始测试
        blank = driver.find_element(by=By.XPATH, value='/html/body/div[5]/div[3]/div/div/div/div/div[2]/form/div[3]/div[18]/div/p/input[2]')
        blank.click()
        time.sleep(30)

        driver.quit()

        print('第%d次' %n)

if __name__=='__main__':
    sele_enter()
#!/usr/bin/python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import unittest, time, re
#import time
import datetime

class Test1(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://www4.tutorabc.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_1(self):
        sessiontime = self.get_sessiontime()
        #[教材預覽]按鈕
        buttonSelector = ".class_bottom > a[perviewmaterial=\"perviewmaterial\"]" #[sessiontime=\"" + sessiontime + "\"]"
        #[教材縮圖清單]
        carouselSelector = ".es-carousel img"
        #print(buttonSelector)
        driver = self.driver
        driver.get(self.base_url + "/asp/login.asp?language=zh-tw")
        driver.find_element_by_id("txt_username").clear()
        driver.find_element_by_id("txt_username").send_keys("nicoletestno4@tutorabc.com")
        driver.find_element_by_id("txt_password").clear()
        driver.find_element_by_id("txt_password").send_keys("tutorabc123")
        driver.find_element_by_css_selector("div.login_button > input[type=\"submit\"]").click()
        for i in range(60):
            try:
                if self.is_element_present(By.CSS_SELECTOR, buttonSelector): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
		#選擇[教材預覽]按鈕並點下
        perviewmaterialMenu = driver.find_element_by_css_selector(".class_bottom")
        perviewmaterialButton = driver.find_element_by_css_selector(buttonSelector)
        ActionChains(driver).move_to_element(perviewmaterialMenu).click(perviewmaterialButton).perform()
        # 等到兩個視窗都開啟
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) == 2)
        # 切換到開啟的視窗
        driver.switch_to.window(driver.window_handles[1])
        # 等待直到第二個視窗的 title 有東西，表示 Ready
        WebDriverWait(driver, 10).until(lambda d: d.title != "")
		# 等到教材清單是否存在
        for i in range(60):
            try:
                if self.is_element_present(By.CSS_SELECTOR, carouselSelector): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        #time.sleep(1)
        #切換到原來視窗
        driver.switch_to.window(driver.window_handles[0])
        #點下登出按鈕
        driver.find_element_by_css_selector("div.logout_botton > a").click()
        WebDriverWait(driver, 10).until(lambda d: d.title != "")
        #測試結束
        driver.close()
        

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

    def get_sessiontime(self):
        i = datetime.datetime.now()
        if i.minute >= 27:
            result = i.strftime("%Y/%m/%d ") + str(i.hour) + ":30"
        else:
            result = i.strftime("%Y/%m/%d ") + str(i.hour-1) +  ":30"
        #print(i.minute)
        return result

if __name__ == "__main__":
    unittest.main()

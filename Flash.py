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
import base64
#python -m pip install requests
import requests
#http://lxml.de/objectify.html
#python -m pip install lxml
from lxml import objectify

class FlashSelenium(object):
    
    def __init__(self, seleniumObj, flashObjectId):
        self.seleniumObj = seleniumObj
        self.flashObjectId = flashObjectId
        self.flashJSStringPrefix = self.createJSPrefix_document(self.flashObjectId)
        
    def start(self):
        self.seleniumObj.start()

    def stop(self):
        self.seleniumObj.stop()
        
    def open(self, Url):
        self.seleniumObj.open(Url)
    
    def call(self, functionName, *parameter):
        self.flashJSStringPrefix = self.checkBrowserAndReturnJSPrefix()
        return self.seleniumObj.execute_script(self.jsForFunction(functionName, list(parameter)))
    
    #### Standard Methods ####
    
    def percent_loaded(self):
        return self.call("PercentLoaded")
    
    def is_playing(self):
        return self.call("IsPlaying")
    
    def get_variable(self, varName):
        return self.call("GetVariable", varName)
    
    def goto_frame(self, value):
        return self.call("GotoFrame", value)
    
    def load_movie(self, layerNumber, Url):
        return self.call("LoadMovie", layerNumber, Url)
    
    def pan(self, x, y, mode):
        return self.call("Pan", x, y, mode)
    
    def play(self):
        return self.call("Play")
    
    def rewind(self):
        return self.call("Rewind")
    
    def set_variable(self, name, value):
        return self.call("SetVariable", name, value)
    
    def set_zoom_rect(self, left, top, right, bottom):
        return self.call("SetZoomRect", left, top, right, bottom)
    
    def stop_play(self):
        return self.call("StopPlay")
    
    def total_frames(self):
        return self.call("TotalFrames")
    
    def zoom(self, percent):
        return self.call("Zoom", percent)
    
    #### TellTarget Methods ####
    
    def t_call_frame(self, target, frameNumber):
        return self.call("TCallFrame", target, frameNumber)
    
    def t_call_label(self, target, label):
        return self.call("TCallLabel", target, label)
    
    def t_current_frame(self, target):
        return self.call("TCurrentFrame", target)
    
    def t_current_label(self, target):
        return self.call("TCurrentLabel", target)
    
    def t_get_property(self, target, property):
        return self.call("TGetProperty", target, property)

    def t_get_property_as_number(self, target, property):
        return self.call("TGetPropertyAsNumber", target, property)
    
    def t_goto_frame(self, target, frameNumber):
        return self.call("TGotoFrame", target, frameNumber)
    
    def t_goto_label(self, target, label):
        return self.call("TGotoLabel", target, label)
    
    def t_play(self, target):
        return self.call("TPlay", target)
    
    def t_set_property(self, property, value):
        return self.call("TSetProperty", property, value)
    
    def t_stop_play(self, target):
        return self.call("TStopPlay", target)
    
    #### Standard Events ####
    
    def on_progress(self, percent):
        return self.call("OnProgress", percent)
    
    def on_ready_state_change(self, state):
        return self.call("OnReadyStateChange", state)

    #### Custom Code ####
    
    def checkBrowserAndReturnJSPrefix(self):
        #get_eval to execute_script
        #'WebDriver' object has no attribute 'get_eval'
        indexOfMicrosoft = self.seleniumObj.execute_script("navigator.appName.indexOf(\"Microsoft Internet\")");
        if indexOfMicrosoft != -1:
            return self.createJSPrefix_window_document(self.flashObjectId)
        else:
            return self.createJSPrefix_document(self.flashObjectId)
        
    def createJSPrefix_window_document(self, flashObjectId):
        return "window.document['" + flashObjectId + "'].";
    
    def createJSPrefix_document(self, flashObjectId):
        return "document['" + flashObjectId + "'].";
    
    def jsForFunction(self, functionName, *args):
        functionArgs = ""
        if len(args) > 0 and args != None :
            for arg in args[0]:
                functionArgs = functionArgs + "'" + str(arg) + "',"
            functionArgs = functionArgs[0:len(functionArgs)-1]
        return self.flashJSStringPrefix + functionName + "(" + functionArgs + ");"

class Test1(unittest.TestCase):
    def setUp(self):
        firefoxProfile = webdriver.FirefoxProfile()
        firefoxProfile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so','true')
        firefoxProfile.set_preference("plugin.state.flash", 2)
        #self.driver = webdriver.Firefox()
        self.driver = webdriver.Firefox(firefoxProfile)
        self.driver.implicitly_wait(30)
        self.base_url = "http://www4.tutorabc.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_1(self):
        #[進入教室]按鈕
        buttonSelector = ".class_bottom > a[entersession2=\"entersession2\"]" #[sessiontime=\"" + sessiontime + "\"]"
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
		#選擇[進入教室]按鈕並點下
        perviewmaterialMenu = driver.find_element_by_css_selector(".class_bottom")
        perviewmaterialButton = driver.find_element_by_css_selector(buttonSelector)
        print(perviewmaterialButton) #<selenium.webdriver.firefox.webelement.FirefoxWebElement (session="8336732c-1902-47df-ab75-ce2ef3ce54e2", element="86490f60-0cbe-4c4e-ae27-83ec49626370")>
        ActionChains(driver).move_to_element(perviewmaterialMenu).click(perviewmaterialButton).perform()
        # 等到兩個視窗都開啟 WebDriverWait(driver, 超时时长, 调用频率, 忽略异常).until(可执行方法, 超时时返回的信息)
        try:
            WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) == 2)
        except: self.fail("[進入教室]按鈕不存在，現在無法進入教室")
        # 切換到開啟的視窗
        driver.switch_to.window(driver.window_handles[1])
        # 等待直到第二個視窗的 title 有東西，表示 Ready
        try:
            WebDriverWait(driver, 10).until(lambda d: d.title != "")
        except: self.fail("第二個視窗不存在")
        # 等到教材清單是否存在
        flashApp = FlashSelenium(driver, "tutormeet")
        print(flashApp)
        try:
            # 若成功呼叫會報錯 Error: Error calling method on NPObject! 表示OK
            abc = flashApp.call("flexFileLoaded")
            print(abc)
        except: pass
        #取得 filepath 參數值
        filepath = self.get_filepath()
        print(filepath)
        #驗證上課講義
        self.check_files(filepath)
        time.sleep(10)
        #切換到原來視窗
        driver.switch_to.window(driver.window_handles[0])
        #點下登出按鈕
        driver.find_element_by_css_selector("div.logout_botton > a").click()
        #測試結束
        driver.close()

    def get_filepath(self):
        url = self.driver.execute_script("return window.location.href;") #https://www.tutormeet.com/tutormeet/tutormeet_FF.html?lang=2&data=MjAxNzA5MjUxMDAwMDk0NHwyNTk0NjV8c2Vzc2lvbjAwMDk0NHxjOTYxZDhiODAxfDF8fGFiY3wyfDA=
        data = self.driver.execute_script("return new URL(window.location.href).searchParams.get('data');") #MjAxNzA5MjUxMDAwMDk0NHwyNTk0NjV8c2Vzc2lvbjAwMDk0NHxjOTYxZDhiODAxfDF8fGFiY3wyfDA=
        realData = base64.b64decode(data).decode('utf-8') #2017092510000944|259465|session000944|c961d8b801|1||abc|2|0
        print(url)
        print(data)
        print(realData)
        splitData = realData.split("|")
        print(splitData)
        print(len(splitData))
        filepath = splitData[2] + "_" + splitData[0]
        return filepath

    def check_files(self, filepath):
        baseurl = self.driver.execute_script("return new URL('/',window.location.href);")#https://www.tutormeet.com/
        print(baseurl)
        # materialUrl & rnd 可省略
        #GET http://www.tutormeet.com/materials/php/listFiles.php?filepath=session000944_2017092218000944&materialUrl=111260&rnd=818 HTTP/1.1
        r = requests.get(baseurl+'materials/php/listFiles.php?filepath=' + filepath)
        print(r.status_code)
        print(r.content)
        directory = objectify.fromstring(r.content)
        print(objectify.dump(directory))
        fileCount = len(directory["file"])
        print(fileCount)
        if fileCount > 0:
            pass
        else:
            self.fail("投影片不存在")
	
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

if __name__ == "__main__":
    unittest.main()
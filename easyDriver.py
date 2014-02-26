#coding:utf8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
import json

class EasyDriver(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://itunesconnect.apple.com"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def login(self):
        driver = self.driver

        driver.get("https://itunesconnect.apple.com")
        driver.find_element_by_id("accountname").clear()
        driver.find_element_by_id("accountname").send_keys("fjzxd01@163.com")
        driver.find_element_by_id("accountpassword").clear()
        driver.find_element_by_id("accountpassword").send_keys("77Iloveyou")
        
        """
        for i in range(5):
            try:
                if driver.find_element_by_name("1.Continue"):
                    break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        """

        goIn = driver.find_elements_by_name("1.Continue")
        print "continue", goIn
        ret = goIn[1].click()
        print "click ret", ret
        driver.find_element_by_link_text("Manage Your Apps").click()
        driver.find_element_by_css_selector("div.app-icon > img").click()
        driver.find_element_by_link_text("Manage Game Center").click()

    def test_easy_driver(self):
        self.login()
        driver = self.driver

        f = open('allTask')
        alltask = f.read()
        alltask = json.loads(alltask)
        #从1 开始
        taskId = 1

        for t in alltask:
            for smallId in xrange(1, 4):
                #driver.get("https://itunesconnect.apple.com/WebObjects/iTunesConnect.woa/wo/119.0.0.7.3.0.9.3.3.1.0.13.3.1.1.11.7.13.1.9.1")

                driver.find_element_by_id("addAchievementEnabled").click()
                driver.find_element_by_id("internalName").clear()
                driver.find_element_by_id("internalName").send_keys(t[0]+str(smallId))
                driver.find_element_by_id("vendorIdentifier").clear()
                driver.find_element_by_id("vendorIdentifier").send_keys("lianyun%d.%d"%(taskId, smallId))
                driver.find_element_by_id("achievementPoints").clear()
                driver.find_element_by_id("achievementPoints").send_keys("1")
                driver.find_element_by_id("visibleTrue").click()
                driver.find_element_by_xpath("//div[@id='gc-add-language-button']/span").click()
                for i in range(60):
                    try:
                        if self.is_element_present(By.XPATH, "//select[@id='languageSelector']"): break
                    except: pass
                    time.sleep(1)
                else: self.fail("time out")
                # ERROR: Caught exception [ReferenceError: selectLocator is not defined]

                language = driver.find_element_by_id("languageSelector")
                allOptions = language.find_elements_by_tag_name("option")
                allOptions[17].click()

                driver.find_element_by_id("achievementDetailName").clear()

                numToEng = {
                        1:" I",
                        2:" II",
                        3:" III"
                        }
                driver.find_element_by_id("achievementDetailName").send_keys(t[1]+numToEng[smallId])
                driver.find_element_by_id("achievementDetailBeforeEarnedDescription").clear()
                driver.find_element_by_id("achievementDetailBeforeEarnedDescription").send_keys(t[2+smallId-1])
                driver.find_element_by_id("achievementDetailAfterEarnedDescription").clear()
                driver.find_element_by_id("achievementDetailAfterEarnedDescription").send_keys(t[2+smallId-1])
                #driver.find_element_by_id("fileInput_achievementImage").clear()
                #driver.find_element_by_id("fileInput_achievementImage").click()
                driver.find_element_by_id("fileInput_achievementImage").send_keys(("C:\\Users\\Administrator\\Desktop\\achieve.png"))
                while True:
                    time.sleep(10)
                    print  "finish Sleep begin click"
                    try:
                        but = driver.find_element_by_id("lightboxSaveButtonEnabled")
                        but.click()
                        print "finish click"
                        break
                    except NoSuchElementException, e:
                        print "not button"

                driver.find_element_by_name("0.0.7.3.0.9.3.1.1.1.0.21.2.0.1.1.1").click()
            taskId += 1
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
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

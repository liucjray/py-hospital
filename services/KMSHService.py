import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

from config.config import *
from helpers.Common import *
from services.TelegramBot import *


class KMSHService:
    def __init__(self):
        self.reset()

    def reset(self):
        config = dict(get_config())
        self.chrome_driver_path = dict_get(config, 'WEBDRIVER.CHROME_DRIVER_PATH', None)
        self.user_id = dict_get(config, 'TWID.ABBY_ID', None)
        self.tg = TelegramBot({})
        self.chat_id = dict_get(config, 'TG.CHAT_ID_RABBY', None)
        self.browser = self.get_browser()

    def get_browser(self):
        options = ChromeOptions()
        options.headless = True
        return webdriver.Chrome(self.chrome_driver_path, options=options)

    def check_required(self):
        check_list = [
            self.chrome_driver_path,
            self.user_id,
            self.chat_id
        ]
        # 檢查必要參數是否存在
        for require in check_list:
            if require is None:
                raise Exception('require is None.')

    def close_windows(self):
        # 關閉所有視窗
        for windows in self.browser.window_handles:
            self.browser.switch_to.window(windows)
            self.browser.close()

    def alert_accept(self):
        # 進入後的預設彈窗
        a1 = self.browser.switch_to.alert
        a1.accept()

    def visit(self):
        login_url = 'http://www.kmsh.org.tw/online/index.asp'
        self.browser.get(login_url)
        self.alert_accept()

    def switch_to_iframe(self, name):
        # 切換至 iframe 操作
        self.browser.switch_to.frame(name)

    def login(self):
        # 輸入 ID 後點擊送出表單
        self.browser.find_element_by_id('UC_NetRegFirst2_TextBox_ChartOrID').send_keys(self.user_id)
        self.browser.find_element_by_id('UC_NetRegFirst2_Button_Submit').click()
        self.alert_accept()

    def enterDept(self):
        # 進入科別
        xpathOfFuChanKe = '//*[@id="UC_NetRegDept1_UC_婦產科_UC_LinkList1_Panel_Link"]/table/tbody/tr/td/a'
        clickFuChanKe = self.browser.find_element_by_xpath(xpathOfFuChanKe).click()

    def enterTab(self):
        # 選取夜間頁籤
        xpathTabOfNight = '//*[@id="UC_NetRegSchedule1_Link_Night"]'
        clickTabOfNight = self.browser.find_element_by_xpath(xpathTabOfNight).click()

    def selectDoctorOfDate(self):
        # 選取掛號醫生&日期
        # xpathDoctorOfDate = '//*[@id="UC_NetRegSchedule1_ctl00_Panel_Schedule"]/table/tbody/tr[1]/td[3]/a'
        xpathDoctorOfDate = '//*[@id="UC_NetRegSchedule1_ctl00_Panel_Schedule"]/table/tbody/tr[1]/td[2]/a'
        targetDoctorOfDate = self.browser.find_element_by_xpath(xpathDoctorOfDate).click()

    def switchToRegPage(self):
        # 切換至掛號系統表單 [另開視窗, 取最後一個 window]
        self.browser.switch_to.window(self.browser.window_handles[-1])

    def sendRegForm(self):
        # 送出掛號
        self.browser.find_element_by_id('Button_SendReg').click()

    def checkRegResult(self):
        # 確認是否掛號成功
        reg_result = self.browser \
            .find_element_by_xpath('//*[@id="Label_NetRegStatus"]/font') \
            .get_attribute('innerText')
        return reg_result == "掛號成功"

    def send_message_for_reg_success(self):
        self.tg.send_message(self.chat_id, "掛號成功")

    def send_message_for_reg_fail(self):
        self.tg.send_message(self.chat_id, "掛號失敗")

    def clean(self):
        self.browser.quit()
        self.reset()

    def handle(self):
        self.check_required()
        try:
            self.visit()
            self.switch_to_iframe('mainframe')
            self.login()
            self.enterDept()
            self.enterTab()
            self.selectDoctorOfDate()
            self.switchToRegPage()
            self.sendRegForm()
            if self.checkRegResult() is True:
                self.send_message_for_reg_success()
            else:
                self.send_message_for_reg_fail()

        except Exception as e:
            self.clean()
            print(e)

        finally:
            self.close_windows()
            self.clean()

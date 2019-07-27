import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

from config.config import *
from helpers.Common import *
from services.TelegramBot import *


class KMSHService:
    def __init__(self, settings=None):
        self.settings = settings
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
        if dict_get(self.settings, 'bg', None) is True:
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

    def enter_dept(self):
        # 進入科別
        selector_of_depts = 'a.treea'
        depts = self.browser.find_elements_by_css_selector(selector_of_depts)
        for dept in depts:
            if dept.text == dict_get(self.settings, 'dept', None):
                dept.click()
                return True
        return False

    def enter_tab(self):
        # 選取時段頁籤
        noon_type = dict_get(self.settings, 'noonType', None)
        xpath_tab_of_noon_type = '//*[@id="UC_NetRegSchedule1_Link_{}"]'.format(noon_type)
        self.browser.find_element_by_xpath(xpath_tab_of_noon_type).click()
        return True

    def select_doctor_of_date(self):
        # 取得頁面上所有的醫師看診時間
        selector_doctor_of_date = '#UC_NetRegSchedule1_ctl00_Panel_Schedule table tr td'
        doctors_of_date = self.browser.find_elements_by_css_selector(selector_doctor_of_date)

        for doctor_of_date in doctors_of_date:

            # 若格子內無資料則跳過
            if len(doctor_of_date.get_attribute('innerHTML').strip()) == 0:
                continue

            # 第一個 span 為醫師看診日期
            if doctor_of_date.find_elements_by_css_selector('span')[0].text != dict_get(self.settings, 'date', None):
                continue

            # link 為掛號連結, 這邊為了確認是否 exist 用了 find_elements_by_css 避開直接查找元素的錯誤
            if len(doctor_of_date.find_elements_by_css_selector('a')) == 0:
                continue

            # 若查找條件過了, 即可確認元素存在可直接取用
            if doctor_of_date.find_element_by_css_selector('a').text != dict_get(self.settings, 'doctor', None):
                continue

            # 若上述條件都通過時才會點選到下一步
            doctor_of_date.find_element_by_css_selector('a').click()
            return True

        return False

    def switch_to_reg_page(self):
        # 切換至掛號系統表單 [另開視窗, 取最後一個 window]
        self.browser.switch_to.window(self.browser.window_handles[-1])

    def send_reg_form(self):
        # 送出掛號
        self.browser.find_element_by_id('Button_SendReg').click()

    def check_reg_result(self):
        # 確認是否掛號成功
        xpath_reg_result_msg = '//*[@id="Label_NetRegStatus"]/font'
        reg_result = self.browser.find_element_by_xpath(xpath_reg_result_msg).get_attribute('innerText')
        return reg_result == "掛號成功"

    def send_message_for_reg_success(self):
        msg = 'Dr.{} 於 {} 預約掛號成功!'.format(
            dict_get(self.settings, 'doctor', None),
            dict_get(self.settings, 'date', None)
        )
        self.tg.send_message(self.chat_id, msg)

    def send_message_for_reg_fail(self):
        msg = 'Dr.{} 於 {} 預約掛號失敗!'.format(
            dict_get(self.settings, 'doctor', None),
            dict_get(self.settings, 'date', None)
        )
        self.tg.send_message(self.chat_id, msg)

    def clean(self):
        self.browser.quit()
        self.reset()

    def handle(self):
        self.check_required()
        try:
            self.visit()
            self.switch_to_iframe('mainframe')
            self.login()
            self.enter_dept()
            self.enter_tab()
            if self.select_doctor_of_date() is False:
                msg = 'Dr.{} 於 {} 目前無法預約掛號!'.format(
                    dict_get(self.settings, 'doctor', None),
                    dict_get(self.settings, 'date', None)
                )
                raise Exception(msg)
            self.switch_to_reg_page()
            self.send_reg_form()
            if self.check_reg_result() is True:
                self.send_message_for_reg_success()
            else:
                self.send_message_for_reg_fail()

        except Exception as e:
            self.clean()
            print(e)

        finally:
            self.close_windows()
            self.clean()

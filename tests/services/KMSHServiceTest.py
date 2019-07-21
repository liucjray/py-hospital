import unittest
from services.KMSHService import *


class KMSHServiceTest(unittest.TestCase):
    def setUp(self):
        self.kmsh = KMSHService()
        self.kmsh.visit()
        self.kmsh.switch_to_iframe('mainframe')
        self.kmsh.login()

    def test_enter_dept(self):
        self.kmsh.settings = {'dept': '婦產科'}
        result = self.kmsh.enter_dept()
        self.assertTrue(result)

    def test_enter_tab(self):
        self.kmsh.settings = {'dept': '婦產科'}
        self.kmsh.enter_dept()
        # AM
        self.kmsh.settings['noonType'] = 'AM'
        result = self.kmsh.enter_tab()
        self.assertTrue(result)
        # PM
        self.kmsh.settings['noonType'] = 'PM'
        result = self.kmsh.enter_tab()
        self.assertTrue(result)
        # Night
        self.kmsh.settings['noonType'] = 'Night'
        result = self.kmsh.enter_tab()
        self.assertTrue(result)

    def test_select_doctor_of_date(self):
        self.kmsh.settings = {'dept': '婦產科'}
        self.kmsh.enter_dept()

        self.kmsh.settings['noonType'] = 'Night'
        self.kmsh.enter_tab()

        self.kmsh.settings['date'] = '2019/7/23'
        self.kmsh.settings['doctor'] = '張慧名'
        result = self.kmsh.select_doctor_of_date()
        self.assertFalse(result)

        self.kmsh.settings['date'] = '2019/7/22'
        self.kmsh.settings['doctor'] = '龍震宇'
        result = self.kmsh.select_doctor_of_date()
        self.assertFalse(result)

        self.kmsh.settings['date'] = '2019/7/24'
        self.kmsh.settings['doctor'] = '王秋麟'
        result = self.kmsh.select_doctor_of_date()
        self.assertTrue(result)
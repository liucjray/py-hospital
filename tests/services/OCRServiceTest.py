import unittest
from services.OCRService import *

import re


class OCRServiceTest(unittest.TestCase):
    def setUp(self):
        self.ocr = OCRService()
        self.ocr.del_all_imgs()

    def test_download_img(self):
        for x in range(30):
            self.ocr.download_img()

    def test_pattern(self):
        pattern = self.ocr.get_pattern()

        ans = 'AAAA'
        matches = re.findall(pattern, ans)
        new_ans = ''.join(matches)
        self.assertEqual(new_ans, 'AAAA')

        ans = 'Az12'
        matches = re.findall(pattern, ans)
        new_ans = ''.join(matches)
        self.assertEqual(new_ans, 'Az12')

        ans = '^123ABC&*(^^'
        matches = re.findall(pattern, ans)
        new_ans = ''.join(matches)
        self.assertEqual(new_ans, '123ABC')

        ans = 'VAs)'
        matches = re.findall(pattern, ans)
        new_ans = ''.join(matches)
        self.assertEqual(new_ans, 'VAs)')

        ans = 'MAW.'
        matches = re.findall(pattern, ans)
        new_ans = ''.join(matches)
        self.assertEqual(new_ans, 'MAW.')

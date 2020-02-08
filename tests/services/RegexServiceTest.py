import unittest

import re


class RegexServiceTest(unittest.TestCase):
    def test_findall(self):
        string = 'hello 123, world 456.'
        pattern = '\d+'
        result = re.findall(pattern, string)
        self.assertEqual(['123', '456'], result)

    def test_split(self):
        string = 'Twelve:12 Eighty nine:89.'
        pattern = '\d+'
        result = re.split(pattern, string)
        self.assertEqual(['Twelve:', ' Eighty nine:', '.'], result)

    def test_split_not_found(self):
        string = 'Twelve, Eighty nine'
        pattern = 'no match'
        result = re.split(pattern, string)
        self.assertEqual([string], result)

    def test_split_max_number(self):
        string = 'Twelve:12 Eighty nine:89.'
        pattern = '\d+'
        max_split_num = 1
        result = re.split(pattern, string, max_split_num)
        self.assertEqual(['Twelve:', ' Eighty nine:89.'], result)

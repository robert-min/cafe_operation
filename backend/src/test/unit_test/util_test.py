from unittest import TestCase
from enum import Enum
from lib.util import extract_korean_initial

class Mock(Enum):
    TEXT = "아메리카노"
    

class UtilsTestCase(TestCase):
    def test_extract_korean_initial(self):
        result = extract_korean_initial(Mock.TEXT.value)
        self.assertEqual('ㅇㅁㄹㅋㄴ', result)
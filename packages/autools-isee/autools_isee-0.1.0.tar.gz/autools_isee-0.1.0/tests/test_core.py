import unittest
from autools.core import reverse_string, count_vowels, is_palindrome

class TestStringUtils(unittest.TestCase):

    def test_reverse(self):
        result = reverse_string("hello")
        self.assertEqual(result, "olleh")

    def test_vowel_count(self):
        result = count_vowels("Python")
        self.assertEqual(result, 1)

    def test_palindrome(self):
        result = is_palindrome("A man a plan a canal Panama")
        self.assertTrue(result)  # 假设 is_palindrome 返回 True 表示是回文

if __name__ == '__main__':
    unittest.main()

import os
import sys
import unittest

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from src.pyenvelop.exceptions import CheckedException, UnCheckedException

class TestCheckedException(unittest.TestCase):
    def test_init(self):
        exception = CheckedException("测试异常")
        self.assertEqual(str(exception), "测试异常")

class TestUnCheckedException(unittest.TestCase):
    def test_init_with_message(self):
        exception = UnCheckedException("测试异常")
        self.assertEqual(str(exception), "测试异常")
        self.assertIsNone(exception.code)
        self.assertIsNone(exception.cause)

    def test_init_with_code(self):
        exception = UnCheckedException("测试异常", error_code="E001")
        self.assertEqual(str(exception), "测试异常")
        self.assertEqual(exception.code, "E001")
        self.assertIsNone(exception.cause)

    def test_init_with_cause(self):
        cause = ValueError("原始异常")
        exception = UnCheckedException("测试异常", cause=cause)
        self.assertEqual(str(exception), "测试异常")
        self.assertIsNone(exception.code)
        self.assertEqual(exception.cause, cause)

    def test_init_with_all(self):
        cause = ValueError("原始异常")
        exception = UnCheckedException("测试异常", error_code="E001", cause=cause)
        self.assertEqual(str(exception), "测试异常")
        self.assertEqual(exception.code, "E001")
        self.assertEqual(exception.cause, cause)

    def test_code_property(self):
        exception = UnCheckedException("测试异常")
        exception.code = "E001"
        self.assertEqual(exception.code, "E001")

    def test_cause_property(self):
        exception = UnCheckedException("测试异常")
        cause = ValueError("原始异常")
        exception.cause = cause
        self.assertEqual(exception.cause, cause)

    def test_invalid_cause_type(self):
        """测试无效的cause类型"""
        with self.assertRaises(TypeError):
            UnCheckedException("测试异常", cause="invalid")
            
        exception = UnCheckedException("测试异常")
        with self.assertRaises(TypeError):
            exception.cause = "invalid"

if __name__ == '__main__':
    unittest.main() 
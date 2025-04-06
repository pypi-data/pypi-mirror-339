import os
import sys
import unittest

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from src.pyenvelop.core import Data, DataSet

class TestData(unittest.TestCase):
    def setUp(self):
        self.test_data = Data(name="test", value="123")
        self.test_dataset = DataSet([{"id": "1", "name": "test1"}, {"id": "2", "name": "test2"}])
        self.complex_data = Data(users=self.test_dataset)
        self.data = Data()

    def test_init_with_string(self):
        data = Data(name="test")
        self.assertEqual(data.get_string_item("name"), "test")

    def test_init_with_int(self):
        data = Data(count=123)
        self.assertEqual(data.get_string_item("count"), "123")

    def test_set_string(self):
        self.test_data.set_string("new_key", "new_value")
        self.assertEqual(self.test_data.get_string_item("new_key"), "new_value")

    def test_set_dataset(self):
        self.test_data.set_dataset("dataset_key", self.test_dataset)
        self.assertIsInstance(self.test_data["dataset_key"], DataSet)

    def test_to_json(self):
        json_str = self.test_data.to_json()
        self.assertIn('"name":"test"', json_str)
        self.assertIn('"value":"123"', json_str)

    def test_to_xml(self):
        xml_str = self.test_data.to_xml()
        self.assertIn('<name>test</name>', xml_str)
        self.assertIn('<value>123</value>', xml_str)
        
        complex_xml = self.complex_data.to_xml()
        self.assertIn('<users>', complex_xml)
        self.assertIn('<row>', complex_xml)
        self.assertIn('<id>1</id>', complex_xml)
        self.assertIn('<name>test1</name>', complex_xml)
        
    def test_special_characters(self):
        """测试特殊字符在JSON/XML中的处理"""
        data = Data(name="test\"with\"quotes", value="line\nbreak")
        json_str = data.to_json()
        self.assertIn('"name":"test\\"with\\"quotes"', json_str)
        self.assertIn('"value":"line\\nbreak"', json_str)
        
        xml_str = data.to_xml()
        self.assertIn('<name>test&quot;with&quot;quotes</name>', xml_str)
        self.assertIn('<value>line\nbreak</value>', xml_str)
        
    def test_none_values(self):
        """测试None值的处理"""
        data = Data()
        data["null_key"] = None
        self.assertIsNone(data.get_string_item("null_key"))
        
    def test_float_values(self):
        """测试浮点数类型的处理"""
        data = Data(price=123.45)
        self.assertEqual(data.get_string_item("price"), "123.45")
        self.assertEqual(data.get_big_decimal("price"), 123.45)
        
    def test_large_numbers(self):
        """测试大数值的转换"""
        data = Data(big_num="9223372036854775807")  # 最大长整型
        self.assertEqual(data.get_long_item("big_num"), 9223372036854775807)
        
        data = Data(overflow="9223372036854775808")  # 超出长整型范围
        self.assertIsNone(data.get_long_item("overflow"))

    def test_init_with_dict(self):
        """测试使用字典初始化"""
        test_dict = {"key1": "value1", "key2": 123}
        data = Data(test_dict)
        self.assertEqual(data.get_string("key1"), "value1")
        self.assertEqual(data.get_int("key2"), 123)

    def test_dict_data(self):
        """测试字典类型数据"""
        test_dict = {"nested": {"key": "value"}, "list": [1, 2, 3]}
        self.data.set_dict("test_dict", test_dict)
        result = self.data.get_dict("test_dict")
        self.assertEqual(result["nested"]["key"], "value")
        self.assertEqual(result["list"], [1, 2, 3])

    def test_list_data(self):
        """测试列表类型数据"""
        test_list = [1, "2", 3.0, True, {"key": "value"}]
        self.data.set_list("test_list", test_list)
        result = self.data.get_list("test_list")
        self.assertEqual(result, test_list)

    def test_nested_data(self):
        """测试嵌套数据结构"""
        nested_data = {
            "level1": {
                "level2": {
                    "level3": {
                        "value": "test"
                    }
                }
            }
        }
        self.data.set_dict("nested", nested_data)
        result = self.data.get_dict("nested")
        self.assertEqual(result["level1"]["level2"]["level3"]["value"], "test")

    def test_complex_data_structure(self):
        """测试复杂数据结构"""
        complex_data = {
            "string": "test",
            "number": 123,
            "float": 3.14,
            "boolean": True,
            "list": [1, 2, 3],
            "dict": {"key": "value"},
            "nested": {
                "list": [{"id": 1}, {"id": 2}],
                "dict": {"key": {"value": "test"}}
            }
        }
        self.data.set_dict("complex", complex_data)
        result = self.data.get_dict("complex")
        self.assertEqual(result, complex_data)

if __name__ == '__main__':
    unittest.main() 
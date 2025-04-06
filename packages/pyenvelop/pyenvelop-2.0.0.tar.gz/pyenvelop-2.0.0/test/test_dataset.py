import os
import sys
import unittest

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from src.pyenvelop.core import DataSet

class TestDataSet(unittest.TestCase):
    def setUp(self):
        """初始化测试环境"""
        self.test_data = [
            {"id": "1", "name": "test1"},
            {"id": "2", "name": "test2"},
            {"id": "3", "name": "test3"}
        ]
        self.dataset = DataSet(self.test_data)

    def test_init(self):
        self.assertEqual(len(self.dataset), 3)
        self.assertEqual(self.dataset[0]["id"], "1")
        self.assertEqual(self.dataset[1]["name"], "test2")

    def test_get_row(self):
        row = self.dataset.get_row(0)
        self.assertEqual(row["id"], "1")
        self.assertIsNone(self.dataset.get_row(999))

    def test_set_row(self):
        new_row = {"id": "3", "name": "test3"}
        self.dataset.set_row(new_row)
        self.assertEqual(len(self.dataset), 3)
        self.assertEqual(self.dataset[2]["id"], "3")

    def test_to_json(self):
        json_str = self.dataset.to_json()
        self.assertIn('"id":"1"', json_str)
        self.assertIn('"name":"test1"', json_str)

    def test_to_xml(self):
        xml_str = self.dataset.to_xml()
        self.assertIn('<row>', xml_str)
        self.assertIn('<id>1</id>', xml_str)
        self.assertIn('<name>test1</name>', xml_str)
        self.assertIn('<id>2</id>', xml_str)
        self.assertIn('<name>test2</name>', xml_str)
        
    def test_index_boundary(self):
        """测试索引边界情况"""
        self.assertIsNone(self.dataset.get_row(-1))
        self.assertIsNone(self.dataset.get_row(3))
        self.assertIsNone(self.dataset.get_row(999))
        
    def test_empty_dataset(self):
        """测试空数据集"""
        empty_dataset = DataSet()
        self.assertEqual(len(empty_dataset), 0)
        self.assertEqual(empty_dataset.to_json(), "[]")
        self.assertEqual(empty_dataset.to_xml(), "")
        
    def test_special_characters(self):
        """测试特殊字符在JSON/XML中的处理"""
        special_dataset = DataSet([{"id": "1", "name": "test\"with\"quotes"}])
        json_str = special_dataset.to_json()
        self.assertIn('"name":"test\\"with\\"quotes"', json_str)
        
        xml_str = special_dataset.to_xml()
        self.assertIn('<name>test&quot;with&quot;quotes</name>', xml_str)

    def test_batch_operations(self):
        """测试批量操作"""
        # 批量设置行
        new_rows = [
            {"id": "4", "name": "test4"},
            {"id": "5", "name": "test5"}
        ]
        self.dataset.set_rows(new_rows)
        self.assertEqual(len(self.dataset), 5)
        self.assertEqual(self.dataset.get_row(3)["name"], "test4")
        self.assertEqual(self.dataset.get_row(4)["name"], "test5")

        # 批量获取行
        rows = self.dataset.get_rows(1, 3)
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]["id"], "2")
        self.assertEqual(rows[2]["id"], "4")

    def test_merge_datasets(self):
        """测试数据集合并"""
        # 创建另一个数据集
        other_data = [
            {"id": "4", "name": "test4"},
            {"id": "5", "name": "test5"}
        ]
        other_dataset = DataSet(other_data)

        # 合并数据集
        self.dataset.merge(other_dataset)
        self.assertEqual(len(self.dataset), 5)
        self.assertEqual(self.dataset.get_row(3)["name"], "test4")
        self.assertEqual(self.dataset.get_row(4)["name"], "test5")

    def test_merge_empty_dataset(self):
        """测试合并空数据集"""
        empty_dataset = DataSet()
        self.dataset.merge(empty_dataset)
        self.assertEqual(len(self.dataset), 3)

    def test_merge_with_empty_dataset(self):
        """测试空数据集合并"""
        empty_dataset = DataSet()
        empty_dataset.merge(self.dataset)
        self.assertEqual(len(empty_dataset), 3)
        self.assertEqual(empty_dataset.get_row(0)["id"], "1")

if __name__ == '__main__':
    unittest.main() 
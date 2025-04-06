import os
import sys
import unittest

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from src.pyenvelop.core import Entity, Data, DataSet

class TestEntity(unittest.TestCase):
    def setUp(self):
        """初始化测试环境"""
        self.entity = Entity()
        self.test_data = Data({"id": "1", "name": "test"})
        self.test_dataset = DataSet([{"id": "1", "name": "test1"}])

    def test_init(self):
        self.assertEqual(len(self.entity), 0)

    def test_get_node(self):
        self.entity.set_node(self.test_data, node="test")
        node = self.entity.get_node("test")
        self.assertEqual(node["id"], "1")
        self.assertIsNone(self.entity.get_node("nonexistent"))

    def test_get_node_dataset(self):
        self.entity.set_node_dataset("test", self.test_dataset)
        dataset = self.entity.get_node_dataset("test")
        self.assertEqual(len(dataset), 1)
        self.assertEqual(dataset[0]["id"], "1")
        self.assertIsNone(self.entity.get_node_dataset("nonexistent"))

    def test_get_node_item(self):
        self.entity.set_node(self.test_data, node="test")
        value = self.entity.get_node_item("id", node="test")
        self.assertEqual(value, "1")
        self.assertIsNone(self.entity.get_node_item("id", node="nonexistent"))

    def test_set_node(self):
        self.entity.set_node(self.test_data, node="test")
        self.assertEqual(self.entity.get_node("test")["id"], "1")

    def test_set_node_dataset(self):
        self.entity.set_node_dataset("test", self.test_dataset)
        dataset = self.entity.get_node_dataset("test")
        self.assertEqual(len(dataset), 1)
        self.assertEqual(dataset[0]["id"], "1")

    def test_set_node_item(self):
        self.entity.set_node_item("id", "1", node="test")
        self.assertEqual(self.entity.get_node_item("id", node="test"), "1")

    def test_to_json(self):
        self.entity.set_node(self.test_data, node="test")
        json_str = self.entity.to_json()
        self.assertIn('"test"', json_str)
        self.assertIn('"id":"1"', json_str)

    def test_to_xml(self):
        self.entity.set_node(self.test_data, node="test")
        xml_str = self.entity.to_xml()
        self.assertIn('<test>', xml_str)
        self.assertIn('<id>1</id>', xml_str)
        
    def test_none_values(self):
        """测试None值处理"""
        self.entity.set_node(None, node="test")
        self.assertIsNone(self.entity.get_node("test"))
        
        self.entity.set_node_dataset("test", None)
        self.assertIsNone(self.entity.get_node_dataset("test"))
        
        self.entity.set_node_item("id", None, node="test")
        self.assertIsNone(self.entity.get_node_item("id", node="test"))
        
    def test_special_characters(self):
        """测试特殊字符在JSON/XML中的处理"""
        special_data = Data({"id": "1", "name": "test\"with\"quotes"})
        self.entity.set_node(special_data, node="test")
        
        json_str = self.entity.to_json()
        self.assertIn('"name":"test\\"with\\"quotes"', json_str)
        
        xml_str = self.entity.to_xml()
        self.assertIn('<test>', xml_str)
        self.assertIn('<name>test&quot;with&quot;quotes</name>', xml_str)
        self.assertIn('</test>', xml_str)
        
    def test_empty_entity(self):
        """测试空实体"""
        empty_entity = Entity()
        self.assertEqual(empty_entity.to_json(), "{}")
        self.assertEqual(empty_entity.to_xml(), "")
        
    def test_str_representation(self):
        """测试字符串表示"""
        self.entity.set_node(self.test_data, node="test")
        str_repr = str(self.entity)
        self.assertIn("test", str_repr)
        self.assertIn("id", str_repr)
        self.assertIn("name", str_repr)

    def test_nested_node_structure(self):
        """测试嵌套节点结构"""
        # 创建嵌套节点
        child_node = Entity()
        child_node.set_node_item("value", "test", node="child")
        self.entity.set_node(child_node, node="parent")
        
        # 验证嵌套节点
        parent = self.entity.get_node("parent")
        self.assertIsNotNone(parent)
        self.assertEqual(parent.get_node_item("value", node="child"), "test")

    def test_deep_nested_structure(self):
        """测试深层嵌套结构"""
        # 创建三层嵌套结构
        level3 = Entity()
        level3.set_node_item("value", "test", node="level3")
        
        level2 = Entity()
        level2.set_node(level3, node="level3")
        
        level1 = Entity()
        level1.set_node(level2, node="level2")
        
        self.entity.set_node(level1, node="level1")
        
        # 验证嵌套结构
        result = self.entity.get_node("level1").get_node("level2").get_node("level3").get_node_item("value", node="level3")
        self.assertEqual(result, "test")

    def test_node_deletion(self):
        """测试节点删除"""
        # 设置节点
        self.entity.set_node(self.test_data, node="test")
        self.assertIsNotNone(self.entity.get_node("test"))
        
        # 删除节点
        self.entity.delete_node("test")
        self.assertIsNone(self.entity.get_node("test"))

    def test_nested_node_deletion(self):
        """测试嵌套节点删除"""
        # 创建嵌套结构
        child = Entity()
        child.set_node_item("value", "test", node="child")
        self.entity.set_node(child, node="parent")
        
        # 删除父节点
        self.entity.delete_node("parent")
        self.assertIsNone(self.entity.get_node("parent"))

    def test_delete_nonexistent_node(self):
        """测试删除不存在的节点"""
        self.entity.delete_node("nonexistent")
        self.assertIsNone(self.entity.get_node("nonexistent"))

if __name__ == '__main__':
    unittest.main() 
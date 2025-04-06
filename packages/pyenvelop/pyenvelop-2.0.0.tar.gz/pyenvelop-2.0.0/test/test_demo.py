import os
import sys
import unittest

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from src.pyenvelop.core import Data, DataSet, Envelop, EnvelopHead, EnvelopBody

class TestEnvelopDemo(unittest.TestCase):
    def setUp(self):
        """测试前的准备工作"""
        self.envelop = Envelop()
        self.header = EnvelopHead()
        self.body = EnvelopBody()
        self.data = Data()
        self.dataset = DataSet([{"set_k1": "set_v1", "set_k2": "set_v2"}])

    def test_envelop_basic(self):
        """测试信封基本功能"""
        # 设置头部
        self.header.set_node_item("success", "true")
        self.header.set_node_item("message", "测试成功")
        self.envelop.header = self.header

        # 设置主体
        self.data.set_string("key1", "value1")
        self.data.set_string("key2", "value2")
        self.body.set_node(self.data, node="test_data")
        self.envelop.body = self.body

        # 验证头部
        self.assertEqual(self.envelop.header.get_node_item("success"), "true")
        self.assertEqual(self.envelop.header.get_node_item("message"), "测试成功")

        # 验证主体
        test_data = self.envelop.body.get_node("test_data")
        self.assertEqual(test_data.get_string("key1"), "value1")
        self.assertEqual(test_data.get_string("key2"), "value2")

    def test_envelop_construction(self):
        """测试信封的构建过程"""
        # 设置头部节点
        self.header.set_node_item("execute", "query", node="abc")
        
        # 设置数据
        self.data.set_string("k2", "v2")
        self.header.set_node(self.data, node="default")
        
        # 设置数据集
        self.header.set_node_dataset("dataset", self.dataset)
        self.header.set_node_dataset("sample", self.dataset)
        
        # 设置信封头部
        self.envelop.set_header(self.header)
        
        # 验证结果
        header = self.envelop.header
        self.assertIsNotNone(header)
        self.assertEqual(header.get_node_item("execute", node="abc"), "query")
        self.assertEqual(header.get_node("default")["k2"], "v2")
        self.assertEqual(len(header.get_node_dataset("dataset")), 1)
        self.assertEqual(len(header.get_node_dataset("sample")), 1)

    def test_envelop_serialization(self):
        """测试信封的序列化和反序列化"""
        # 设置头部节点
        self.header.set_node_item("execute", "query", node="abc")
        
        # 设置数据
        self.data.set_string("k2", "v2")
        self.header.set_node(self.data, node="default")
        
        # 设置数据集
        self.header.set_node_dataset("dataset", self.dataset, node="dataset")
        self.header.set_node_dataset("dataset", self.dataset, node="test_core")
        
        # 设置信封头部
        self.envelop.set_header(self.header)
        
        # 测试点1: 转换为字典
        dict_data = self.envelop.to_dict()
        self.assertIn('header', dict_data)
        self.assertIn('abc', dict_data['header'])
        self.assertIn('default', dict_data['header'])
        self.assertIn('dataset', dict_data['header'])
        self.assertIn('test_core', dict_data['header'])
        
        # 测试点2: 获取默认节点
        default_node = self.envelop.get_header().get_node()
        self.assertIn('<k2>v2</k2>', str(default_node))
        
        # 测试点3: 获取指定节点
        abc_node = self.envelop.get_header().get_node("abc")
        self.assertIn('<execute>query</execute>', str(abc_node))
        
        # 测试点4: 获取节点项
        k2_value = self.envelop.get_header().get_node_item("k2", node="default")
        self.assertEqual(k2_value, "v2")
        
        # 测试点5: 获取数据集
        test_core_dataset = self.envelop.get_header().get_node_dataset("dataset", node="test_core")
        self.assertIn('<set_k1>set_v1</set_k1>', str(test_core_dataset))
        self.assertIn('<set_k2>set_v2</set_k2>', str(test_core_dataset))
        
        # 测试点6: 获取另一个数据集
        dataset_node = self.envelop.get_header().get_node_dataset("dataset", node="dataset")
        self.assertIn('<set_k1>set_v1</set_k1>', str(dataset_node))
        self.assertIn('<set_k2>set_v2</set_k2>', str(dataset_node))
        
        # 测试点7: 转换为字典
        json_data = self.envelop.to_dict()
        self.assertIn('header', json_data)
        self.assertIn('abc', json_data['header'])
        self.assertIn('default', json_data['header'])
        self.assertIn('dataset', json_data['header'])
        self.assertIn('test_core', json_data['header'])
        
        # 测试点8: 从字典重建信封
        envelop2 = Envelop(**json_data)
        self.assertEqual(self.envelop.to_json(), envelop2.to_json())

    def test_envelop_with_body(self):
        """测试带主体的信封构建"""
        # 设置头部数据
        data = Data()
        data.set_string("success", "true")
        data.set_string("message", "执行成功")
        self.header.set_node(data, node="default")
        
        # 设置主体数据
        self.body.set_node_item("name", "linzhiwei")
        self.body.set_node_item("age", "18")
        self.body.set_node_dataset("dataset", self.dataset)
        
        # 设置信封
        self.envelop.set_header(self.header)
        self.envelop.body = self.body
        
        # 验证结果
        json_str = self.envelop.to_json()
        self.assertIn('"header"', json_str)
        self.assertIn('"body"', json_str)
        self.assertIn('"success":"true"', json_str)
        self.assertIn('"message":"执行成功"', json_str)
        self.assertIn('"name":"linzhiwei"', json_str)
        self.assertIn('"age":"18"', json_str)
        self.assertIn('"dataset":[{"set_k1":"set_v1","set_k2":"set_v2"}]', json_str)

if __name__ == '__main__':
    unittest.main() 


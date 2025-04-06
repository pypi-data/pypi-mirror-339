import os
import sys
import unittest
import json

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from src.pyenvelop.core import Envelop, EnvelopHead, EnvelopBody, Data, DataSet, Entity

class TestEnvelopHead(unittest.TestCase):
    """测试信封头部类"""

    def setUp(self):
        """初始化测试环境"""
        self.header = EnvelopHead()

    def test_init_default_values(self):
        """测试默认值初始化"""
        self.assertEqual(self.header.get_node_item("success"), "true")
        self.assertEqual(self.header.get_node_item("message"), "执行成功")

    def test_to_json(self):
        """测试转换为JSON"""
        json_str = self.header.to_json()
        self.assertIn('"success":"true"', json_str)
        self.assertIn('"message":"执行成功"', json_str)

    def test_to_xml(self):
        """测试转换为XML"""
        xml_str = self.header.to_xml()
        self.assertIn("<success>true</success>", xml_str)
        self.assertIn("<message>执行成功</message>", xml_str)

class TestEnvelopBody(unittest.TestCase):
    def setUp(self):
        self.body = EnvelopBody()
        self.test_data = Data({"id": "1", "name": "test"})
        self.test_dataset = DataSet([{"id": "1", "name": "test1"}])

    def test_init(self):
        """测试初始化"""
        self.assertEqual(len(self.body), 0)

    def test_set_get_node(self):
        """测试节点的设置和获取"""
        self.body.set_node(self.test_data, node="test")
        node = self.body.get_node("test")
        self.assertEqual(node["id"], "1")
        self.assertEqual(node["name"], "test")

    def test_set_get_dataset(self):
        """测试数据集的设置和获取"""
        self.body.set_node_dataset("test", self.test_dataset)
        dataset = self.body.get_node_dataset("test")
        self.assertEqual(len(dataset), 1)
        self.assertEqual(dataset[0]["id"], "1")

    def test_to_json(self):
        """测试JSON转换"""
        self.body.set_node(self.test_data, node="test")
        json_str = self.body.to_json()
        self.assertIn('"test"', json_str)
        self.assertIn('"id":"1"', json_str)

    def test_to_xml(self):
        """测试XML转换"""
        self.body.set_node(self.test_data, node="test")
        xml_str = self.body.to_xml()
        self.assertIn('<test>', xml_str)
        self.assertIn('<id>1</id>', xml_str)

    def test_clone(self):
        """测试主体克隆"""
        # 设置数据
        self.body.set_node(self.test_data, node="test")
        self.body.set_node_dataset("dataset", self.test_dataset)
        
        # 克隆主体
        cloned_body = self.body.clone()
        
        # 验证克隆结果
        self.assertEqual(cloned_body.get_node("test")["id"], "1")
        self.assertEqual(len(cloned_body.get_node_dataset("dataset")), 1)
        
        # 验证修改克隆不影响原对象
        cloned_body.set_node_item("new", "value", node="test")
        self.assertIsNone(self.body.get_node_item("new", node="test"))

class TestEnvelop(unittest.TestCase):
    """测试信封类"""

    def setUp(self):
        """初始化测试环境"""
        self.envelop = Envelop()

    def test_init_default(self):
        """测试默认初始化"""
        self.assertIsInstance(self.envelop.header, EnvelopHead)
        self.assertIsInstance(self.envelop.body, EnvelopBody)
        self.assertEqual(self.envelop.header.get_node_item("success"), "true")
        self.assertEqual(self.envelop.header.get_node_item("message"), "执行成功")

    def test_init_with_values(self):
        """测试带值初始化"""
        header_dict = {
            "success": "true",
            "message": "测试消息"
        }
        body_dict = {}
        envelop = Envelop(header=header_dict, body=body_dict)
        self.assertEqual(envelop.header.get_node_item("success"), "true")
        self.assertEqual(envelop.header.get_node_item("message"), "测试消息")

    def test_header_property(self):
        """测试header属性"""
        header = EnvelopHead()
        header.set_node_item("message", "测试消息")
        self.envelop.header = header
        self.assertEqual(self.envelop.header.get_node_item("message"), "测试消息")
        with self.assertRaises(TypeError):
            self.envelop.header = "invalid"

    def test_header_methods(self):
        """测试header的get/set方法"""
        header = EnvelopHead()
        header.set_node_item("message", "测试消息")
        self.envelop.set_header(header)
        self.assertEqual(self.envelop.get_header().get_node_item("message"), "测试消息")
        with self.assertRaises(TypeError):
            self.envelop.set_header("invalid")

    def test_body_property(self):
        """测试body属性"""
        body = EnvelopBody()
        data = Data({"value": "test"})
        body.set_node(data, node="test")
        self.envelop.body = body
        self.assertEqual(self.envelop.body.get_node("test").get_string("value"), "test")
        with self.assertRaises(TypeError):
            self.envelop.body = "invalid"

    def test_body_methods(self):
        """测试body的get/set方法"""
        body = EnvelopBody()
        data = Data({"value": "test"})
        body.set_node(data, node="test")
        self.envelop.set_body(body)
        self.assertEqual(self.envelop.get_body().get_node("test").get_string("value"), "test")
        with self.assertRaises(TypeError):
            self.envelop.set_body("invalid")

    def test_to_json(self):
        """测试转换为JSON"""
        # 设置头部
        self.envelop.header.set_node_item("success", "true")
        self.envelop.header.set_node_item("message", "测试成功")
        
        # 设置主体
        data = Data({"value": "test"})
        self.envelop.body.set_node(data, node="test")
        
        json_str = self.envelop.to_json()
        self.assertIn('"success":"true"', json_str)
        self.assertIn('"message":"测试成功"', json_str)
        self.assertIn('"test":', json_str)
        self.assertIn('"value":"test"', json_str)

    def test_to_xml(self):
        """测试转换为XML"""
        # 设置头部
        self.envelop.header.set_node_item("success", "true")
        self.envelop.header.set_node_item("message", "测试成功")
        
        # 设置主体
        data = Data({"value": "test"})
        self.envelop.body.set_node(data, node="test")
        
        xml_str = self.envelop.to_xml()
        self.assertIn("<success>true</success>", xml_str)
        self.assertIn("<message>测试成功</message>", xml_str)
        self.assertIn("<test>", xml_str)
        self.assertIn("<value>test</value>", xml_str)

    def test_str_representation(self):
        """测试字符串表示"""
        # 设置头部
        self.envelop.header.set_node_item("success", "true")
        self.envelop.header.set_node_item("message", "测试成功")
        
        # 设置主体
        data = Data({"value": "test"})
        self.envelop.body.set_node(data, node="test")
        
        str_repr = str(self.envelop)
        self.assertIn('<success>true</success>', str_repr)
        self.assertIn('<message>测试成功</message>', str_repr)
        self.assertIn('<test>', str_repr)
        self.assertIn('<value>test</value>', str_repr)
        self.assertIn('</test>', str_repr)
        
    def test_validate(self):
        """测试信封验证"""
        self.assertTrue(self.envelop.validate())
        
    def test_validate_with_rules(self):
        """测试带规则的信封验证"""
        # 设置头部
        self.envelop.header.set_node_item("success", "true")
        self.envelop.header.set_node_item("message", "测试成功")
        
        # 定义验证规则
        rules = {
            "header": {
                "success": lambda x: x == "true",
                "message": lambda x: x == "测试成功"
            }
        }
        
        # 验证成功的情况
        self.assertTrue(self.envelop.validate(rules))
        
        # 验证失败的情况
        self.envelop.header.set_node_item("success", "false")
        self.assertFalse(self.envelop.validate(rules))
        
    def test_dataset_serialization(self):
        """测试数据集的序列化和反序列化一致性"""
        # 创建测试数据
        dataset = DataSet([
            {"id": "1", "name": "test1"},
            {"id": "2", "name": "test2"}
        ])
        
        # 设置到信封中
        self.envelop.body.set_node_dataset("dataset", dataset=dataset, node="users")
        
        # 序列化为JSON
        json_str = self.envelop.to_json()
        
        # 从JSON创建新的信封
        new_envelop = Envelop()
        data = json.loads(json_str)
        users_data = data["body"]["users"]["dataset"]
        new_envelop.body.set_node_dataset("dataset", dataset=DataSet(users_data), node="users")
        
        # 验证数据一致性
        self.assertEqual(
            self.envelop.body.get_node_dataset("dataset", node="users").to_dict(),
            new_envelop.body.get_node_dataset("dataset", node="users").to_dict()
        )

if __name__ == '__main__':
    unittest.main() 
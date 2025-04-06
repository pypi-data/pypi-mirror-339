import os
import sys
import unittest

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

# 导入所有测试类
from test_data import TestData
from test_dataset import TestDataSet
from test_entity import TestEntity
from test_envelop import TestEnvelopHead, TestEnvelopBody, TestEnvelop
from test_exceptions import TestCheckedException, TestUnCheckedException
from test_demo import TestEnvelopDemo

def run_all_tests():
    # 创建测试套件
    test_suite = unittest.TestSuite()
    
    # 添加所有测试类
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestData))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestDataSet))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestEntity))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestEnvelopHead))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestEnvelopBody))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestEnvelop))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCheckedException))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestUnCheckedException))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestEnvelopDemo))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(test_suite)

if __name__ == '__main__':
    run_all_tests() 
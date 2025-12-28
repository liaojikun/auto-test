import pytest
import importlib
import os
import sys

# 用于存放当前测试用例获取到的数据字典
_CURRENT_TEST_DATA = {}

def find_tdata(key):
    """全局查找函数：根据传入的字符串键，从当前用例的数据块中获取参数"""
    return _CURRENT_TEST_DATA.get(key, {})

class BaseRunner:
    @pytest.fixture(autouse=True)
    def _auto_load_tdata(self, request):
        """
        自动化数据加载钩子：
        1. 获取当前测试文件名 (如 test_login.py) -> 转换成 tdata_login.py
        2. 获取当前测试函数名 (如 test_login_fail_0001) -> 对应变量 tdata_login_fail_0001
        """
        global _CURRENT_TEST_DATA
        
        # 获取测试函数所在的模块路径和函数名
        test_module_path = request.fspath.strpath
        test_func_name = request.node.name
        
        # 1. 计算 tdata 模块名
        # 例如: /path/test_login.py -> tdata_login
        dir_path = os.path.dirname(test_module_path)
        base_name = os.path.basename(test_module_path)
        tdata_module_name = base_name.replace("test_", "tdata_").replace(".py", "")
        
        # 2. 动态加载 tdata 模块
        try:
            # 确保当前目录在 sys.path 中以便导入
            if dir_path not in sys.path:
                sys.path.insert(0, dir_path)
            
            tdata_module = importlib.import_module(tdata_module_name)
            # 重新加载模块，防止在单次进程中多次运行数据不刷新
            importlib.reload(tdata_module)
            
            # 3. 根据函数名映射数据变量
            # test_login_fail_0001 -> tdata_login_fail_0001
            data_var_name = test_func_name.replace("test_", "tdata_")
            _CURRENT_TEST_DATA = getattr(tdata_module, data_var_name, {})
            
        except ImportError:
            _CURRENT_TEST_DATA = {}
            print(f"\n[Warning] 未找到数据文件: {tdata_module_name}.py")
        except Exception as e:
            _CURRENT_TEST_DATA = {}
            print(f"\n[Error] 加载数据出错: {e}")

    @classmethod
    def run(cls):
        """主运行入口"""
        # 获取子类所在的文件路径
        caller_file = sys.modules[cls.__module__].__file__
        pytest.main(["-s", "-v", caller_file])
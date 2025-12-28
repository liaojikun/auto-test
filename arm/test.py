import pytest
import importlib
import os
import sys

# ==========================================
# 全局上下文管理
# ==========================================

# 用于存放当前测试用例获取到的数据字典
_CURRENT_TEST_DATA = {}
# 用于存放 teardown 函数的任务队列 (堆栈)
_TEARDOWN_STACK = []

def find_tdata(key):
    """
    全局查找函数：根据传入的字符串键（如 "step.account.login"），
    从当前用例的数据块中获取对应的参数字典。
    """
    return _CURRENT_TEST_DATA.get(key, {})

# ==========================================
# 主运行基类
# ==========================================

class BaseRunner:
    
    @classmethod
    def add_teardown(cls, func):
        """
        向堆栈中添加清理任务。
        通常由 BaseStep 或其子类调用。
        """
        if callable(func):
            _TEARDOWN_STACK.append(func)
            # 获取函数名用于日志打印
            func_name = func.__name__ if hasattr(func, '__name__') else "lambda"
            print(f"[Engine] 已注册清理任务: {func_name}")

    @pytest.fixture(autouse=True)
    def _lifecycle_management(self, request):
        """
        生命周期管理钩子 (核心引擎):
        1. 自动化加载同级同名的 tdata 数据
        2. 初始化并排空 Teardown 堆栈
        3. 用例执行完成后顺序执行清理任务
        """
        global _CURRENT_TEST_DATA
        
        # --- [Setup 阶段] ---
        # 1. 初始化清理堆栈
        _TEARDOWN_STACK.clear()
        
        # 2. 解析路径并加载数据文件
        test_module_path = request.fspath.strpath
        test_func_name = request.node.name
        
        dir_path = os.path.dirname(test_module_path)
        base_name = os.path.basename(test_module_path)
        # 转换: test_login.py -> tdata_login
        tdata_module_name = base_name.replace("test_", "tdata_").replace(".py", "")
        
        try:
            if dir_path not in sys.path:
                sys.path.insert(0, dir_path)
            
            # 动态导入数据模块并刷新
            tdata_module = importlib.import_module(tdata_module_name)
            importlib.reload(tdata_module)
            
            # 获取对应函数的数据变量: test_login_fail_0001 -> tdata_login_fail_0001
            data_var_name = test_func_name.replace("test_", "tdata_")
            _CURRENT_TEST_DATA = getattr(tdata_module, data_var_name, {})
            
        except ImportError:
            _CURRENT_TEST_DATA = {}
            # print(f"[Warning] 未找到匹配的数据文件: {tdata_module_name}.py")
        except Exception as e:
            _CURRENT_TEST_DATA = {}
            print(f"[Error] 加载数据失败: {e}")

        # --- [执行测试用例] ---
        yield

        # --- [Teardown 阶段] ---
        if _TEARDOWN_STACK:
            print(f"\n[Engine] 用例执行完毕，开始顺序执行 Teardown 任务 (共 {len(_TEARDOWN_STACK)} 个)...")
            
            # 按照 FIFO (先进先出) 顺序执行: 1.login_data -> 2.expect_data
            while _TEARDOWN_STACK:
                task = _TEARDOWN_STACK.pop(0) # 弹出最早加入的函数
                try:
                    task()
                except Exception as e:
                    print(f"[Error] 执行清理任务失败: {e}")

    @classmethod
    def run(cls):
        """
        启动入口：在子类中使用 if __name__ == "__main__": cls.run() 调用
        """
        # 自动定位调用该方法的模块文件
        caller_module = sys.modules[cls.__module__]
        caller_file = caller_module.__file__
        
        print(f"\n{'='*20} 测试开始: {os.path.basename(caller_file)} {'='*20}")
        
        # 默认配置: -s (输出打印), -v (详细模式)
        pytest.main(["-s", "-v", caller_file])
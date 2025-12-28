from arm.test import BaseRunner

class BaseStep:
    def teardown(self, func):
        # 调用 BaseRunner 的类方法来注册任务
        BaseRunner.add_teardown(func)
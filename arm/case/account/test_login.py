from arm.test import BaseRunner
from arm.step.apply import Apply

class TestLogin(BaseRunner):
    apply_step = Apply()
    
    def test_login_fail_0001(self):
        # 1. 登录失败测试
        self.apply_step.account.user.step_login("step.account.login")
        # step.common.expect("step.common.expect")

    def test_login_fail_0002(self):
        # 2. 账号冻结测试
        self.apply_step.account.user.step_login("step.account.login")
        # step.common.expect("step.common.expect")

if __name__ == "__main__":
    TestLogin.run()
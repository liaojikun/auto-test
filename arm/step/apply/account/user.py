from arm.test import find_tdata
from arm.step.base_step import BaseStep

class User(BaseStep):
    def step_login(self, tdata_key):
        # 核心：通过 key 获取自己的参数
        data = find_tdata(tdata_key)
        username = data.get("username")
        password = data.get("password")
        print(f"\n[Step] step_login: 正在登录: 用户名={username}, 密码={password}")
        # 这里写实际请求逻辑...
        self.teardown(
            lambda: self.clear_login_data()
        )
    
    def clear_login_data(self):
        print("\n[Step] clear_login_data: 清理登录数据...")
        # 这里写实际清理逻辑...

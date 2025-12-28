from arm.test import find_tdata

class User:
    def step_login(self, tdata_key):
        # 核心：通过 key 获取自己的参数
        data = find_tdata(tdata_key)
        username = data.get("username")
        password = data.get("password")
        print(f"\n[Step] 正在登录: 用户名={username}, 密码={password}")
        # 这里写实际请求逻辑...
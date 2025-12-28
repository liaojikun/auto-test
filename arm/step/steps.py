from arm.test import find_tdata

class Account:
    def login(self, tdata_key):
        # 核心：通过 key 获取自己的参数
        data = find_tdata(tdata_key)
        username = data.get("username")
        password = data.get("password")
        print(f"\n[Step] 正在登录: 用户名={username}, 密码={password}")
        # 这里写实际请求逻辑...

class Common:
    def expect(self, tdata_key):
        data = find_tdata(tdata_key)
        status = data.get("status_code")
        msg = data.get("message")
        print(f"[Step] 验证预期: 状态码={status}, 消息={msg}")
        assert status == 401
        # 这里写断言逻辑...

# 为了方便 test 调用，实例化它们
class Steps:
    account = Account()
    common = Common()

step = Steps()
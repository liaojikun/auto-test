"""
1、希望主类里面实现一个功能，test用例通过同级同名的tdata文件，来获取自己的参数。具体描述如下：
例如test_login.py里有一条用例：
def test_login_fail_0001():
    # 登录失败
    step.account.login("step.account.login")
    step.common.expect("step.common.expect")

def test_login_fail_0002():
    pass
def test_login_fail_0003():
    pass
    

2、同级目录下有一个 tdata_login.py，里面放着test_login.py所需要的参数，
内容例如：
tdata_login_fail_0001 = {
    "step.account.login": {
        "username": "wrong_user",
        "password": "wrong_pass",
    }
    "step.common.expect": {
        "status_code": 401,
        "message": "用户名或密码错误"
    }
tdata_login_fail_0002 = {}
tdata_login_fail_0003 = {}
实现说明，tdata_login_fail_0001，对应test_login.py里的test_login_fail_0001函数，所需要的参数test_login_fail_0001使用到的function（通过find_tdata拿到对应自己的参数）如果需要传参数，就给个step开头的字符串，会到tdata_login_fail_0001里去找对应的参数进行传递。


3、step.account.login函数的内容:
def login(tdata=None):
    data = find_tdata(tdata)
    # 执行登录逻辑 ....



project/
├── base_runner.py
├── steps.py
└── case/
    └── account/
        ├── test_login.py
        └── tdata_login.py

我的目录结构如下：       
│  .gitignore
│  config
│
├─.vscode
│      settings.json
│
├─apply
└─arm
    │  test.py
    │  __init__.py
    │
    ├─case
    │  │  __init__.py
    │  │
    │  ├─account
    │  │  │  tdata_login.py
    │  │  │  test_login.py
    │  └─ └─ __init__.py
    │
    ├─step
    │  │  steps.py
    │  │  __init__.py
    │  │
    │  ├─apply
    │  │  │  __init__.py
    │  │  │
    │  │  ├─account
    │  │  │      user.py
    │  │  │      __init__.py
    │  │  │
    │  │  └─order
    └─ └─__pycache__

    
user.py里的内容如下：
from arm.test import find_tdata
class User:
    def login(self, tdata_key):
        # 核心：通过 key 获取自己的参数
        data = find_tdata(tdata_key)
        username = data.get("username")
        password = data.get("password")
        print(f"\n[Step] 正在登录: 用户名={username}, 密码={password}")
        # 这里写实际请求逻辑...

test_login.py里的内容如下：期望通过self.apply_step.account.user.step_login()这样的方式调用
class TestLogin(BaseRunner):
    apply_step = Apply()
    
    def test_login_fail_0001(self):
        # 1. 登录失败测试
        self.apply_step.account.user.step_login("step.account.login")
        # step.common.expect("step.common.expect")
如果想要实现这一的效果，init.py里需要怎么做

=========================================
test_login.py
from arm.test import BaseRunner
from arm.step.apply import Apply

class TestLogin(BaseRunner):
    apply_step = Apply()
    
    def test_login_fail_0001(self):
        # 1. 登录失败测试
        self.apply_step.account.user.step_login("step.account.login")
        self.apply_step.common.assertion.expect("step.common.expect")

user.py
class Assertion:
    def expect(self, tdata_key):
        data = find_tdata(tdata_key)
        status = data.get("status_code")
        msg = data.get("message")
        print(f"[Step] 验证预期: 状态码={status}, 消息={msg}")
        assert status == 401
        # 这里写断言逻辑...

        self.teardown(
            lambda: self.clear_expect_data()
        )
    
    def clear_expect_data(self):
        print("\n[Step] 清理预期数据...")
        # 这里写实际清理逻辑...

assertion.py
class User:
    def step_login(self, tdata_key):
        # 核心：通过 key 获取自己的参数
        data = find_tdata(tdata_key)
        username = data.get("username")
        password = data.get("password")
        print(f"\n[Step] 正在登录: 用户名={username}, 密码={password}")
        # 这里写实际请求逻辑...
        self.teardown(
            lambda: self.clear_login_data()
        )
    
    def clear_login_data(self):
        print("\n[Step] 清理登录数据...")
        # 这里写实际清理逻辑...

期望test.py里实现一个teardown功能，已堆栈的方式加入所需要的执行函数。等待本条用例执行完后根据堆栈顺序执行teardown里的函数
例如test_login_fail_0001执行顺序：
1.step_login
2.expect
3.clear_login_data
4.clear_expect_data

"""


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
    
"""


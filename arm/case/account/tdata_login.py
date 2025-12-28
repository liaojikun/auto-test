tdata_login_fail_0001 = {
    "step.account.user.step_login": {
        "username": "wrong_user",
        "password": "wrong_pass",
    },
    "step.common.assertion.expect": {
        "!result": "{step.account.user.step_login result}",
        "status_code": 401,
        "message": "用户名或密码错误"
    }
}

tdata_login_fail_0002 = {
    "step.account.login": {
        "username": "blocked_user",
        "password": "any_password",
    },
    "step.common.expect": {
        "result": "模拟登录结果数据",
        "status_code": 403,
        "message": "账号已冻结"
    }
}
from .user import User

class Account:
    def __init__(self):
        # 实例化 user 模块
        self.user = User()
        # 如果以后有其他 user 相关的类，也可以在这里实例化
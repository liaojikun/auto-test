from .account import Account
# from .order import Order  # 假设你以后会有 order 模块

class Apply:
    def __init__(self):
        self.account = Account()
        # self.order = Order() # 同样的逻辑
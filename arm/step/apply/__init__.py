from .account import Account
from .common import Common
# from .order import Order  # 假设你以后会有 order 模块

class Apply:
    def __init__(self):
        self.account = Account()
        self.common = Common()
        # self.order = Order() # 同样的逻辑
from arm.test import find_tdata
from arm.step.base_step import BaseStep

class Assertion(BaseStep):
    def expect(self, tdata_key):
        self.teardown(
            lambda: self.clear_expect_data()
        )
        data = find_tdata(tdata_key)
        status = data.get("status_code")
        msg = data.get("message")
        print(f"[Step] expect: 验证预期: 状态码={status}, 消息={msg}")
        assert "模拟登录结果数据" == data["result"]
        assert status == 401
        # 这里写断言逻辑...
    
    def clear_expect_data(self):
        print("\n[clear] clear_expect_data: 清理预期数据...")
        # 这里写实际清理逻辑...
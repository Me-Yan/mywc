from user import User


class ExecuteCode:

    @staticmethod
    def execute_code(base_data, phone, password, action, count, min_price, max_price, delay_seconds, again=False):
        """执行程序"""

        user = User(phone=phone, password=password, base_data=base_data)
        user.login().buy_goods(action=action, count=count, min_price=min_price, max_price=max_price,
                               delay_seconds=delay_seconds, again=again)
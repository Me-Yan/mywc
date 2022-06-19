
"""
--------Amos
"""
import threading
from util import Util
from execute_code import ExecuteCode


if __name__ == "__main__":
    """
    上午场时间、下午场时间、参考时间
    入场
    查询、参与、抢购
    抢几幅、价格区间、延迟时间(秒)
    """

    base_data = Util.build_base_data()

    threading.Thread(target=ExecuteCode.execute_code, name="Amos",
                     args=(base_data, "xxxxx", "xxxxx", "抢购", 1, 0, 50000, 0)).start()  # Amos

    # threading.Thread(target=ExecuteCode.execute_code, name="双林",
    #                  args=(base_data, "xxxxx", "xxxxx", "抢购", 1, 0, 50000, 0)).start()  # 双林
    #
    # threading.Thread(target=ExecuteCode.execute_code, name="帅娃",
    #                  args=(base_data, "xxxxx", "xxxxx", "抢购", 1, 0, 50000, 0)).start() # 帅娃
    #
    # threading.Thread(target=ExecuteCode.execute_code, name="老郑",
    #                  args=(base_data, "xxxxx", "xxxxx", "抢购", 1, 0, 50000, 0)).start()   # 老郑

    # threading.Thread(target=ExecuteCode.execute_code, name="包子",
    #                  args=(base_data, "xxxxx", "xxxxx", "抢购", 1, 0, 50000, 0)).start()  # 包子
    #
    # threading.Thread(target=ExecuteCode.execute_code, name="贾哥",
    #                  args=(base_data, "xxxxx", "xxxxx", "抢购", 1, 0, 50000, 0)).start()    # 贾哥
    #
    # threading.Thread(target=ExecuteCode.execute_code, name="粉红",
    #                  args=(base_data, "xxxxx", "xxxxx", "抢购", 1, 0, 50000, 0)).start()    # 粉红
    #
    # threading.Thread(target=ExecuteCode.execute_code, name="桂林",
    #                  args=(base_data, "xxxxx", "xxxxx", "抢购", 1, 0, 50000, 0)).start() # 桂林
    #
    # threading.Thread(target=ExecuteCode.execute_code, name="曲",
    #                  args=(base_data, "xxxxx", "xxxxx", "抢购", 1, 0, 50000, 0)).start()  # 曲
















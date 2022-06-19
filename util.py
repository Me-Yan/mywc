import json
import time
from datetime import datetime

class Util:

    YYYY_MM_DD_HH_MM_SS_FF = "%Y-%m-%d %H:%M:%S.%f"

    YYYY_MM_DD = "%Y-%m-%d"


    @staticmethod
    def get_millisecond(datetime_str, pattern="%Y-%m-%d %H:%M:%S.%f"):
        """将日期时间字符串格式转换为毫秒数"""

        millisecond = 0

        if datetime_str:
            temp_datetime = time.strptime(datetime_str, pattern)
            millisecond = int(time.mktime(temp_datetime)) * 1000

        return millisecond

    @staticmethod
    def get_sid(flag_time):
        """获取当前时间的sid"""

        now = datetime.now()
        now_str = now.strftime(Util.YYYY_MM_DD_HH_MM_SS_FF)
        now_date_str = now.strftime(Util.YYYY_MM_DD)

        flag_datetime_str = "%s %s" % (now_date_str, flag_time)
        flag_datetime = time.strptime(flag_datetime_str, Util.YYYY_MM_DD_HH_MM_SS_FF)
        now_datetime = time.strptime(now_str, Util.YYYY_MM_DD_HH_MM_SS_FF)

        now_micro = int(time.mktime(now_datetime))
        flag_micro = int(time.mktime(flag_datetime))

        if now_micro <= flag_micro:
            sid = 1
        else:
            sid = 9

        return sid

    @staticmethod
    def get_start_datetime_str(flag_time, morning_time_str, afternoon_time_str):
        """获取接下来要开始的场次"""

        now = datetime.now()
        now_str = now.strftime(Util.YYYY_MM_DD_HH_MM_SS_FF)
        now_date_str = now.strftime(Util.YYYY_MM_DD)

        flag_datetime_str = "%s %s" % (now_date_str, flag_time)
        flag_datetime = time.strptime(flag_datetime_str, Util.YYYY_MM_DD_HH_MM_SS_FF)
        now_datetime = time.strptime(now_str, Util.YYYY_MM_DD_HH_MM_SS_FF)

        now_micro = int(time.mktime(now_datetime))
        flag_micro = int(time.mktime(flag_datetime))

        if now_micro <= flag_micro:
            begin_datetime_str = "%s %s" % (now_date_str, morning_time_str)
        else:
            begin_datetime_str = "%s %s" % (now_date_str, afternoon_time_str)

        return begin_datetime_str

    @staticmethod
    def build_base_data():
        """构建基本需要的数据"""

        base_data = {}

        with open("data.json", "r", encoding="utf-8") as data_file:
            base_data = json.load(data_file)

        sid = Util.get_sid(base_data["time_data"]["flag_time"])

        base_data["activity_data"]["current_sid"] = sid

        return base_data


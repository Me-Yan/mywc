import time
from datetime import datetime

class Util:

    @staticmethod
    def get_millisecond(datetime_str, pattern):
        """
        将日期时间字符串格式转换为毫秒数
        :param pattern:
        :param datetime_str:
        :return:
        """

        millisecond = 0

        if datetime_str:
            temp_datetime = time.strptime(datetime_str, pattern)
            millisecond = int(time.mktime(temp_datetime)) * 1000

        return millisecond

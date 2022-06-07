import json
import time
from datetime import datetime
import requests
from util import Util as util


class GetData:

    datetime_pattern = "%Y-%m-%d %H:%M:%S.%f"

    def __init__(self):
        with open("data.json", "r", encoding="utf-8") as data_file:
            self.basic_json = json.load(data_file)

        with open("user.json", "r", encoding="utf-8") as user_file:
            self.login_data = json.load(user_file)

        self.token = None
        self.session = None
        self.address_info = None

    def login(self):
        """
        用户登录
        :return:
        @toekn 用户登录后的token
        @ss 用户访问的会话
        """

        login_url = "%s%s" % (self.basic_json["basic_path"], self.basic_json["urls"]["login_url"])

        user_data = self.login_data

        ss = requests.session()
        res = ss.post(url=login_url, json=user_data, headers=self.basic_json["basic_header"])

        res_json = res.json()

        print(res_json)

        self.address_info = res_json["data"]["address_list"][0]

        self.token = res_json['data']['token']
        self.session = ss

        print(self.token)

    def get_goods_data(self, sid, index):
        """
        用户根据场次sid、页码index获取单页数据
        :param token: 登录令牌
        :param session: 会话
        :param sid: 场次
        :param index: 页码
        :return:
        """

        req_data = {
            "page_index": index,
            "page_size": 10,
            "sid": sid,
            "token": self.token
        }

        req_url = "%s%s" % (self.basic_json["basic_path"], self.basic_json["urls"]["goods_url"])

        res = self.session.post(url=req_url, json=req_data, headers=self.basic_json["basic_header"])

        res_json = res.json()

        list = res_json['data']['list']

        print(list)

        return list

    def get_all_data(self, period_list, index_list):
        """
        组装所有场次的商品
        :param token:
        :param session:
        :param period_list:
        :param index_list:
        :return:
        """

        all_list = []

        if period_list and index_list:
            for sid in period_list:
                for index in index_list:
                    temp_list = self.get_goods_data(sid, index)
                    if temp_list:
                        all_list.extend(temp_list)
        if self.session:
            self.session.close()

        return all_list

    def process_data(self, goods_Data):
        """
        根据商品数据组装sql
        :param goods_Data:
        :return:
        """

        if goods_Data:
            sql = "INSERT INTO goods (gid, cid, sid, mode, period, name, price, belong, nickname, update_time) VALUES"

            for item in goods_Data:
                gid = item['gid']
                cid = item['cid']
                sid = item['sid']
                mode = int(item['state'])
                period = "上午"
                if sid == 9:
                    period = "下午"
                name = item['name']
                price = item['price']
                price = round(float(price) / 100, 2)
                belong = item['belong']
                nickname = item['belong_nickname'] if "belong_nickname" in item else ""
                update_time = item['update_time']

                item_sql = "(%d, %d, %d, %d, '%s', '%s', %.2f, %d, '%s', '%s')," % (gid, cid, sid, mode, period, name, price, belong, nickname, update_time)
                sql = "%s%s" % (sql, item_sql)

            sql = "%s;" % sql.rstrip(',')

            return sql

        return None

    def submit_order(self, gid, cid, sid, mode):
        """
        提交订单
        :param gid:
        :param cid:
        :param mode:
        :return:
        """
        req_url = "%s%s" % (self.basic_json["basic_path"], self.basic_json["urls"]["submit_url"])

        req_data = {
            "gid": gid,
            "cid": cid,
            "sid": sid,
            "mode": "%d" % mode,
            "token": "%s" % self.token,
            "address_info": "%s" % self.address_info
        }

        res = self.session.post(url=req_url, json=req_data, headers=self.basic_json["basic_header"])

        res_json = res.json()

        return res_json

    def get_user_gtime(self):
        """
        查看用户访问的时间
        :return:
        """
        req_url = "%s%s" % (self.basic_json["basic_path"], self.basic_json["urls"]["time_url"])

        sid, index_list, begin_datetime = GetData.common_util()

        req_data = {
            "sid": sid,
            "token": "%s" % self.token
        }

        res = self.session.post(url=req_url, json=req_data, headers=self.basic_json["basic_header"])
        print(res.json())

    def visit_all_goods(self, count, price_period, delay_seconds):
        """
        轮询所有商品
        :return:
        """

        sid, index_list, begin_datetime = GetData.common_util()

        period_list = [sid]

        print("begin_datetime=%s, sid=%d" %(begin_datetime, sid))

        goods_list = self.get_all_data(period_list, index_list)
        goods_list = sorted(goods_list, key=lambda x:int(x['price']), reverse=True)

        visit_count = 0
        success_count = 0
        if goods_list:
            while True:
                print("---------request_time:%s" % datetime.now().strftime(GetData.datetime_pattern))

                cur_milli = int(round(time.time() * 1000))
                begin_milli = int(util.get_millisecond(begin_datetime, GetData.datetime_pattern)) + int(1000 * delay_seconds)

                if cur_milli >= begin_milli:
                    print(goods_list)
                    for item in goods_list:
                        gid = item['gid']
                        cid = item['cid']
                        temp_sid = item['sid']
                        mode = int(item['state'])
                        price = round(float(item["price"]) / 100, 2)

                        if price>=price_period[0] and price<=price_period[1]:
                            request_time = datetime.now().strftime(GetData.datetime_pattern)

                            res_data = self.submit_order(gid=gid, cid=cid, sid=temp_sid, mode=mode)

                            response_time = datetime.now().strftime(GetData.datetime_pattern)

                            if res_data["res_code"] == 1 or res_data["msg"] == "抢购成功，请尽快支付!":
                                success_count += 1

                            visit_count += 1

                            print("visit_count=%d, ,success_count=%d, ,%.2f, ,request_time=%s, ,response_time=%s, ,response=(%d, %s)"
                                  % (visit_count, success_count, price, request_time, response_time, res_data["res_code"], res_data["msg"]))

                        if success_count >= count:
                            break

                if success_count >= count:
                    break

    @staticmethod
    def common_util():
        now = datetime.now()
        now_str = now.strftime(GetData.datetime_pattern)
        now_date = now.strftime("%Y-%m-%d")

        flag_datetime_str = "%s 12:00:00.000000" % now_date
        flag_datetime = time.strptime(flag_datetime_str, GetData.datetime_pattern)
        now_datetime = time.strptime(now_str, GetData.datetime_pattern)

        now_micro = int(time.mktime(now_datetime))
        flag_micro = int(time.mktime(flag_datetime))

        if now_micro <= flag_micro:
            sid = 1
            index_list = list(range(0, 7))
            begin_datetime = "%s 10:30:00.000000" % now_date
        else:
            sid = 9
            index_list = list(range(0, 2))
            begin_datetime = "%s 12:00:00.000000" % now_date

        return sid, index_list, begin_datetime
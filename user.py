import threading

import requests
from goods_action import GoodsAction
from database import Database


class User:

    def __init__(self, phone, password, verify_code, base_data):
        self.phone = phone
        self.password = password
        self.verify_code = verify_code
        self.base_data = base_data
        self.system_data = base_data["system_data"]
        self.user_data = None

    def login(self):
        login_data = {
            "phone": "%s" % self.phone,
            "pwd": "%s" % self.password
        }
        if self.verify_code:
            login_data["sms_code"] = self.verify_code

        login_url = "%s%s" % (self.system_data["basic_path"], self.system_data["urls"]["login_url"])
        headers = self.system_data["basic_header"]

        session = requests.session()
        res = session.post(url=login_url, json=login_data, headers=headers)

        res_json = res.json()

        self.user_data = {
            "nickname": "%s" % res_json["data"]["nickname"],
            "token": "%s" % res_json["data"]['token'],
            "address": "%s" % res_json["data"]["address_list"][0],
            "session": session
        }

        self.base_data["user_data"] = self.user_data

        if res_json["res_code"] == 1 and res_json["msg"] == "登录成功":
            print("------%s......登录...成功-------" % threading.current_thread().getName())

        return self

    def buy_goods(self, action="抢购", count=1, min_price=0, max_price=50000, delay_seconds=0, again=False, stable_goods=None):
        """用户购买商品"""

        order_action = GoodsAction(base_data=self.base_data, action=action, count=count, min_price=min_price, max_price=max_price, delay_seconds=delay_seconds)

        if action == "查询":
            page_size = self.base_data["activity_data"]["page_size"]
            list_sid = self.base_data["activity_data"]["list_sid"]

            goods_list = order_action.list_all_goods(list_sid, page_size)
            if goods_list:
                sql = order_action.build_sql(goods_list, list_sid)

                database = Database()
                database.clear_goods("DELETE FROM goods")
                database.insert_goods_data(sql)
        elif action == "分析":
            page_size = self.base_data["activity_data"]["page_size"]

            list_store = self.base_data["activity_data"]["list_store"]

            for store in list_store:
                list_sid = store["list_sid"]
                mor_sid = list_sid[0]
                after_sid = list_sid[1]
                goods_list = order_action.list_all_goods(list_sid, page_size)
                if goods_list:
                    sql = order_action.build_sql(goods_list, list_sid)

                    database = Database()
                    database.clear_goods("DELETE FROM goods")
                    database.insert_goods_data(sql)

                    analysis_sql = order_action.analysis_data(store["store_name"], mor_sid, after_sid)
                    database = Database()
                    # database.delete_today_analysis()
                    database.analysis_data(analysis_sql)
        elif action == "入场":
            order_action.join_buy()
            order_action.get_user_gtime()
        elif action == "抢购":
            order_action.join_buy()
            order_action.get_user_gtime()
            order_action.loop_submit(again)
        elif action == "抢购指定":
            order_action.join_buy()
            order_action.get_user_gtime()

            if stable_goods is not None:
                gid = stable_goods["gid"]
                cid = stable_goods["cid"]
                sid = stable_goods["sid"]

                current_thread = threading.current_thread()
                thread_name = current_thread.getName()
                while True:
                    res_data = order_action.submit_order(gid, cid, sid)

                    if res_data["msg"] == "抢购成功，请尽快支付!" or res_data["res_code"] == 1:
                        print(
                            "\n------%s......%s.....恭喜抢购成功...,gid=%d,response=(%d, %s)"
                            % (thread_name, self.user_data["nickname"], gid, res_data["res_code"], res_data["msg"]))

                        break
                    else:
                        print(
                            "\n------%s......%s.....抢购失败...,gid=%d, ,response=(%d, %s)"
                            % (thread_name, self.user_data["nickname"], gid, res_data["res_code"], res_data["msg"]))



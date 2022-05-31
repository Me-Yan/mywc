import _thread
import json
import requests


class GetData:

    def __init__(self):
        with open("data.json", "r", encoding="utf-8") as data_file:
            self.basic_json = json.load(data_file)
        self.token = None
        self.session = None

    def login(self):
        """
        用户登录
        :return:
        @toekn 用户登录后的token
        @ss 用户访问的会话
        """

        login_url = "%s%s" % (self.basic_json["basic_path"], self.basic_json["urls"]["login_url"])

        user_data = self.basic_json["user"]

        ss = requests.session()
        res = ss.post(url=login_url, json=user_data, headers=self.basic_json["basic_header"])

        res_json = res.json()

        print(res_json)

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
            sql = "INSERT INTO goods (gid, cid, sid, mode, period, name, price, belong, nickname) VALUES"

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

                item_sql = "(%d, %d, %d, %d, '%s', '%s', %.2f, %d, '%s')," % (gid, cid, sid, mode, period, name, price, belong, nickname)
                sql = "%s%s" % (sql, item_sql)

            sql = "%s;" % sql.rstrip(',')

            return sql

        return None

    def get_user_gtime(self, sid):
        """
        查看用户访问的时间
        :return:
        """
        req_url = "%s%s" % (self.basic_json["basic_path"], self.basic_json["urls"]["time_url"])

        req_data = {
            "sid": sid,
            "token": "%s" % self.token
        }

        res = self.session.post(url=req_url, json=req_data, headers=self.basic_json["basic_header"])
        print(res.json())

    def submit_order(self, gid, cid, sid, mode):
        """
        提交订单
        :param gid:
        :param cid:
        :param sid:
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
            "address_info": {
                "id": 147,
                "uid": 198,
                "name": "Amos",
                "phone": "18380448173",
                "province": "四川省",
                "city": "成都市",
                "county": "双流区",
                "detail": "中和街道",
                "isdefault": 1,
                "create_time": "2022-05-26 01:52:25"
            }
        }

        # for index in range(0, 2):
        res = self.session.post(url=req_url, json=req_data, headers=self.basic_json["basic_header"])
        print(res.json())

    def visit_all_goods(self):

        goods_list = self.get_all_data([9], [0, 1])

        count = 0
        if goods_list:
            while True:
                print(goods_list)
                for item in goods_list:
                    gid = item['gid']
                    cid = item['cid']
                    sid = item['sid']
                    mode = int(item['state'])
                    self.submit_order(gid=gid, cid=cid, sid=sid, mode=mode)
                    count += 1
                    print(count)

    def create_thread(self, number):
        """
        创建线程执行任务
        :param number:
        :return:
        """
        goods_list = self.get_all_data([9], [0, 1])

        for item in range(0, number):
            _thread.start_new_thread(self.visit_all_goods, (goods_list,))


















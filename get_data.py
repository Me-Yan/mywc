import requests


class GetData:

    basic_headers = {
        "Connection": "keep-alive",
        "Host": "wx.muyuanfankj.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63060012)",
        "content-type": "application/json; charset=utf-8"
    }

    basic_path = "https://wx.muyuanfankj.cn"

    def login(self):

        login_url =  "%s/web/user/login" % GetData.basic_path

        user_data = {
            "phone": "18380448173",
            "pwd": "Mjustforyou9496"
        }

        ss = requests.session()
        res = ss.post(url=login_url, json=user_data, headers=GetData.basic_headers)

        res_json = res.json()

        print(res_json)

        token = res_json['data']['token']

        return token, ss

    def get_goods_data(self, token, session, sid, index):

        req_data = {
            "page_index": index,
            "page_size": 10,
            "sid": sid,
            "token": token
        }

        req_url = "%s/web/rush/getRushGoods" % GetData.basic_path

        res = session.post(url=req_url, json=req_data, headers=GetData.basic_headers)

        res_json = res.json()

        list = res_json['data']['list']

        print(list)

        return list

    def get_all_data(self, token, session, period_list, index_list):

        all_list = []

        if period_list and index_list:
            for sid in period_list:
                for index in index_list:
                    temp_list = self.get_goods_data(token, session, sid, index)
                    if temp_list:
                        all_list.extend(temp_list)
        if session:
            session.close()

        return all_list

    def process_data(self, goods_Data):

        if goods_Data:
            sql = "INSERT INTO goods (gid, cid, sid, period, name, price, belong, nickname) VALUES"

            for item in goods_Data:
                gid = item['gid']
                cid = item['cid']
                sid = item['sid']
                period = "上午"
                if sid == 9:
                    period = "下午"
                name = item['name']
                price = item['price']
                price = round(float(price) / 100, 2)
                belong = item['belong']
                nickname = item['belong_nickname']

                item_sql = "(%d, %d, %d, '%s', '%s', %.2f, %d, '%s')," % (gid, cid, sid, period, name, price, belong, nickname)
                sql = "%s%s" % (sql, item_sql)

            sql = "%s;" % sql.rstrip(',')

            return sql

        return None















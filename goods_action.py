import math
import threading
import time
from datetime import datetime
from util import Util

class GoodsAction:

    default_pattern = "%Y-%m-%d %H:%M:%S.%f"

    def __init__(self, base_data, action="抢购", count=1, min_price=0, max_price=50000, delay_seconds=0):
        self.action = action
        self.count = count
        self.min_price = min_price
        self.max_price = max_price
        self.delay_seconds = delay_seconds

        self.base_data = base_data

        self.user_data = base_data["user_data"]
        self.token = base_data["user_data"]["token"]
        self.address_info = base_data["user_data"]
        self.session = base_data["user_data"]["session"]

        self.activity_data = base_data["activity_data"]
        self.list_sid = base_data["activity_data"]["list_sid"]
        self.current_sid = base_data["activity_data"]["current_sid"]
        self.page_size = base_data["activity_data"]["page_size"]

        self.system_data = base_data["system_data"]
        self.basic_header = base_data["system_data"]["basic_header"]
        self.basic_path = base_data["system_data"]["basic_path"]
        self.urls = base_data["system_data"]["urls"]

        self.time_data = base_data["time_data"]
        self.flag_time = base_data["time_data"]["flag_time"]
        self.morning_time = base_data["time_data"]["morning_time"]
        self.afternoon_time = base_data["time_data"]["afternoon_time"]

    def get_per_goods(self, sid, index, page_size):
        """获取每页的数据"""

        goods_list = []

        req_url = "%s%s" % (self.basic_path, self.urls["goods_url"])

        req_data = {
            "page_index": index,
            "page_size": page_size,
            "sid": sid,
            "token": "%s" % self.token
        }

        res = self.session.post(url=req_url, json=req_data, headers=self.basic_header)

        res_json = res.json()

        if res_json["data"]["list"]:
            goods_list = res_json["data"]["list"]

        return goods_list

    def list_all_goods(self, list_sid, page_size):
        """获取该场活动的所有商品"""

        count = 0

        goods_list = []

        if list_sid:
            for sid in list_sid:
                total_page = self.get_total_page(sid)
                for index in range(0, total_page):
                    temp_list = self.get_per_goods(sid, index, page_size)
                    if temp_list:
                        goods_list.extend(temp_list)
                        count += 1

        if self.session:
            self.session.close()

        if goods_list:
            goods_list = sorted(goods_list, key=lambda x: int(x['price']), reverse=True)

        print(goods_list)

        if len(list_sid) == 1:
            print("------获取 %d 页数据，共 %d 个商品---------" % (count, len(goods_list)))
        else:
            print("------共 %d 个商品---------" % (len(goods_list)))

        return goods_list

    def build_sql(self, goods_list):
        """构建商品的sql"""

        if goods_list:
            sql = "INSERT INTO goods (gid, cid, sid, mode, period, name, price, belong, nickname, update_time) VALUES"

            for item in goods_list:
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

                item_sql = "(%d, %d, %d, %d, '%s', '%s', %.2f, %d, '%s', '%s')," % (
                gid, cid, sid, mode, period, name, price, belong, nickname, update_time)
                sql = "%s%s" % (sql, item_sql)

            sql = "%s;" % sql.rstrip(',')

            return sql

    def get_total_page(self, sid):
        """获取当前场次商品的总页数"""

        req_url = "%s%s" % (self.basic_path, self.urls["goods_url"])

        req_data = {
            "page_index": 0,
            "page_size": self.page_size,
            "sid": sid,
            "token": "%s" % self.token
        }

        res = self.session.post(url=req_url, json=req_data, headers=self.basic_header)

        res_json = res.json()

        if res_json["data"]["list"]:
            count = res_json["data"]["total_count"]

        total_page = math.ceil(count / self.page_size)

        return total_page

    def join_buy(self):
        """访问相应场次，会被记录"""

        req_url = "%s%s" % (self.basic_path, self.urls["join_url"])

        req_data = {
            "type": "进入场次",
            "sid": self.current_sid,
            "token": "%s" % self.token
        }

        res = self.session.post(url=req_url, json=req_data, headers=self.basic_header)
        res_json = res.json()

        current_thread = threading.current_thread()
        thread_name = current_thread.getName()

        if res_json["res_code"] == 1:
            print("------%s......进入场次..成功---" % thread_name)
        else:
            print("------%s......进入场次..失败失败失败---" % thread_name)

    def get_user_gtime(self):
        """获取用户访问的时间"""

        req_url = "%s%s" % (self.basic_path, self.urls["time_url"])

        req_data = {
            "sid": self.current_sid,
            "token": "%s" % self.token
        }

        res = self.session.post(url=req_url, json=req_data, headers=self.basic_header)

        res_json = res.json()

        if res_json["res_code"] == 1:
            print("------%s......触发时间判断..成功---" % threading.current_thread().getName())
        else:
            print("------%s......触发时间判断..成功---" % threading.current_thread().getName())

    def submit_order(self, gid, cid, sid, mode):
        """抢购商品"""

        req_url = "%s%s" % (self.basic_path, self.urls["submit_url"])

        req_data = {
            "gid": gid,
            "cid": cid,
            "sid": sid,
            "mode": "1",
            "token": "%s" % self.token,
            "address_info": "%s" % self.address_info
        }

        res = self.session.post(url=req_url, json=req_data, headers=self.basic_header)

        res_json = res.json()

        return res_json

    def loop_submit(self, again):
        """轮询抢购所有商品"""

        current_thread = threading.current_thread()
        thread_name = current_thread.getName()
        nickname = self.user_data["nickname"]

        begin_datetime_str = Util.get_start_datetime_str(self.flag_time, self.morning_time, self.afternoon_time)

        visit_count = 0
        success_count = 0
        circle_count = 0

        flag = False

        list_sid = [self.current_sid]

        goods_list = self.list_all_goods(list_sid, self.page_size)

        new_goods_list = []

        if goods_list:
            while True:

                new_goods_list = goods_list[:]

                if not flag:
                    print("------%s....%s..当前时间:%s" % (thread_name, nickname, datetime.now().strftime(GoodsAction.default_pattern)))

                    cur_milli = int(round(time.time() * 1000))
                    begin_milli = int(Util.get_millisecond(begin_datetime_str, Util.YYYY_MM_DD_HH_MM_SS_FF)) + int(1000 * self.delay_seconds)

                    if cur_milli >= begin_milli:
                        flag = True
                        print("------%s....%s..开始抢购了,请等待结果........" % (thread_name, nickname))

                if flag:
                    circle_count += 1
                    start_milli = int(round(time.time() * 1000))
                    print("------%s....%s..第%d回合--------------------" % (thread_name, nickname, circle_count))

                    # 如果能够获取到商品的状态，需要将这个商品list更换成切片的形式
                    for item in new_goods_list:
                        gid = item['gid']
                        cid = item['cid']
                        temp_sid = item['sid']
                        mode = int(item['state'])

                        # 1: 可抢 2：已被抢
                        if mode == 1 or again is True:
                            price = round(float(item["price"]) / 100, 2)

                            if self.min_price <= price <= self.max_price:

                                res_data = self.submit_order(gid=gid, cid=cid, sid=temp_sid, mode=mode)

                                visit_count += 1

                                if res_data["res_code"] == -1:
                                    if res_data["msg"] == "很遗憾,您没有抢到":
                                        if again is False:
                                            goods_list.remove(item)
                                    elif res_data["msg"] == "当日抢购数量已达上限!" or res_data["msg"] == "优先抢购数量已用完，请等待正式抢购!":
                                        pass
                                    elif res_data["msg"] == "当前时间抢购失败!" or res_data["msg"] == "商品抢购失败":
                                        pass
                                    else:
                                        print("------%s.......response=%s : %s" % (thread_name, res_data["res_code"], res_data["msg"]))
                                elif res_data["msg"] == "抢购成功，请尽快支付!" or res_data["res_code"] == 1:
                                    success_count += 1

                                    if success_count >= self.count:
                                        success_time = datetime.now().strftime(Util.YYYY_MM_DD_HH_MM_SS_FF)

                                        print("\n------%s......%s.....恭喜抢购成功...visit_count=%d, ,success_count=%d, ,gid=%d, ,price=%.2f, ,success_time=%s, ,response=(%d, %s)"
                                            % (thread_name, self.user_data["nickname"], visit_count, success_count, gid, price, success_time, res_data["res_code"], res_data["msg"]))

                                        break

                            else:
                                goods_list.remove(item)
                        elif mode == 2:
                            goods_list.remove(item)

                    end_milli = int(round(time.time() * 1000))

                    print("------%s....%s..第%d回合用时:%d......------------" % (thread_name, nickname, circle_count, int(end_milli-start_milli)))

                    if success_count >= self.count:
                        break

                    if not goods_list:
                        end_time = datetime.now().strftime(Util.YYYY_MM_DD_HH_MM_SS_FF)
                        print("\n------%s....%s..一个也没有抢到------------%s" % (thread_name, nickname, end_time))
                        break

        self.session.close()

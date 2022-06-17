from get_data import GetData
from database import Database

"""
--------Amos
"""
if __name__ == "__main__":

    flag = 0    # 0:表示入场   1:表示查询商品  2:表示抢购

    gt = GetData()
    db = Database()

    gt.login()

    if flag == 0:
        gt.join_buy()
    elif flag == 1:
        goods_list = gt.get_all_data([1, 9], list(range(0, 11)))
        sql = gt.process_data(goods_list)
        db.insert_goods_data(sql=sql)
    elif flag == 2:
        gt.get_user_gtime()
        gt.visit_all_goods(1, [0, 11000], 0)    # 抢几幅、价格区间、延迟几秒
